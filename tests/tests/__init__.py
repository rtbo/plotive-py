import plotive as pv
from PIL import Image as pil
import os


def fig_small(plot: pv.Plot, **fig_kwargs) -> pv.Figure:
    # Helper function to create a small figure for testing
    return pv.Figure(plot=plot, size=(400, 300), **fig_kwargs)

def fig_mid(plot: pv.Plot, **fig_kwargs) -> pv.Figure:
    # Helper function to create a medium figure for testing
    return pv.Figure(plot=plot, size=(600, 450), **fig_kwargs)

def fig_high(plot: pv.Plot, **fig_kwargs) -> pv.Figure:
    return pv.Figure(plot=plot, size=(400, 500), **fig_kwargs)

def fig_wide(plot: pv.Plot, **fig_kwargs) -> pv.Figure:
    return pv.Figure(plot=plot, size=(600, 300), **fig_kwargs)

_BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def _ref_file_path(ref_name: str) -> str:
    return os.path.join(_BASE_DIR, "refs", f"{ref_name}.png")

def _failed_file_path(ref_name: str) -> str:
    return os.path.join(_BASE_DIR, "failed", f"{ref_name}.png")

def _diff_file_path(ref_name: str) -> str:
    return os.path.join(_BASE_DIR, "failed", f"{ref_name}-diff.png")


def _render_fig_to_img(fig: pv.Figure, style) -> pil.Image:
    fig_pxl = fig.render_pxl(style=style)
    print(f"Rendered figure to pixel data: {fig_pxl.width}x{fig_pxl.height}, {len(fig_pxl.data)} bytes")
    return pil.frombuffer(
        "RGBA", (fig_pxl.width, fig_pxl.height), fig_pxl.data, "raw", "RGBa", 0, 1
    )

def assert_fig_eq_ref(fig: pv.Figure, ref_name: str, style="bw"):
    from pixelmatch.contrib.PIL import pixelmatch

    ref_path = _ref_file_path(ref_name)
    failed_path = _failed_file_path(ref_name)
    diff_path = _diff_file_path(ref_name)

    fig_img = _render_fig_to_img(fig, style)
    ref_img = pil.open(ref_path)

    diff_img = pil.new("RGBA", fig_img.size)
    try:
        mismatch = pixelmatch(fig_img, ref_img, diff_img, includeAA=True)
        err = None
    except ValueError as e:
        mismatch = 0
        err = e

    if mismatch > 0 or err is not None:
        print(f"Figure ref assertion failed: '{ref_name}'")
        if err is not None:
            print(f"  Error comparing figure to reference: {err}")
        else:
            print(f"  Number of different pixels: {mismatch}")
        print()
        os.makedirs(os.path.dirname(failed_path), exist_ok=True)
        os.makedirs(os.path.dirname(diff_path), exist_ok=True)
        fig_img.save(failed_path)
        diff_img.save(diff_path)
        print(f"    Actual figure: {failed_path}")
        print(f"       Ref figure: {ref_path}")
        print(f"             Diff: {diff_path}")
        assert False, f"Figure does not match reference: '{ref_name}'"
    else:
        if os.path.exists(failed_path):
            os.remove(failed_path)
        if os.path.exists(diff_path):
            os.remove(diff_path)

