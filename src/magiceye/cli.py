from absl import app
from absl import flags
import pathlib
import numpy as np

from . import autostereogram

FLAGS = flags.FLAGS

flags.DEFINE_string("hidden", None, "Path to the hidden image.", required=True)
flags.DEFINE_string("pattern",
                    None,
                    "Path to the pattern image.",
                    required=True)
flags.DEFINE_string("output",
                    None,
                    "Path to save the generated autostereogram.",
                    required=True)
flags.DEFINE_float("max_depth", np.inf,
                   "Ignore depth values greater than this. In meters.")
flags.DEFINE_float("max_disparity", 0.33,
                   "Maximum offset due to disparity, as a fraction of pattern width.")
flags.DEFINE_float(
    "pattern_width", 0.125,
    "Pattern's width, as a fraction of image width.")


def _main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments")

  autostereogram.run(pathlib.Path(FLAGS.hidden),
                     pathlib.Path(FLAGS.pattern),
                     pathlib.Path(FLAGS.output),
                     max_disparity=FLAGS.max_disparity,
                     pattern_width=FLAGS.pattern_width,
                     max_depth=FLAGS.max_depth)


def main():
  """Script entry point that calls app.run()."""
  app.run(_main)


if __name__ == "__main__":
  main()
