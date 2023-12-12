from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def convert_to_webp(image_path, quality):
    with Image.open(image_path) as img:
        img.convert('RGB').save(image_path + '.webp', 'webp', quality=quality)

def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

class WatchDirectory(FileSystemEventHandler):
    def __init__(self, quality):
        self.quality = quality

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            convert_to_webp(event.src_path, self.quality)

if __name__ == "__main__":
    config = read_config('config.txt')
    folder_to_watch = config['FOLDER_TO_WATCH']
    quality = int(config['QUALITY'])

    event_handler = WatchDirectory(quality)
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
