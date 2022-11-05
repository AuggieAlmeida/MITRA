from tkinter import Frame, Label, Canvas
from lib.colours import color


class GradientFrame(Canvas):
    def __init__(self, parent, color1=color("background"), color2="#e0eaef", **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._drawgradient)

    def _drawgradient(self, event = None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1, g1, b1) = self.winfo_rgb(self._color1)
        (r2, g2, b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1)/limit
        g_ratio = float(g1-g2)/limit
        b_ratio = float(b2-b1)/limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(r1 + (g_ratio * i))
            nb = int(r1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
            self.create_line(i, 0, i, height, tags=("gradient"), fill=color)
        self.lower("gradient")


def init_bar(master):
    bar = GradientFrame(master, width=980, height=60)

    for child in bar.winfo_children():
        widget_class = child.__class__.__name__
        if widget_class == "Label":
            child.grid_configure(pady=0, padx=15, sticky="W")
        elif widget_class == "Frame":
            child.grid_configure(pady=0, padx=0, sticky="NSWE")
        else:
            child.grid_configure(padx=5, pady=3, sticky='N')