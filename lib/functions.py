def set_window_center(window, width, height):
    w_s = window.winfo_screenwidth()
    h_s = window.winfo_screenheight()
    x_co = (w_s - width) / 2
    y_co = (h_s - height) / 2 - 50
    window.geometry("%dx%d+%d+%d" % (width, height, x_co, y_co))
    window.maxsize(width, height)

def set_window_sided(window, width, height):
    w_s = window.winfo_screenwidth()
    h_s = window.winfo_screenheight()
    x_co = (w_s - width) / 2 - 1
    y_co = (h_s - height) / 3 + 1
    window.geometry("%dx%d+%d+%d" % (width, height, x_co, y_co))
    window.minsize(width, height)


def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()
