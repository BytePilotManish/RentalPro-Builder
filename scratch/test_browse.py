import tkinter as tk
from tkinter import filedialog
import sys

def browse():
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        folder = filedialog.askdirectory(parent=root, title="Select Output Saving Directory")
        root.destroy()
        return folder
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("Opening folder dialog...")
    folder = browse()
    print(f"Selected folder: {folder}")
