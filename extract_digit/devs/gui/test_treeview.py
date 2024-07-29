import tkinter as tk
from collections.abc import Callable, Iterable
from tkinter import ttk
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


class MyApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Screen")
        self.selectable_process = ProcessLists(self).add_processes(PROCESSES)
        self.selectable_process.pack(side="left")

        self.add_btn_frame = ttk.Frame(self)
        self.top_add_btn = ttk.Button(
            self.add_btn_frame, text=
        )

        self.selected_process = ProcessLists(self)
        self.selected_process.pack(side="right")


class ProcessLists(ttk.Frame):
    def __init__(self, master_window: tk.Tk) -> None:
        super().__init__(master_window)
        self.listview_frame = ttk.Frame(self)
        self.scrollbar = ttk.Scrollbar(self.listview_frame)
        self.process_list = ttk.Treeview(
            self.listview_frame, yscrollcommand=self.scrollbar.set, show="tree"
        )
        self.scrollbar.configure(command=self.process_list.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.process_list.pack(side="left", fill="both", expand=True)
        self.listview_frame.pack(side="top")

        self.clear_btn = ttk.Button(
            self, text="clear", command=self.on_clear_btn
        )
        self.clear_btn.pack(side="bottom")

        # self.submit_btn = ttk.Button(
        #     self, text="submit", command=self.on_submit_btn
        # )
        # self.submit_btn.pack(side="right")

    def on_clear_btn(self) -> None:
        selects = self.process_list.selection()
        self.process_list.selection_remove(selects)

    # def on_submit_btn(self) -> None:
    #     selects = self.process_list.selection()
    #     print([self.process_list.item(item) for item in selects])

    def add_processes(
        self, processes: Iterable[dict[TreeViewOptionStrT, Any]]
    ) -> "ProcessLists":
        try:
            for process in processes:
                self.process_list.insert("", "end", **process)
        except TypeError as e:
            print(e)
        return self

class AddButtonFrame(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.add_to_top_btn = ttk.Button(self, text="add to top", command=self.on_add_to_top)
        self.add_to_above_btn = ttk.Button(self, text="add to above", command=self.on_add_to_above)
        self.add_to_below_btn = ttk.Button(self, text="add to below", command=self.on_add_to_below)
        self.add_to_bottom_btn = ttk.Button(self, text="add to bottom", command=self.on_add_to_bottom)

    def on_add_to(
        self,
        place: Literal["top", "above", "below", "bottom"],
        src_list: ttk.Treeview,
        dst_list: ttk.Treeview
    ) -> Callable:
        src_processes_ids = src_list.selection()
        dst_process_id = dst_list.()
        src_processes = [src_list.item(src_id) for src_id in src_processes_ids]
        dst_list.insert("", )
        pass

# root = MyApp()
# scrollbar = ttk.Scrollbar(root)
# listbox = ttk.Treeview(root, yscrollcommand=scrollbar.set, show="tree")
# scrollbar.configure(command=listbox.yview)

# scrollbar.pack(side="right", fill="y")
# listbox.pack(side="left", fill="both", expand=True)

# for i in range(100):
#     text = f"Item #{i+1}"
#     listbox.insert("", "end", text=text)

# root.mainloop()
