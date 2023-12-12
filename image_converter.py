import os
import datetime
import queue as Queue
from PIL import Image as PILImage
from tkinter import *
from tkinter import filedialog, scrolledtext

def get_new_filename(original_path, quality):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    basename = os.path.splitext(os.path.basename(original_path))[0][:15]
    return f"{timestamp}_{quality}_{basename}.webp"

def convert_to_webp(image_path, output_path, quality, queue):
    try:
        with PILImage.open(image_path) as img:
            ensure_folder_exists(output_path)
            new_filename = get_new_filename(image_path, quality)
            output_file = os.path.join(output_path, new_filename)
            img.convert('RGB').save(output_file, 'webp', quality=quality)
            queue.put(f"Converted image: {new_filename}")
    except IOError as e:
        queue.put(f"IOError with file {image_path}: {e}")
    except Exception as e:
        queue.put(f"Error converting {os.path.basename(image_path)}: {e}")

def ensure_folder_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder: {folder}")

class GuiPart:
    def __init__(self, master, queue):
        self.queue = queue
        self.master = master
        self.file_path = None
        self.output_folder = StringVar(master, value='./OUTPUT')  # Default output folder
        self.quality = StringVar(master, value='75')  # Default quality value

        master.title("Image Converter")

        self.upload_button = Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        self.folder_button = Button(master, text="Choose Output Folder", command=self.choose_output_folder)
        self.folder_button.pack(pady=5)

        self.quality_label = Label(master, text="Quality (1-100):")
        self.quality_label.pack(pady=5)

        self.quality_entry = Entry(master, textvariable=self.quality)
        self.quality_entry.pack(pady=5)

        self.convert_button = Button(master, text="Convert", command=self.convert_image)
        self.convert_button.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(master, wrap=WORD, height=10)
        self.text_area.pack(padx=10, pady=10, fill=BOTH, expand=True)

    def upload_image(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpeg;*.jpg;*.png;*.bmp;*.gif")]
        )
        if self.file_path:
            self.text_area.insert(END, f"Selected file: {self.file_path}\n")

    def choose_output_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_folder.set(folder_selected)
            self.text_area.insert(END, f"Output folder set to: {folder_selected}\n")

    def convert_image(self):
        if self.file_path and self.quality.get().isdigit():
            quality_val = int(self.quality.get())
            output_folder = self.output_folder.get()
            ensure_folder_exists(output_folder)
            convert_to_webp(self.file_path, output_folder, quality_val, self.queue)
        else:
            self.queue.put("Please select an image and set a valid quality value.")

    def process_incoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.text_area.insert(END, msg + '\n')
            except Queue.Empty:
                pass

def main():
    root = Tk()
    queue = Queue.Queue()
    gui = GuiPart(root, queue)

    def periodic_call():
        gui.process_incoming()
        root.after(100, periodic_call)

    periodic_call()
    root.mainloop()

if __name__ == "__main__":
    main()
