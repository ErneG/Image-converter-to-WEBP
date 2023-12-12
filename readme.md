# Image Converter Script

This script monitors multiple folders for new images, converts them to WEBP format, and saves them to an output folder. It also moves existing output files to a history folder each time the script runs, ensuring unique preservation by appending a timestamp to any duplicate filenames.

## Configuration
- Define source folders and their respective qualities in `config.txt`.
- Specify the output folder and history folder in `config.txt`.

## How to Use
- Update `config.txt` with your folder paths and quality settings.
- Run the script. It will manage the output and history folders, avoiding any file overwrite issues.
