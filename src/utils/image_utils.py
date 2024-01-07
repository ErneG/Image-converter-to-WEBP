import os
import datetime
from PIL import Image, ImageSequence
import webp

def get_new_filename(original_path, quality):
    """
    Generate a new filename based on the original path, quality, and current timestamp.
    The new filename includes a timestamp, quality level, and the original file's base name.
    The filename is truncated to prevent excessively long names.

    :param original_path: Path of the original image file.
    :param quality: Quality setting for the new image.
    :return: New filename with a timestamp, quality, and original basename.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    basename = os.path.splitext(os.path.basename(original_path))[0][:15]
    return f"{timestamp}_{quality}_{basename}.webp"

def ensure_folder_exists(folder):
    """
    Ensure the specified folder exists. If not, create it.
    This function is used to make sure the output directory is available before saving files to it.

    :param folder: Path of the folder to check/create.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder: {folder}")

def convert_to_webp(image_path, output_path, quality, queue):
    """
    Convert an image file to WebP format. If the image is a GIF, it handles it differently to preserve animation.
    Exceptions during conversion are caught and reported back via the queue.

    :param image_path: Path of the original image file.
    :param output_path: Path for saving the converted image.
    :param quality: Quality setting for the new image.
    :param queue: Queue to put status messages or errors.
    """
    try:
        if image_path.lower().endswith('.gif'):
            convert_gif_to_webp(image_path, output_path, quality, queue)
        else:
            convert_single_image_to_webp(image_path, output_path, quality, queue)
    except Exception as e:
        queue.put(f"Error converting {os.path.basename(image_path)}: {e}")

def convert_single_image_to_webp(image_path, output_path, quality, queue):
    """
    Convert a non-GIF image file to WebP format.
    The function converts the image to RGB mode before saving to handle images with alpha channels.

    :param image_path: Path of the original image file.
    :param output_path: Path for saving the converted image.
    :param quality: Quality setting for the new WebP image.
    :param queue: Queue to put status messages.
    """
    with Image.open(image_path) as img:
        ensure_folder_exists(output_path)
        new_filename = get_new_filename(image_path, quality)
        output_file = os.path.join(output_path, new_filename)
        img.convert('RGB').save(output_file, 'webp', quality=quality)
        queue.put(f"Converted image: {output_file}")

def convert_gif_to_webp(gif_path, output_path, quality, queue):
    """
    Convert a GIF image file to an animated WebP format.
    Each frame of the GIF is extracted and combined into a single animated WebP.

    :param gif_path: Path of the original GIF file.
    :param output_path: Path for saving the converted image.
    :param quality: Quality setting for the new WebP image.
    :param queue: Queue to put status messages.
    """
    ensure_folder_exists(output_path)
    new_filename = get_new_filename(gif_path, quality)
    output_file = os.path.join(output_path, new_filename)

    with Image.open(gif_path) as img:
        frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
        webp.save_images(frames, output_file, quality=quality, method=6)
        queue.put(f"Converted image: {output_file}")
