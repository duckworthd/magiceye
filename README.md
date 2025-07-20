# Magic Eye: Autostereogram Generator

This repository contains a short demo for generating autostereogram ("magic eye") images.

## Usage

```bash
# Clone the Github repository
git clone https://github.com/duckworthd/magiceye.git
cd magiceye

# Download DepthPro model checkpoint to ./checkpoints/
# ... See https://github.com/apple/ml-depth-pro for details ...
mkdir checkpoints

python -m pip instal uv 
uv run magiceye \
  --hidden=images/jane.jpg \
  --pattern=images/cats.jpg \
  --output=images/output.jpg \
  --max_depth=3.0
```

## Development

Run unit tests with,

```bash
uv run pytest
```