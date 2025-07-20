# Overview

I'm writing a small command line tool for generating autostereograms from RGB images. The command line tool will take in 2 images: one for generating the "hidden" image and one for generating a pattern. For example,

```
> ls
hidden.jpg pattern.jpg

> autostereogram --hidden=example.jpg --pattern=pattern.jpg --output=output.jpg

> ls
hidden.jpg pattern.jpg output.jpg
```

# Details

The output image should have the same resollution as the hidden image.

The pattern image does NOT contain the pattern itself. Instead, it contains the element that should be tiled over and over to create a pattern. This may require resizing the pattern to something smaller and tiling it. Choose an appropriate number of times to tile along both height and width.

Autostereograms require depth maps. Use Apple's Depth Pro, running on the local machine, to generate depth maps.

Implement this project in Python, using `uv` to manage the Python version and dependencies. Use `mediapy` for loading and saving images. Use `absl` for flags and logging. Use 'pathlib' for managing filepaths.

# Plan Generation

Start by writing a step-by-step plan for implementing this project. Break down larger steps into individual commit-sized tasks. Formulate this as a TODO list and save it as `TODOs.md`

For each task, generate a prompt for modifying the codebase to add this new functionality.
