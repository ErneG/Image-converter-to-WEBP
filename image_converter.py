import os
import shutil
import datetime
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def convert_to_webp(image_path, output_path, quality):
    try:
        with Image.open(image_path) as img:
            output_file = os.path.join(output_path, os.path.basename(image_path) + '.webp')
            img.convert('RGB').save(output_file, 'webp', quality=quality)
            print(f"Converted image: {os.path.basename(image_path)} at quality {quality}")
    except Exception as e:
        print(f"Error converting {os.path.basename(image_path)}: {e}")

def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

def ensure_folder_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder: {folder}")

def move_files_to_history(output_folder, history_folder):
    for file in os.listdir(output_folder):
        original_path = os.path.join(output_folder, file)
        new_path = os.path.join(history_folder, file)
        
        # Check if the file already exists in the history folder
        if os.path.exists(new_path):
            # Create a new file name with a timestamp to prevent overwriting
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            basename, extension = os.path.splitext(file)
            new_filename = f"{basename}_{timestamp}{extension}"
            new_path = os.path.join(history_folder, new_filename)
        
        shutil.move(original_path, new_path)

class WatchDirectory(FileSystemEventHandler):
    def __init__(self, quality, output_folder):
        self.quality = quality
        self.output_folder = output_folder

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            print(f"Received event for: {event.src_path}")
            convert_to_webp(event.src_path, self.output_folder, self.quality)

if __name__ == "__main__":
    config = read_config('config.txt')
    output_folder = config['OUTPUT_FOLDER']
    history_folder = config['HISTORY_FOLDER']
    
    ensure_folder_exists(output_folder)
    ensure_folder_exists(history_folder)
    move_files_to_history(output_folder, history_folder)

    observers = []
    for key, value in config.items():
        if key.startswith('FOLDER_'):
            quality = int(key.split('_')[1])
            folder_to_watch = value
            ensure_folder_exists(folder_to_watch)
            event_handler = WatchDirectory(quality, output_folder)
            observer = Observer()
            observer.schedule(event_handler, folder_to_watch, recursive=False)
            observer.start()
            observers.append(observer)
            print(f"Monitoring {folder_to_watch} at quality {quality}")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
        for observer in observers:
            observer.join()
        print("Stopped monitoring.")
