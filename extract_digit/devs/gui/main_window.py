import tkinter as tk
from tkinter import ttk


class Application(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.master: tk.Tk

        self.master.geometry("300x300")
        print(type(master))
        self.master.title("Tkinter with Class Template")

        self.create_widgets()
        self.pack()

    def create_widgets(self) -> None:
        pass

    def callBack(self) -> None:
        pass


def main() -> None:
    root = tk.Tk()
    app = Application(master=root)  # Inherit
    app.mainloop()


if __name__ == "__main__":
    main()
