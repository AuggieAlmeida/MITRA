def color(name):
    try:
        if name == "background":
            return "#eef7fc"
        elif name == "background2":
            return "#5fadff"
        elif name == "background-bar":
            return "#5daafd"
    except KeyError:
        return "Not Found"
