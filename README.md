# Magic Eye: Autostereogram Generator

This repository contains a short demo for generating autostereogram ("magic eye") images.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/duckworthd/magiceye.git
    cd magiceye
    ```

2.  **Install locally:**

    ```bash
    pip install uv
    uv pip install --editable .
    ```

4.  **Download Depth Pro Checkpoints:**

    Download the Depth Pro model checkpoints from [Apple's repository](https://github.com/apple/ml-depth-prediction) and place them in the `./checkpoints/` directory within the project.

## Usage

```bash
uv run magiceye
  --hidden=images/jane.jpg
  --pattern=images/cats.jpg
  --output=images/output.jpg
  --max_depth=3.0
```

## Development

Run unit tests with,

```bash
uv pip install -e . --with test
uv run pytest
```