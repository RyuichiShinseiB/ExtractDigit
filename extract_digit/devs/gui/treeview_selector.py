import tkinter as tk
from tkinter import ttk


def update_indices() -> None:
    # 右のTreeviewのすべての項目のインデックスを更新
    for i, item in enumerate(right_treeview.get_children()):
        item_text = right_treeview.item(item, "text").split(". ", 1)[-1]
        new_text = f"{i+1}. {item_text}"
        right_treeview.item(item, text=new_text)


def move_selected_items_above() -> None:
    selected_items = (
        left_treeview.selection()
    )  # 左のTreeviewで選択された項目のインデックスを取得
    selected_index_right = (
        right_treeview.selection()
    )  # 右のTreeviewで選択された項目のインデックスを取得
    if selected_index_right:
        index_right = right_treeview.index(selected_index_right[0])
        for item in selected_items:
            item_text = left_treeview.item(
                item, "text"
            )  # 左のTreeviewで選択された項目のテキストを取得
            new_item = right_treeview.insert(
                "", index_right, text=item_text
            )  # 右のTreeviewで選択された項目の上に追加
        update_indices()  # インデックスを更新


def move_selected_items_below() -> None:
    selected_items = (
        left_treeview.selection()
    )  # 左のTreeviewで選択された項目のインデックスを取得
    selected_index_right = (
        right_treeview.selection()
    )  # 右のTreeviewで選択された項目のインデックスを取得
    if selected_index_right:
        index_right = right_treeview.index(selected_index_right[0])
        for item in selected_items:
            item_text = left_treeview.item(
                item, "text"
            )  # 左のTreeviewで選択された項目のテキストを取得
            new_item = right_treeview.insert(
                "", index_right + 1, text=item_text
            )  # 右のTreeviewで選択された項目の下に追加
        update_indices()  # インデックスを更新


# メインウィンドウの作成
root = tk.Tk()
root.title("Treeview Example")

# 左のTreeviewの作成
left_treeview = ttk.Treeview(root, selectmode="extended")
left_treeview.heading("#0", text="Left Listbox", anchor="w")

# 右のTreeviewの作成
right_treeview = ttk.Treeview(root, selectmode="browse")
right_treeview.heading("#0", text="Right Listbox", anchor="w")

# 項目を左のTreeviewに追加
items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
items_ = {
    1: {
        "name": "Item 1",
        "contents": [f"1-{i} aaa" for i in range(5)],
    },
    2: {
        "name": "Item 2",
        "contents": [f"2-{i} bbb" for i in range(3)],
    },
    3: {
        "name": "Item 3",
        "contents": [f"3-{i} ccc" for i in range(1)],
    },
    4: {
        "name": "Item 4",
        "contents": [f"4-{i} ccc" for i in range(4)],
    },
}
for item in items_.values():
    i = left_treeview.insert("", "end", text=item["name"])

    for content in item["contents"]:
        left_treeview.insert(i, "end", text=content)

# 上に移動ボタンの作成
move_above_button = tk.Button(
    root, text="Move Above ->", command=move_selected_items_above
)
# 下に移動ボタンの作成
move_below_button = tk.Button(
    root, text="Move Below ->", command=move_selected_items_below
)

# ウィジェットの配置
left_treeview.grid(row=0, column=0)
move_above_button.grid(row=0, column=1, padx=10)
move_below_button.grid(row=1, column=1, padx=10)
right_treeview.grid(row=0, column=2, rowspan=3)

# メインループの実行
root.mainloop()
