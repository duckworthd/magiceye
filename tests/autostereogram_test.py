import os
import unittest.mock

import mediapy
import numpy as np
import pytest
import torch

from magiceye import autostereogram


def test_e2e(tmp_path):
  """A basic end-to-end test to ensure the main script runs without crashing.

  This test mocks the expensive model loading and inference steps to keep it
  fast and self-contained, while still testing the depth map normalization logic.
  """
  # 1. Create dummy input files in a temporary directory.
  hidden_path = tmp_path / "hidden.png"
  pattern_path = tmp_path / "pattern.png"
  output_path = tmp_path / "output.png"

  # Create a simple hidden image (a white square on a black background).
  hidden_img = np.zeros((64, 128, 3), dtype=np.uint8)  # Non-square shape.
  hidden_img[16:48, 32:96, :] = 255
  mediapy.write_image(hidden_path, hidden_img)

  # Create a simple random noise pattern image.
  pattern_img = np.random.randint(0, 256, (16, 20, 3), dtype=np.uint8)  # Non-multiple shape
  mediapy.write_image(pattern_path, pattern_img)

  # 2. Create a dummy depth map that we expect the mocked model to return.
  # The values are not normalized, to test the normalization logic.
  dummy_raw_depth = np.zeros((64, 128), dtype=np.float32)
  dummy_raw_depth[16:48, 32:96] = 100.0
  dummy_raw_depth[0, 0] = 200.0  # To create a range for normalization.
  dummy_raw_depth = torch.Tensor(dummy_raw_depth)

  # 3. Create mocks for the model and transform functions.
  mock_model = unittest.mock.MagicMock()
  # The model's infer method should return our dummy depth map.
  mock_model.infer.return_value = {'depth': dummy_raw_depth}

  # The transform can be a simple pass-through function for the test.
  mock_transform = unittest.mock.MagicMock(side_effect=lambda x: x)

  # 4. Patch the function that loads the expensive model.
  with unittest.mock.patch(
      'depth_pro.create_model_and_transforms',
      return_value=(mock_model, mock_transform)) as mock_create_model:
    # 5. Run the main logic.
    autostereogram.run(hidden_path, pattern_path, output_path)

    # 6. Assert that the output was created and our mocks were used.
    mock_create_model.assert_called_once()
    mock_model.infer.assert_called_once()
    assert os.path.exists(output_path)