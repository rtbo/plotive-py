import plotive as pv


def download_font_from_dafont(font_name):
    import requests
    import zipfile
    from io import BytesIO

    r = requests.get(f"https://dl.dafont.com/dl/?f={font_name}")
    r.raise_for_status()

    with zipfile.ZipFile(BytesIO(r.content)) as z:
        for name in z.namelist():
            if name.lower().endswith((".ttf", ".otf")):
                return z.read(name)

    raise RuntimeError("No font file found in the downloaded zip archive.")


font = download_font_from_dafont("modern_tokyo")

fig = pv.Figure(
    # title in array or tuple triggers rich text parsing
    title=("[font=Modern Tokyo;size=36]Custom font[/font;size] example",),
    plot=pv.Plot(
        series=pv.series.Line(
            x=[1, 2, 3, 4, 5],
            y=[1, 4, 9, 16, 25],
        ),
    ),
)

fig.show(params=pv.Params(fonts=font))
