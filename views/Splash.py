#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from tkinter import Canvas, Label, Tk, Image

from PIL import Image, ImageTk

import lib.global_variable as glv
from lib.functions import set_window_center


class Splash(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.w = 300
        self.resizable(False, False)
        self.h = 300
        set_window_center(self, self.w, self.h)
        self.title("MITRA")
        self.splash()

    def splash(self):
        image_file = os.path.join(
            glv.get_variable("APP_PATH"),
            glv.get_variable("DATA_DIR"),
            "assets",
            "LOGO.png",
        )

        canvas = Canvas(self, width=self.w, height=250, bg="white")
        if os.path.exists(image_file):
            img = Image.open(image_file)
            image = ImageTk.PhotoImage(img)
            canvas.create_image(self.w / 2, 250 / 2, image=image)

        canvas.pack(fill="both")
        Label(self, text="Carregando", bg="green", fg="#fff", height=2).pack(
            fill="both", side="bottom"
        )

        self.after(1000, self.destroy)
        self.mainloop()
