import tkinter as tk
from .gui import GuiPart
import queue as Queue

def main():
    root = tk.Tk()
    queue = Queue.Queue()
    gui = GuiPart(root, queue)

    def periodic_call():
        """Process incoming queue messages and update GUI."""
        gui.process_incoming()
        root.after(50, periodic_call)

    periodic_call()
    root.mainloop()

if __name__ == "__main__":
    main()
