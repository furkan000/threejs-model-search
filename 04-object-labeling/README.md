# Automated Labeling

## Overview

This project contains scripts for rendering 3D meshes from a scene and generating descriptive captions for the rendered images. The rendering process uses `trimesh` and `pyrender` libraries, while the captioning process leverages the BLIP model and the OpenAI API for generating coherent descriptions.

## Files

1. **render.py**: Renders 3D meshes from a GLB file, saves the rendered images.
2. **caption.py**: Generates captions for the rendered images using a pre-trained BLIP model and combines them using GPT-4o.

## Requirements

- A GLB file to render (`cafeteria.glb` in the example).
- OpenAI API key set as an environment variable `OPENAI_API_KEY`.

## Setup

1. Install the required Python packages:

   ```bash
   pip install -r ../requirements.txt
   ```

2. Set the OpenAI API key:

   ```bash
   export OPENAI_API_KEY='your_openai_api_key'
   ```

3. (Optional) If you want to render a different GLB file (default is `cafeteria.glb`), follow these steps:

   - Place your GLB file in the `./models` directory.
   - Update the `path_to_model` variable in the `render.py` file to point to your GLB file. For example:

   ```python
   path_to_model = "./models/your_model.glb"
   ```

## Usage

1. **Rendering 3D Meshes**: Run the `render.py` script to render the 3D meshes from the GLB file.

   ```bash
   python render.py
   ```

   This will generate rendered images and save them in the `./render` directory.

2. **Generating Captions**: Run the `caption.py` script to generate captions for the rendered images.

   ```bash
   python caption.py
   ```