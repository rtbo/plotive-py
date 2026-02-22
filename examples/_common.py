
def process_figure(fig, data_src):
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Plotive examples")
    parser.add_argument(
        "--style",
        type=str,
        default=None,
        help="Override a style to use for the plot.",
    )
    # positional argument for output file
    parser.add_argument(
        "output_file",
        nargs="?",
        default=None,
        help="The file to save the plot to (default: show the plot).",
    )
    args = parser.parse_args()

    if args.output_file:
        if args.output_file.endswith(".png"):
            fig.save_png(args.output_file, data_source=data_src, style=args.style)
        elif args.output_file.endswith(".svg"):
            fig.save_svg(args.output_file, data_source=data_src, style=args.style)
        else:
            print("Unsupported file format. Please use .png or .svg.", file=sys.stderr)
    else:
        fig.show(data_source=data_src, style=args.style)
