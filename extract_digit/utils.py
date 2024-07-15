import tkinter as tk
from tkinter import filedialog

doc_path = ""


def load_file() -> None:
    global doc_path
    doc_path = filedialog.askopenfilename(
        filetypes=[("image files", ("*.jpg", "*.png", "*.JPEG"))]
    )


def main() -> None:
    root = tk.Tk()
    root.title("some")
    load_file_btn = tk.Button(root, text="load a file", command=load_file)
    load_file_btn.pack()
    root.mainloop()


def select_img_with_window() -> str:
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        filetypes=[("image files", ("*.jpg", "*.png", "*.JPEG"))]
    )
    return path


def select_directory_with_window() -> str:
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    return path
