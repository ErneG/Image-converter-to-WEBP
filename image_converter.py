from PIL import Image

def convert_to_webp(image_path):
    """
    Convert an image to WEBP format.
    :param image_path: Path to the input image file.
    """
    with Image.open(image_path) as img:
        img.convert('RGB').save(image_path + '.webp', 'webp')

image_path = 'image.jpg'
convert_to_webp(image_path)
