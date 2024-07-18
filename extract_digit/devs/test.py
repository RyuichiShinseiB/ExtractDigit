from typing import Sequence

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
from matplotlib.lines import Line2D


class InteractivePlot:
    def __init__(
        self,
        points_x: Sequence[float] = (-1, 1, 1, -1),
        points_y: Sequence[float] = (1, 1, -1, -1),
    ) -> None:
        self.fig, self.ax = plt.subplots()
        self.points: list[tuple[float, float]] = list(zip(points_x, points_y))
        self.line: Line2D | None = None
        self.selected_point: tuple[float, float] | None = None
        self.selected_point_index: int | None = None
        self.is_moving_all_points = False
        self.start_drag_x: float | None = None
        self.start_drag_y: float | None = None
        self.init_plot()
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)  # type: ignore
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)  # type: ignore
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)  # type: ignore

    def init_plot(self) -> None:
        x, y = zip(*self.points)
        (self.line,) = self.ax.plot(x, y, marker="o", linestyle="-")
        self.ax.plot([x[0], x[-1]], [y[0], y[-1]], "r--")

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

        if event.button == 1:  # Left mouse button
            if event.xdata is None or event.ydata is None:
                return
            for i, (x, y) in enumerate(self.points):
                if (x - event.xdata) ** 2 + (y - event.ydata) ** 2 < 0.1:
                    self.selected_point = (x, y)
                    self.selected_point_index = i
                    return

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
        # print("in on_motion: ", type(event))
        # print(f"{self.is_moving_all_points=}")
        print(
            f"""
            {self.selected_point = }
            {event.xdata = }
            {event.ydata = }
            {self.start_drag_x = }
            {self.start_drag_y = }
            """
        )
        if event.inaxes != self.ax:
            return

        if (
            self.is_moving_all_points
            and self.start_drag_x is not None
            and self.start_drag_y is not None
            and event.xdata is not None
            and event.ydata is not None
        ):
            print("in points moving scope")
            dx = event.xdata - self.start_drag_x
            dy = event.ydata - self.start_drag_y
            self.points = [(x + dx, y + dy) for x, y in self.points]
            self.start_drag_x = event.xdata
            self.start_drag_y = event.ydata
            self.update_plot()

        if self.selected_point_index is not None:
            print("in point moving scope")
            self.points[self.selected_point_index] = (event.xdata, event.ydata)
            self.update_plot()


plot = InteractivePlot()
plt.show()
