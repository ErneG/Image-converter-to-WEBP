from queue import Queue
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import threading
from src.utils.image_utils import convert_to_webp, ensure_folder_exists

class GuiPart:
    def __init__(self, master, queue):
        """
        Initialize the GUI components.
        :param master: Tkinter root or parent window.
        :param queue: Queue for communication between threads.
        """
        self.queue = queue
        self.master = master
        self.file_paths = []
        self.quality = tk.StringVar(master, value='75')
        self.dark_mode = tk.BooleanVar(value=False)
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface components.
        """
        self.master.title("Image Converter")

        style = ttk.Style()
        style.theme_use('clam')

        # Upload Image Button
        self.upload_button = ttk.Button(self.master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        # Quality Setting
        self.quality_label = ttk.Label(self.master, text="Quality (1-100):")
        self.quality_label.pack(pady=5)
        self.quality_entry = ttk.Entry(self.master, textvariable=self.quality)
        self.quality_entry.pack(pady=5)

        # Choose Output Folder Button
        self.folder_button = ttk.Button(self.master, text="Choose Output Folder", command=self.choose_output_folder)
        self.folder_button.pack(pady=5)

        # Note about default output folder
        self.default_folder_note = ttk.Label(self.master, text="Note: If no output folder is selected, a default 'OUTPUT' folder will be created at the root of the app.")
        self.default_folder_note.pack(pady=5)

        # Convert Button
        self.convert_button = ttk.Button(self.master, text="Convert", command=self.convert_image_thread)
        self.convert_button.pack(pady=5)

        # Dark Mode Toggle
        self.toggle_dark_mode_button = ttk.Checkbutton(self.master, text="Dark Mode", var=self.dark_mode, command=self.toggle_dark_mode)
        self.toggle_dark_mode_button.pack(pady=5)

        # Text Area for Messages
        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, height=10)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_area.configure(state='disabled')  # Make the text area read-only
        
        
    def upload_image(self):
        """
        Handle the image upload action.
        """
        self.file_paths = filedialog.askopenfilenames(
            filetypes=[("Image Files", "*.jpeg;*.jpg;*.png;*.bmp;*.gif")]
        )
        if self.file_paths:
            selected_files = "\n".join(self.file_paths)
            self.insert_text(f"Selected files:\n{selected_files}\n")

    def choose_output_folder(self):
        """
        Handle the action for choosing an output folder.
        """
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_folder = folder_selected
            self.insert_text(f"Output folder set to: {folder_selected}\n")

    def convert_image_thread(self):
        """
        Create a thread for image conversion to prevent the UI from freezing during the process.
        """
        thread = threading.Thread(target=self.convert_image)
        thread.start()


    def convert_image(self):
        """
        Convert the selected images using the specified quality.
        """
        if self.file_paths and self.quality.get().isdigit():
            quality_val = int(self.quality.get())
            output_folder = getattr(self, 'output_folder', './OUTPUT')
            ensure_folder_exists(output_folder)
            for file_path in self.file_paths:
                convert_to_webp(file_path, output_folder, quality_val, self.queue)
        else:
            self.queue.put("Please select images and set a valid quality value.")

    def insert_text(self, message):
        """
        Insert text into the text area and ensure the text area remains read-only for the user.
        """
        self.text_area.configure(state='normal')  # Temporarily enable the widget to modify its contents
        self.text_area.insert(tk.END, message + '\n')
        self.text_area.configure(state='disabled')  # Disable the widget to make it read-only
        
    def process_incoming(self):
        """
        Process incoming messages from the queue and update the GUI.
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.insert_text(msg)  # Use the new insert_text method
            except Queue.Empty:
                pass


    def toggle_dark_mode(self):
        """
        Toggle the dark mode theme for the GUI.
        """
        bg_color = '#333333' if self.dark_mode.get() else 'SystemButtonFace'
        fg_color = '#aaaaaa' if self.dark_mode.get() else 'SystemWindowText'
        btn_color = '#555555' if self.dark_mode.get() else 'SystemButtonFace'

        self.master.configure(background=bg_color)

        # Update ttk style for dark mode
        style = ttk.Style()
        style.configure('TButton', background=btn_color, foreground=fg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TEntry', fieldbackground=bg_color, foreground=fg_color, insertbackground=fg_color)

        # Correct style for TCheckbutton to ensure it looks like a checkbox
        style.map('TCheckbutton',
                background=[('active', bg_color), ('selected', bg_color)],
                foreground=[('active', fg_color), ('selected', fg_color)])

        self.text_area.configure(background=bg_color, fg=fg_color)
        self.quality_entry.configure(style='TEntry')

        for widget in [self.upload_button, self.folder_button, self.convert_button]:
            widget.configure(style='TButton')
        self.quality_label.configure(style='TLabel')
        self.toggle_dark_mode_button.configure(style='TCheckbutton')  # Apply the correct style

