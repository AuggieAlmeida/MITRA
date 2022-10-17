def color(name):
    try:
        if name == "background":
            return "#eef7fc"
        elif name == "background-bar":
            return "#56b0e6"
    except KeyError:
        return "Not Found"
