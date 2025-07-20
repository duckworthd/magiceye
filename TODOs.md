# Autostereogram Command Line Tool TODOs

1.  **Project Setup:**
    *   \[x] Initialize the project with `uv`: Create `pyproject.toml` and set up the basic structure.
        *   Prompt: "Create a `pyproject.toml` file with necessary metadata (name, version, description, authors, license) and dependencies (`mediapy`, `absl-py`). Initialize a basic project structure with a `src` directory and a main script file (e.g., `src/autostereogram.py`)."
    *   \[x] Set up `absl` flags: Define flags for input hidden image, input pattern image, and output image.
        *   Prompt: "In `src/autostereogram.py`, import `absl` and define flags for `--hidden`, `--pattern`, and `--output`, specifying their types (string) and help messages."

2.  **Image Loading and Validation:**
    *   \[x] Implement image loading: Load the hidden and pattern images using `mediapy`.
        *   Prompt: "In `src/autostereogram.py`, implement a function to load images using `mediapy.read_image`. Handle potential file not found or invalid format errors with appropriate logging (using `absl.logging`)."

3.  **Pattern Handling:**
    *   \[x] Implement pattern tiling: Resize and tile the pattern image to create a full-size pattern matching the hidden image dimensions.
        *   Prompt: "Implement a function to resize the pattern image (if necessary) and tile it to match the dimensions of the hidden image.  Consider a reasonable default tiling factor or allow specifying it via a flag."

4.  **Depth Map Generation:**
    *   \[x] Integrate with Depth Pro: Add functionality to call Apple's Depth Pro to generate a depth map from the hidden image. Use the API described on [Github](https://github.com/apple/ml-depth-pro).
        *   Prompt: "Implement a function that executes Apple's Depth Pro's Python API. Normalize the depth map to [0, 1], where 1 is the farthest distance found in the depth map. Ensure that the RGB image passed to Depth Pro meets the API's expected shape requirements."

5.  **Autostereogram Generation:**
    *   \[x] Implement autostereogram algorithm: Implement the core algorithm to generate the autostereogram using the tiled pattern and the depth map.
        *   Prompt: "Implement the autostereogram generation algorithm. This involves iterating over the pixels of the output image, calculating pixel shifts based on the depth map, and determining the final pixel values from the tiled pattern. If possible, avoid doing this loop in Python and use vectorized numpy operations instead."

6.  **Output and Error Handling:**
    *   \[x] Save the output image: Save the generated autostereogram to the specified output path using `mediapy`.
        *   Prompt: "Implement code to save the generated autostereogram as an image file (e.g., JPG) using `mediapy.write_image` at the path specified by the `--output` flag."

7.  **Testing:**
    *   \[x] Add basic tests: Create basic tests to ensure the script runs without errors with valid inputs.
        *   Prompt: "Create a test suite (e.g., using `pytest`) and add basic tests to verify that the script runs without crashing for valid input images and produces an output image."