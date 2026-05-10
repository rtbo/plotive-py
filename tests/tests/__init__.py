import plotive as pv
from PIL import Image as pil
import os
import random


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


"""random.Random instance with a fixed seed for deterministic behavior."""


class NotRandom(random.Random):
    def __init__(self, seed: int = 1234567890987654321):
        super().__init__(seed)

    def make_col_uniform(
        self, len: int, min: float = 0.0, max: float = 1.0
    ) -> list[float]:
        """Generate a column of random values."""
        return [self.uniform(min, max) for _ in range(len)]

    def make_col_normal(
        self, len: int, mu: float = 0.0, sigma: float = 1.0
    ) -> list[float]:
        return [self.normalvariate(mu, sigma) for _ in range(len)]


_BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def _ref_file_path(ref_name: str) -> str:
    return os.path.join(_BASE_DIR, "refs", f"{ref_name}.png")


def _failed_file_path(ref_name: str) -> str:
    return os.path.join(_BASE_DIR, "failed", f"{ref_name}.png")


def _diff_file_path(ref_name: str) -> str:
    return os.path.join(_BASE_DIR, "failed", f"{ref_name}-diff.png")


def _render_fig_to_img(fig: pv.Figure, style) -> pil.Image:
    fig_pxl = fig.render_pxl(style=style)
    print(
        f"Rendered figure to pixel data: {fig_pxl.width}x{fig_pxl.height}, {len(fig_pxl.data)} bytes"
    )
    return pil.frombuffer(
        "RGBA", (fig_pxl.width, fig_pxl.height), fig_pxl.data, "raw", "RGBa", 0, 1
    )


def assert_fig_eq_ref(fig: pv.Figure, ref_name: str, style="bw"):
    from pixelmatch.contrib.PIL import pixelmatch

    ref_path = _ref_file_path(ref_name)
    failed_path = _failed_file_path(ref_name)
    diff_path = _diff_file_path(ref_name)

    mismatch = 0
    err = None

    try:
        fig_img = _render_fig_to_img(fig, style)
        ref_img = pil.open(ref_path)

        diff_img = pil.new("RGBA", fig_img.size)
        mismatch = pixelmatch(fig_img, ref_img, diff_img, includeAA=True)
    except FileNotFoundError as e:
        err = e

    if mismatch > 0:
        print(f"Figure ref assertion failed: '{ref_name}'")
        print(f"  Number of different pixels: {mismatch}")
        print()
        os.makedirs(os.path.dirname(failed_path), exist_ok=True)
        os.makedirs(os.path.dirname(diff_path), exist_ok=True)
        fig_img.save(failed_path)
        diff_img.save(diff_path)
        print(f"    Tested figure: {failed_path}")
        print(f"       Ref figure: {ref_path}")
        print(f"             Diff: {diff_path}")
        assert False, f"Figure does not match reference: '{ref_name}'"
    elif err is not None:
        print(f"Figure ref assertion failed: '{ref_name}'")
        print(f"  Error comparing figure to reference: {err}")
        os.makedirs(os.path.dirname(failed_path), exist_ok=True)
        fig_img.save(failed_path)
        print(f"    Tested figure: {failed_path}")
        assert False, f"Missing figure reference: '{ref_name}'"
    else:
        if os.path.exists(failed_path):
            os.remove(failed_path)
        if os.path.exists(diff_path):
            os.remove(diff_path)
