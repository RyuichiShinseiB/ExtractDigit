import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


class InteractivePlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.points = [(1, 2), (2, 3), (3, 1), (4, 4), (5, 2)]
        self.line = None
        self.selected_point = None
        self.selected_point_index = None
        self.is_moving_all_points = False
        self.start_drag_x = None
        self.start_drag_y = None
        self.init_plot()
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def init_plot(self):
        x, y = zip(*self.points)
        (self.line,) = self.ax.plot(x, y, marker="o", linestyle="-")
        self.ax.plot([x[0], x[-1]], [y[0], y[-1]], "r--")

    def update_plot(self):
        x, y = zip(*self.points)
        self.line.set_data(x, y)
        self.ax.lines[-1].set_data([x[0], x[-1]], [y[0], y[-1]])
        self.fig.canvas.draw()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return

        if event.button == 1:  # Left mouse button
            for i, (x, y) in enumerate(self.points):
                if (x - event.xdata) ** 2 + (y - event.ydata) ** 2 < 0.1:
                    self.selected_point = (x, y)
                    self.selected_point_index = i
                    return

            # Check if clicking on the line
            if self.line.contains(event)[0]:
                self.is_moving_all_points = True
                self.start_drag_x = event.xdata
                self.start_drag_y = event.ydata

    def on_release(self, event):
        self.selected_point = None
        self.selected_point_index = None
        self.is_moving_all_points = False
        self.start_drag_x = None
        self.start_drag_y = None

    def on_motion(self, event):
        if event.inaxes != self.ax:
            return

        if self.selected_point is not None:
            self.points[self.selected_point_index] = (event.xdata, event.ydata)
            self.update_plot()

        if self.is_moving_all_points:
            dx = event.xdata - self.start_drag_x
            dy = event.ydata - self.start_drag_y
            self.points = [(x + dx, y + dy) for x, y in self.points]
            self.start_drag_x = event.xdata
            self.start_drag_y = event.ydata
            self.update_plot()


plot = InteractivePlot()
plt.show()
