from absl import logging
import pathlib
import chex
import depth_pro
from matplotlib import pyplot as plt
import mediapy
import numpy as np
import os
import torch


def run(hidden_image_path: pathlib.Path,
        pattern_image_path: pathlib.Path,
        output_path: pathlib.Path,
        max_disparity: float = 0.1,
        pattern_width: float = 0.125,
        max_depth: float = np.inf):
  """Generates a magic eye image.
  
  Args:
    hidden_image_path: Path to RGB image to hide in the magic eye.
    pattern_image_path: Path to the image to use as a repeating pattern.
    output_path: Path to save the generated magic eye image.
    max_disparity: Maximum disparity, as a fraction of pattern width.
    pattern_width: Pattern's width, as a fraction of image width.
    max_depth: Ignore depth values greater than this.
  """
  logging.info(f"Loading images...")
  hidden_image = mediapy.read_image(hidden_image_path)
  pattern_image = mediapy.read_image(pattern_image_path)

  logging.info(f'hidden={hidden_image.shape} pattern={pattern_image.shape}')
  height, width, _ = hidden_image.shape

  logging.info("Creating pattern...")
  pattern_width_px = width * pattern_width
  pattern_image = create_pattern_image(pattern_image,
                                       pattern_width=pattern_width_px)

  logging.info("Predicting depth map...")
  depth_npy_path = output_path.parent / f'{hidden_image_path.stem}.depth.npy'
  depth_png_path = output_path.parent / f'{hidden_image_path.stem}.depth.png'

  if os.path.exists(depth_npy_path):
    depth_map = np.load(depth_npy_path)
  else:
    depth_map = infer_depth(hidden_image)
    np.save(depth_npy_path, depth_map)

  disparity_map = depth_to_disparity(depth_map, max_depth=max_depth)
  mediapy.write_image(depth_png_path, colorize(disparity_map))

  logging.info("Building autostereogram...")
  max_disparity_px = pattern_width_px * max_disparity
  autostereogram = generate_autostereogram(pattern_image, disparity_map,
                                           max_disparity_px)

  mediapy.write_image(output_path, autostereogram)


def create_pattern_image(pattern_image: np.ndarray,
                         pattern_width: float) -> np.ndarray:
  """Creates an appropriately-sized pattern for a magic eye image.."""
  logging.info("Resizing and tiling pattern...")
  h, w, _ = pattern_image.shape

  # Resize the pattern to be small relative to the hidden image.
  H = int(pattern_width)
  W = int(pattern_width * (h / w))
  resized_pattern = mediapy.resize_image(pattern_image, (H, W))
  logging.info(f"Resized pattern from {w}x{h} to {H}x{W}.")

  return resized_pattern


def create_random_pattern_image(pattern_width: float) -> np.ndarray:
  """Creates a square, random, white noise image."""
  # Resize the pattern to be small relative to the hidden image.
  target_p_width = int(pattern_width)
  target_p_height = int(pattern_width)
  shape = (target_p_height, target_p_width, 1)
  pattern = np.random.default_rng(0).integers(0, 255, size=shape)
  pattern = np.broadcast_to(pattern, (target_p_height, target_p_width, 3))
  pattern = pattern.astype(np.uint8)
  return pattern


def infer_depth(image: np.ndarray) -> np.ndarray:
  """Estimate the depth of each pixel, in meters."""
  chex.assert_shape(image, (None, None, 3))
  h, w, c = image.shape

  logging.info("Initializing DepthPro...")
  device = torch.device('cpu')
  if torch.cuda.is_available():
    device = torch.device('cuda')
  model, transform = depth_pro.create_model_and_transforms(device=device)

  logging.info("Running inference...")
  image = transform(image)
  outputs = model.infer(image)
  depth = outputs['depth']
  depth = depth.detach().cpu().numpy()
  chex.assert_shape(depth, (h, w))

  return depth


def generate_autostereogram(pattern: np.ndarray, disparity_map: np.ndarray,
                            max_shift: float) -> np.ndarray:
  """Generates the magic eye image.
  
  Args:
    pattern: f32[h,w,C]. Pattern to use as background.
    disparity_map: f32[H,W]. 1 / depth of each pixel, normalized in [0, 1].
    max_shift: Maximum number of pixels to shift, based on disparity map.
  """
  H, W = disparity_map.shape
  h, w, C = pattern.shape
  if max_shift > w:
    raise ValueError("Maximum pixel shift must be smaller than pattern width.")

  result = np.zeros((H, W + w, C), dtype=pattern.dtype)
  for y in range(H):
    for x in range(W + w):
      if x < w:
        result[y, x] = pattern[y % h, x]
      else:
        shift = int(disparity_map[y, x - w] * max_shift)
        result[y, x] = result[y, x - w + shift]

  return result


def depth_to_disparity(depth: np.ndarray,
                       min_depth: float = 0.1,
                       max_depth: float = np.inf,
                       buffer: float = 0.0,
                       epsilon: float = 1e-3) -> np.ndarray:
  """Constructs a normalized disparity map.
  
  Args: 
    depth: f32[H,W]. Depth of each pixel in meters.
    min_depth: Minimum allowed depth in meters.
    max_depth: Maximum allowed depth in metters.
    buffer: Increase to push background backwards.
    epsilon: Increase to push foreground backwards.
  
  Returns:
    f32[H,W]. Disparity of each pixel, normalized in [0, 1].
  """
  too_close = depth < min_depth
  too_far = depth > max_depth
  is_valid = (~too_close) & (~too_far)
  if not np.any(is_valid):
    bounds = depth.min(), depth.max()
    raise ValueError(f"Depth values in {bounds}")
  depth[too_close] = min_depth
  depth[too_far] = max_depth

  # Convert to disparity.
  disparity = 1.0 / (depth + epsilon)

  # Squash valid pixels to [0, 1].
  valid = disparity[is_valid]
  upper = np.max(valid)
  lower = np.min(valid)
  disparity = (disparity - lower) / (upper - lower)
  disparity = np.clip(disparity, 0, 1)

  # Separate foreground from background.
  disparity = (disparity + buffer) / (1 + buffer)
  disparity[too_close] = 1.0
  disparity[too_far] = 0.0

  return disparity


def colorize(depth: np.ndarray) -> np.ndarray:
  """Generates an RGB depth map visualization."""
  chex.assert_shape(depth, (None, None))
  cmap = plt.get_cmap('turbo')
  return cmap(depth)
