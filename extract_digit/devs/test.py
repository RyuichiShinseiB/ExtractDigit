from math import sqrt
from typing import Sequence

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.lines import Line2D


class InteractivePlot:
    def __init__(
        self,
        points_x: Sequence[float] | None = None,
        points_y: Sequence[float] | None = None,
    ) -> None:
        self.image = cv2.imread(
            # "extract_digit/devs/sample_orc_digit.png", cv2.IMREAD_GRAYSCALE
            "data/src_images/IMG_20240708_132157_011.jpg",
            cv2.IMREAD_GRAYSCALE,
        )
        h, w = self.image.shape[:2]
        offset_h, offset_w = h // 3, w // 3

        self.fig, self.ax = plt.subplots()
        self.points: list[tuple[float, float]] = (
            list(zip(points_x, points_y))
            if points_x is not None and points_y is not None
            else [
                (offset_w, offset_h),
                (offset_w * 2, offset_h),
                (offset_w * 2, offset_h * 2),
                (offset_w, offset_h * 2),
            ]
        )
        self.line: Line2D | None = None
        self.selected_point: tuple[float, float] | None = None
        self.selected_point_index: int | None = None
        self.is_moving_all_points = False
        self.start_drag_x: float | None = None
        self.start_drag_y: float | None = None
        self.hit_test_radius = (w + h) / 2 / 100
        self.init_plot()
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)  # type: ignore
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)  # type: ignore
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)  # type: ignore
        self.ax.callbacks.connect("xlim_changed", self.on_axes_change)
        self.ax.callbacks.connect("ylim_changed", self.on_axes_change)

    def init_plot(self) -> None:
        self.ax.imshow(self.image)
        x, y = zip(*self.points)
        (self.line,) = self.ax.plot(
            # x, y, marker="o", linestyle="-", color="r", picker=100
            x,
            y,
            "r--",
            marker="o",
            # color="none",
            # markeredgecolor="red",
            # facecolor="None",
            # picker=100,
        )
        self.ax.plot([x[0], x[-1]], [y[0], y[-1]], "r--")

        # for line in self.ax.lines:
        # line.set_pickradius()
        # print(line.get_picker())
        #     line.set_pickradius()

    def update_plot(self) -> None:
        if self.line is None:
            return
        x, y = zip(*self.points)
        self.line.set_data(x, y)
        self.ax.lines[-1].set_data([x[0], x[-1]], [y[0], y[-1]])
        self.fig.canvas.draw()

    def on_click(self, event: MouseEvent) -> None:
        # print("in on_click: ", type(event))
        if event.inaxes != self.ax:
            return

        if event.xdata is None or event.ydata is None:
            return
        if event.button == 1:  # Left mouse button
            for i, point in enumerate(self.points):
                if self._check_inner_radius(point, (event.xdata, event.ydata)):
                    self.selected_point = point
                    self.selected_point_index = i
                    return

        elif event.dblclick == 1:
            # Check if clicking on the line
            if self.line is None:
                return
            self.is_moving_all_points = (
                self.line.contains(event)[0]
                or self.ax.lines[-1].contains(event)[0]
            )
            self.start_drag_x = event.xdata
            self.start_drag_y = event.ydata

    def on_release(self, _: MouseEvent) -> None:
        # print("in on_release: ", type(_))
        self.selected_point = None
        self.selected_point_index = None
        self.is_moving_all_points = False
        self.start_drag_x = None
        self.start_drag_y = None

    def on_motion(self, event: MouseEvent) -> None:
        if event.inaxes != self.ax:
            return
        if event.xdata is None or event.ydata is None:
            return

        # in points moving scope
        if (
            self.is_moving_all_points
            and self.start_drag_x is not None
            and self.start_drag_y is not None
        ):
            dx = event.xdata - self.start_drag_x
            dy = event.ydata - self.start_drag_y
            self.points = [(x + dx, y + dy) for x, y in self.points]
            self.start_drag_x = event.xdata
            self.start_drag_y = event.ydata
            self.update_plot()

        # in point moving scope
        if self.selected_point_index is not None:
            self.points[self.selected_point_index] = (event.xdata, event.ydata)
            self.update_plot()

    def on_axes_change(self, event_ax: Axes) -> None:
        xlim = event_ax.get_xlim()
        ylim = event_ax.get_ylim()
        width = xlim[1] - xlim[0]
        height = ylim[0] - ylim[1]
        self.hit_test_radius = (width + height) / 2 / 100
        # print(f"Zoomed xlim: {xlim}, ylim{ylim}")

    def _check_inner_radius(
        self, p_a: tuple[float, float], p_b: tuple[float, float]
    ) -> bool:
        radius = sqrt((p_a[0] - p_b[0]) ** 2 + (p_a[1] - p_b[1]) ** 2)
        return radius < self.hit_test_radius


plot = InteractivePlot()
plt.show()
points = np.array(plot.points, dtype=np.uint32)
print(points)
