import os
import shutil
import datetime
import threading
import queue as Queue
from PIL import Image as PILImage
from tkinter import *
from tkinter import scrolledtext
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def get_new_filename(original_path, quality):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Compact timestamp
    basename = os.path.splitext(os.path.basename(original_path))[0][:15]  # First 15 characters
    return f"{timestamp}_{quality}_{basename}.webp"

def convert_to_webp(image_path, output_path, quality, queue):
    try:
        with PILImage.open(image_path) as img:
            new_filename = get_new_filename(image_path, quality)
            output_file = os.path.join(output_path, new_filename)
            img.convert('RGB').save(output_file, 'webp', quality=quality)
            queue.put(f"Converted image: {new_filename}")
    except IOError as e:
        queue.put(f"IOError with file {image_path}: {e}")
    except Exception as e:
        queue.put(f"Error converting {os.path.basename(image_path)}: {e}")


        
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
    def __init__(self, quality, output_folder, queue):
        self.quality = quality
        self.output_folder = output_folder
        self.queue = queue

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            self.queue.put(f"Received event for: {event.src_path}")
            convert_to_webp(event.src_path, self.output_folder, self.quality, self.queue)


class GuiPart:
    def __init__(self, master, queue, start_command, stop_command):
        self.queue = queue
        self.master = master
        self.observers = []  # List to keep track of observer threads
        master.title("Image Converter")

        self.text_area = scrolledtext.ScrolledText(master, wrap=WORD, height=10)
        self.text_area.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.start_button = Button(master, text="Start", command=start_command)
        self.start_button.pack(pady=(0, 10))

        self.stop_button = Button(master, text="Stop", command=stop_command)
        self.stop_button.pack(pady=(0, 10))

    def process_incoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.text_area.insert(END, msg + '\n')
            except Queue.Empty:
                pass

    def on_window_close(self):
        if self.observers:
            for observer in self.observers:
                observer.stop()
            for observer in self.observers:
                observer.join()
        self.master.destroy()

            
def start_monitoring(queue):
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
            event_handler = WatchDirectory(quality, output_folder, queue)
            observer = Observer()
            observer.schedule(event_handler, folder_to_watch, recursive=False)
            observer.start()
            observers.append(observer)

    return observers


class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        start_monitoring(self.queue)

class WatchDirectory(FileSystemEventHandler):
    def __init__(self, quality, output_folder, queue):
        self.quality = quality
        self.output_folder = output_folder
        self.queue = queue

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            self.queue.put(f"Received event for: {event.src_path}")
            convert_to_webp(event.src_path, self.output_folder, self.quality, self.queue)
            

def main():
    root = Tk()
    queue = Queue.Queue()

    def start_command():
        gui.observers = start_monitoring(queue)

    gui = GuiPart(root, queue, start_command, root.quit)
    root.protocol("WM_DELETE_WINDOW", gui.on_window_close)

    def periodic_call():
        gui.process_incoming()
        root.after(100, periodic_call)

    periodic_call()
    root.mainloop()



if __name__ == "__main__":
    main()