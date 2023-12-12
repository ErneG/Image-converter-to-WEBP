# Image Converter Script with GUI

This script automatically converts images added to specific folders to WEBP format and saves them to an output folder using a unique naming convention. It now includes a Tkinter-based GUI for easier control and monitoring.

## Features
- Monitors specified folders for new images and converts them to WEBP format.
- Unique naming for converted images: '[YYYYMMDD_HHMMSS]_[quality]_[original_filename:15].webp'.
- GUI for starting/stopping the monitoring process and viewing log messages.
- Error handling for continuous operation and specific error messages for file access and image processing issues.

## Configuration
- Set source folders and quality settings in `config.txt`.
- Specify the output and history folders in `config.txt`.

## How to Use
- Adjust `config.txt` with folder paths and quality settings.
- Run the script. The GUI will appear for control and monitoring.
- Use the 'Start' button to begin monitoring and 'Stop' to end it.
- View conversion logs and error messages directly in the GUI.
