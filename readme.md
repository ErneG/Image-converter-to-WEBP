# Image Converter Script with Enhanced GUI

This script features an enhanced GUI that allows users to manually select multiple images for conversion to WEBP format, specify the quality, choose the output folder, and view conversion logs.

## Features

-   Select multiple images for conversion using a file dialog.
-   Ability to choose the desired output folder for the converted images.
-   Specify the conversion quality for the WEBP format (1-100).
-   Converted images are saved in the selected output folder with unique naming: '[YYYYMMDD_HHMMSS]\_[quality]\_[original_filename:15].webp'.
-   Real-time log messages are displayed in the GUI, including conversion status and error messages for each image.
-   Toggleable dark mode for the GUI.

## Installation and Setup

Before running the Image Converter, ensure you have Python installed on your system. This application is developed and tested with Python 3.10.

1. **Clone or Download the Repository**:

    ```
    git clone https://github.com/SolidDeath/Image-converter-to-WEBP.git
    ```

    ```
    cd ImageConverter
    ```

2. **Set Up a Virtual Environment** (Optional but recommended):

-   Create a virtual environment:
    ```
    python -m venv venv
    ```
-   Activate the virtual environment:
    -   On Windows:
        ```
        .\venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```
        source venv/bin/activate
        ```

3. **Install Dependencies**:

```
    pip install -r requirements.txt
```

4. **Run the Application**:

```
    python -m src.app
```

## Usage

-   Run the script to open the GUI.
-   Click 'Upload Image' to select one or more image files for conversion.
-   Click 'Choose Output Folder' to select a folder where the converted images will be saved.
-   Enter the desired quality for the WEBP conversion in the provided field.
-   Click 'Convert' to start the conversion process for all selected images.
-   View the status of each conversion and any error messages in the text area of the GUI.

## Contributions

Contributions to the Image Converter project are welcome. Please consider forking the project, making your changes, and submitting a pull request.

## License

MIT
