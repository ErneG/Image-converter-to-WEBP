# Image Converter Script

This script monitors multiple folders for new images, converts them to WEBP format, and saves them to an output folder. Previous outputs are moved to a history folder each time the script runs.

## Configuration
- Define source folders and their respective qualities in `config.txt`.
- Specify the output folder and history folder in `config.txt`.

## How to Use
- Update `config.txt` with your folder paths and quality settings.
- Run the script. It will move existing output files to the history folder, monitor the specified folders, and convert new images to WEBP format.
