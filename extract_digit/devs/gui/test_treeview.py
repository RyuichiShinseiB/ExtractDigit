import tkinter as tk
from collections.abc import Iterable, Sequence
from tkinter import messagebox, ttk
from typing import Any, Literal, TypeAlias

ProcessNameStrT: TypeAlias = str
TreeViewOptionStrT: TypeAlias = Literal[
    "text", "image", "values", "open", "tags"
]
PROCESSES: list[dict[TreeViewOptionStrT, Any]] = [
    {"text": "crop", "values": 0},
    {"text": "binarize", "values": 1},
    {"text": "find edge", "values": 2},
    {"text": "estimate", "values": 3},
]


class MyApp(tk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.process_list = ProcessList(self).add_processes(PROCESSES)

        self.exce_process_list = ExecutionProcessList(self)

        self.btn = AddButtonFrame(
            self,
            self.process_list.process_list.listbox,
            self.exce_process_list.process_list.listbox,
        )
        self.process_list.grid(row=0, column=0, sticky="ns")
        self.btn.grid(row=0, column=1, sticky="ns")
        self.exce_process_list.grid(row=0, column=2, sticky="ns")


class ScrollListbox(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.scrollbar = ttk.Scrollbar(self)
        self.listbox = tk.Listbox(
            self,
            yscrollcommand=self.scrollbar.set,
            selectmode="extended",
            exportselection=False,
        )
        self.scrollbar.configure(command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)


class ProcessList(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.process_list = ScrollListbox(self)
        self.process_list.pack(
            side="top",
        )

        self.clear_btn = ttk.Button(
            self, text="selection clear", command=self.on_clear_btn
        )
        self.clear_btn.pack(side="bottom")

    def on_clear_btn(self) -> None:
        self.process_list.listbox.select_clear(0, tk.END)

    def add_processes(
        self, processes: Iterable[dict[TreeViewOptionStrT, Any]]
    ) -> "ProcessList":
        try:
            for i, process in enumerate(processes):
                self.process_list.listbox.insert(i, process["text"])
        except TypeError as e:
            print(e)
        return self


class ExecutionProcessList(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.process_list = ScrollListbox(self)
        self.process_list.listbox.config(selectmode="single")
        self.process_list.pack(side="top")

        self.btn_frame = ttk.Frame(self)
        self.reset_btn = ttk.Button(
            self.btn_frame,
            text="reset",
            command=self.on_reset_btn,
        )
        self.remove_btn = ttk.Button(
            self.btn_frame, text="remove", command=self.on_remove_btn
        )
        self.reset_btn.grid(row=0, column=0)
        self.remove_btn.grid(row=0, column=1)
        self.btn_frame.pack(side="bottom")

    def on_reset_btn(self) -> None:
        is_reseting = messagebox.askokcancel(
            "Warning", "Are you sure you want to delete all your settings?"
        )
        if is_reseting:
            self.process_list.listbox.delete(0, tk.END)

    def on_remove_btn(self) -> None:
        selected = self.process_list.listbox.curselection()
        for i in selected:
            self.process_list.listbox.delete(i)

    def add_processes(
        self, processes: Iterable[dict[TreeViewOptionStrT, Any]]
    ) -> "ExecutionProcessList":
        try:
            for i, process in enumerate(processes):
                self.process_list.listbox.insert(i, process["text"])
        except TypeError as e:
            print(e)
        return self


class AddButtonFrame(ttk.Frame):
    def __init__(
        self, master: tk.Misc, src_listbox: tk.Listbox, dst_listbox: tk.Listbox
    ) -> None:
        super().__init__(master)
        self.src_listbox = src_listbox
        self.dst_listbox = dst_listbox
        self.add_to_top_btn = ttk.Button(
            self, text="add to top", command=self.on_add_to_top
        )
        self.add_to_above_btn = ttk.Button(
            self, text="add to above", command=self.on_add_to_above_btn
        )
        self.add_to_below_btn = ttk.Button(
            self, text="add to below", command=self.on_add_to_below_btn
        )
        self.add_to_bottom_btn = ttk.Button(
            self, text="add to bottom", command=self.on_add_to_bottom_btn
        )

        self.add_to_top_btn.pack()
        self.add_to_above_btn.pack()
        self.add_to_below_btn.pack()
        self.add_to_bottom_btn.pack()

    def on_add_to_top(self) -> None:
        src_list_idxs: tuple[int] = self.src_listbox.curselection()
        self.add_dst_listbox(src_list_idxs, 0, "top")

    def on_add_to_above_btn(self) -> None:
        src_list_idxs: tuple[int] = self.src_listbox.curselection()
        try:
            dst_list_idx: int = self.dst_listbox.curselection()[0]
        except IndexError:
            dst_list_idx = 0
        self.add_dst_listbox(src_list_idxs, dst_list_idx, "above")

    def on_add_to_below_btn(self) -> None:
        src_list_idxs: tuple[int] = self.src_listbox.curselection()
        try:
            dst_list_id: int | str = self.dst_listbox.curselection()[-1] + 1
        except IndexError:
            dst_list_id = tk.END
        self.add_dst_listbox(src_list_idxs, dst_list_id, "below")

    def on_add_to_bottom_btn(self) -> None:
        src_list_idxs: tuple[int] = self.src_listbox.curselection()
        self.add_dst_listbox(src_list_idxs, tk.END, "bottom")

    def add_dst_listbox(
        self,
        idxs: Sequence[int],
        start_index: str | int,
        prefix: str | None = None,
    ) -> None:
        if len(idxs) == 0:
            return
        prefix = "none" if prefix is None else prefix
        for i, idx in enumerate(idxs):
            self.dst_listbox.insert(
                start_index
                if isinstance(start_index, str)
                else start_index + i,
                f"{prefix}: {self.src_listbox.get(idx)}",
            )
        self.update_indices()

    def update_indices(self) -> None:
        for i in range(self.dst_listbox.size()):
            item_text: str = self.dst_listbox.get(i)
            new_text = f"{i+1}. {item_text.split('. ', 1)[-1]}"
            self.dst_listbox.delete(i)
            self.dst_listbox.insert(i, new_text)


root = tk.Tk()
myapp = MyApp(root)
myapp.pack()

root.mainloop()
