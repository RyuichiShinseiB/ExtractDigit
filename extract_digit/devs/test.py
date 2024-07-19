from math import sqrt
from typing import Sequence

import cv2
import matplotlib.pyplot as plt
import matplotlib.widgets as wg
import numpy as np
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.lines import Line2D

from extract_digit.processing import crop_transform_show_digits


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

        self.fig = plt.figure(figsize=(14, 7))
        # left side view (original image)
        self.ax_main = self.fig.add_subplot(1, 2, 1)
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
        self.selected_point_index: int | None = None
        self.is_moving_all_points = False
        self.start_drag_x: float | None = None
        self.start_drag_y: float | None = None
        self.hit_test_radius = (w + h) / 2 / 100

        # right side view (processed image)
        self.ax_prcd = self.fig.add_subplot(1, 2, 2)
        self.processed_img: cv2.typing.MatLike = np.full(
            (200, 300), 255, np.uint8
        )

        # button
        self.ax_run = self.fig.add_axes((0.7, 0.05, 0.1, 0.075))
        self.btn_run = wg.Button(
            self.ax_run,
            "crop and rectify",
            color="#7a776c",
            hovercolor="#38b48b",
        )

        self.init_plot()

        self.fig.canvas.mpl_connect("button_press_event", self.on_click)  # type: ignore
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)  # type: ignore
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)  # type: ignore
        self.ax_main.callbacks.connect("xlim_changed", self.on_axes_change)
        self.ax_main.callbacks.connect("ylim_changed", self.on_axes_change)

        self.btn_run.on_clicked(self.on_btn_clicked)  # type: ignore

    def init_plot(self) -> None:
        self.ax_main.imshow(self.image, "gray")
        x, y = zip(*self.points)
        (self.line,) = self.ax_main.plot(
            x,
            y,
            "r--",
            marker="o",
        )
        self.ax_main.plot([x[0], x[-1]], [y[0], y[-1]], "r--")

        self.ax_prcd.imshow(np.zeros((200, 300), np.uint8), "gray")

    def update_plot(self) -> None:
        if self.line is None:
            return
        x, y = zip(*self.points)
        self.line.set_data(x, y)
        self.ax_main.lines[-1].set_data([x[0], x[-1]], [y[0], y[-1]])
        self.fig.canvas.draw()

    def on_click(self, event: MouseEvent) -> None:
        # print("in on_click: ", type(event))
        if event.inaxes != self.ax_main:
            return

        if event.xdata is None or event.ydata is None:
            return
        if event.button == 1:  # Left mouse button
            if event.dblclick:
                # Check if clicking on the line
                if self.line is None:
                    return
                self.is_moving_all_points = (
                    self.line.contains(event)[0]
                    or self.ax_main.lines[-1].contains(event)[0]
                )
                self.start_drag_x = event.xdata
                self.start_drag_y = event.ydata

            else:
                for i, point in enumerate(self.points):
                    if self._check_inner_radius(
                        point, (event.xdata, event.ydata)
                    ):
                        self.selected_point_index = i
                        return

    def on_release(self, _: MouseEvent) -> None:
        # print("in on_release: ", type(_))
        self.selected_point_index = None
        self.is_moving_all_points = False
        self.start_drag_x = None
        self.start_drag_y = None

    def on_motion(self, event: MouseEvent) -> None:
        if event.inaxes != self.ax_main:
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

    def on_btn_clicked(self, _: MouseEvent) -> None:
        # print(type(_))
        self.processed_img = crop_transform_show_digits(
            self.image,
            [(int(point[0]), int(point[1])) for point in self.points],
            (200, 300),
        )
        self.ax_prcd.imshow(self.processed_img, "gray")
        self.fig.canvas.draw()

    def _check_inner_radius(
        self, p_a: tuple[float, float], p_b: tuple[float, float]
    ) -> bool:
        radius = sqrt((p_a[0] - p_b[0]) ** 2 + (p_a[1] - p_b[1]) ** 2)
        return radius < self.hit_test_radius


plot = InteractivePlot()
plt.show()
points = np.array(plot.points, dtype=np.uint32)
print(points)
