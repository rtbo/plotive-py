
def _parse_args():
    import sys

    args = {
        "style": None,
        "png": False,
        "svg": False,
        "show": False,
    }

    BUILTIN_STYLES = [
        "black-white",
        "monochrome",
        "black",
        "bw",
        "light",
        "standard",
        "dark",
        "okabe-ito",
        "okabe",
        "tol-bright",
        "tol",
        "catppuccin-mocha",
        "mocha",
        "catppuccin-macchiato",
        "macchiato",
        "catppuccin-frappe",
        "frappe",
        "catppuccin-latte",
        "latte",
        "dracula",
        "alucard",
    ]

    for arg in sys.argv[1:]:
        if arg == "png":
            args["png"] = True
        elif arg.startswith("png="):
            args["png"] = arg[4:]
        elif arg == "svg":
            args["svg"] = True
        elif arg.startswith("svg="):
            args["svg"] = arg[4:]
        elif arg == "show":
            args["show"] = True
        elif arg in BUILTIN_STYLES:
            args["style"] =  arg
        else:
            raise ValueError(f"Unknown argument: {arg}")

    if not args["png"] and not args["svg"]:
        args["show"] = True

    return args



def process_figure(fig, data_src, default_name):
    args = _parse_args()

    if args["png"]:
        filename = default_name if args["png"] == True else args["png"]
        if not filename.endswith(".png"):
            filename += ".png"
        fig.save_png(filename, data_source=data_src, style=args["style"])

    if args["svg"]:
        filename = default_name if args["svg"] == True else args["svg"]
        if not filename.endswith(".svg"):
            filename += ".svg"
        fig.save_svg(filename, data_source=data_src, style=args["style"])

    if args["show"]:
        fig.show(data_source=data_src, style=args["style"])

