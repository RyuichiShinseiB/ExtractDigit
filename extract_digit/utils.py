import queue
import tkinter as tk
from tkinter import filedialog
from typing import Sequence, overload

import matplotlib.pyplot as plt

# from .param_config import Point
from extract_digit.param_config import Point, numT

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


class Quadraliteral:
    @overload
    def __init__(self, vertices: Sequence[Point] | None = None) -> None: ...
    @overload
    def __init__(
        self, vertices: Sequence[tuple[numT, numT]] | None = None
    ) -> None: ...
    def __init__(
        self,
        vertices: Sequence[tuple[numT, numT]] | Sequence[Point] | None = None,
    ) -> None:
        self.points: queue.Queue[Point] = queue.Queue(4)
        self._x_points: queue.Queue[numT] = queue.Queue(4)
        self._y_points: queue.Queue[numT] = queue.Queue(4)
        if vertices is not None:
            if len(vertices) > 4:
                raise ValueError("The number of elements must be four")
            for vertice in vertices:
                self._x_points.put(
                    vertice.x if isinstance(vertice, Point) else vertice[0]
                )
                self._y_points.put(
                    vertice.y if isinstance(vertice, Point) else vertice[0]
                )
                self.points.put(
                    vertice
                    if isinstance(vertice, Point)
                    else Point(vertice[0], vertice[1])
                )

    @property
    def x_points(self) -> tuple[numT, ...]:
        return tuple(self._x_points.queue)

    @property
    def y_points(self) -> tuple[numT, ...]:
        return tuple(self._y_points.queue)

    def set_point(self, point: tuple[numT, numT] | Point) -> "Quadraliteral":
        if self._x_points.full():
            self._x_points.get()
        if self._y_points.full():
            self._y_points.get()
        self._x_points.put(point[0])
        self._y_points.put(point[1])
        return self


def gui_test() -> None:
    from matplotlib.backend_bases import MouseEvent

    def motion(event: MouseEvent) -> None:
        x = event.xdata
        y = event.ydata
        # print(x, y)

        if x is not None and y is not None:
            ql.set_point((x, y))
            print(ql.x_points, ql.y_points)
            ln.set_data(ql.x_points, ql.y_points)
        plt.draw()

    fig = plt.figure()
    ql = Quadraliteral()
    (ln,) = plt.plot([], [], "x")

    fig.canvas.mpl_connect("button_release_event", motion)  # type: ignore
    plt.show()


if __name__ == "__main__":
    # lifo: queue.Queue[int] = queue.Queue(4)
    # lifo.put(4)
    # lifo.put(0)
    # lifo.put(8)
    # lifo.put(9)
    # print(lifo.queue)
    # print(lifo.get())
    # lifo.put(3)
    # print(lifo.get())
    gui_test()
