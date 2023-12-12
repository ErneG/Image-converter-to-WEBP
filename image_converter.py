from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def convert_to_webp(image_path):
    with Image.open(image_path) as img:
        img.convert('RGB').save(image_path + '.webp', 'webp')

class WatchDirectory(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            convert_to_webp(event.src_path)

folder_to_watch = './images'  # Set folder path here

if __name__ == "__main__":
    event_handler = WatchDirectory()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
