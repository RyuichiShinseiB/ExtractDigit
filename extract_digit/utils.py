import queue
import tkinter as tk
from tkinter import filedialog
from typing import Generic, Sequence, cast, overload

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.backend_bases import MouseEvent, PickEvent
from matplotlib.lines import Line2D

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


class Quadraliteral(Generic[numT]):
    @overload
    def __init__(
        self, vertices: Sequence[Point[numT]] | None = None
    ) -> None: ...
    @overload
    def __init__(
        self, vertices: Sequence[tuple[numT, numT]] | None = None
    ) -> None: ...
    def __init__(
        self,
        vertices: Sequence[tuple[numT, numT]]
        | Sequence[Point[numT]]
        | None = None,
    ) -> None:
        self.points: queue.Queue[Point[numT]] = queue.Queue(4)
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
    def motion(event: MouseEvent) -> None:
        x = event.xdata
        y = event.ydata
        # print(x, y)

        if x is None or y is None:
            return
        ql.set_point((x, y))
        print(ql.x_points, ql.y_points)
        ln.set_data(ql.x_points, ql.y_points)
        plt.draw()

    fig = plt.figure()
    ql: Quadraliteral[float] = Quadraliteral()
    (ln,) = plt.plot([], [], "x")

    fig.canvas.mpl_connect("button_release_event", motion)  # type: ignore
    plt.show()


class InteractivePolygons:
    def __init__(
        self, x: npt.ArrayLike, y: npt.ArrayLike, max_length: int = 0
    ) -> None:
        self.xdata = x
        self.ydata = y
        self.max_length = len(self.xdata) if max_length is None else max_length  # type: ignore
        self._picked_ind = -1
        self.gco: Line2D | None = None

    @property
    def xdata_(self) -> npt.ArrayLike:
        return np.concat([self.xdata, [self.xdata[0]]])  # type: ignore

    @property
    def ydata_(self) -> npt.ArrayLike:
        return np.concat([self.ydata, [self.ydata[0]]])  # type: ignore

    @property
    def picked_ind(self) -> int:
        return self._picked_ind

    @picked_ind.setter
    def picked_ind(self, ind: int) -> None:
        self._picked_ind = ind

    def update_location(
        self, x: float, y: float, ind: int | None = None
    ) -> None:
        if ind is None:
            ind = self.picked_ind
        if ind > self.max_length - 1:
            ind = 0
        print("updating index: ", ind)
        self.xdata[ind] = x  # type: ignore
        self.ydata[ind] = y  # type: ignore

    def xy_points(self) -> tuple[tuple[float, float], ...]:
        return tuple(zip(self.xdata, self.ydata))  # type: ignore


def move_dots() -> None:
    def motion(event: MouseEvent) -> None:
        if xydata.gco is None:
            return
        x = event.xdata
        y = event.ydata
        if x is None or y is None:
            return
        xydata.update_location(x, y)
        xydata.gco.set_data(
            xydata.xdata_,
            xydata.ydata_,
        )
        plt.draw()

    def onpick(event: PickEvent) -> None:
        xydata.gco = cast(Line2D, event.artist)
        xydata.xdata = xydata.gco.get_xdata()[: xydata.max_length]  # type:ignore
        xydata.ydata = xydata.gco.get_ydata()[: xydata.max_length]  # type:ignore
        xydata.picked_ind = event.ind[0]  # type: ignore

    def release(_: MouseEvent) -> None:
        xydata.gco = None

    xydata = InteractivePolygons(
        np.random.rand(4), np.random.rand(4), max_length=4
    )
    fig, ax = plt.subplots()
    ax.plot(xydata.xdata_, xydata.ydata_, "o-", picker=15)

    fig.canvas.mpl_connect("pick_event", onpick)  # type: ignore
    fig.canvas.mpl_connect("motion_notify_event", motion)  # type: ignore
    fig.canvas.mpl_connect("button_release_event", release)  # type: ignore
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
    # gui_test()
    move_dots()
    # data = InteractivePolygons(np.random.rand(4), np.random.rand(4))
    # print(data._xdata_for_add)
    # print(data._ydata_for_add)
