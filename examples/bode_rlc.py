import numpy as np
import plotive as pv

L = 1e-4  # 100 µH
C = 1e-6  # 1 uF
TITLE = "RLC Circuit Bode Plot"


def rlc_freq_response(freq, R, L, C):
    """Returns the transfer function of a series RLC circuit."""
    pulse = 2 * np.pi * freq
    num = 1
    real = 1 - (pulse**2) * L * C
    imag = pulse * R * C

    mag = num / np.sqrt(real**2 + imag**2)
    ph = -np.arctan2(imag, real)

    return 20 * np.log10(mag), ph


if __name__ == "__main__":
    freq = np.logspace(2, 6, 500)  # 100 Hz to 1 MHz
    mags = ["mag1", "mag2", "mag3"]
    phs = ["ph1", "ph2", "ph3"]
    R_values = [1, 10, 100]  # Ohms

    data_source = {"freq": freq}
    mag_series = []
    ph_series = []

    for R, mag_col, ph_col in zip(R_values, mags, phs):
        mag, ph = rlc_freq_response(freq, R, L, C)
        data_source[mag_col] = mag
        data_source[ph_col] = ph
        mag_series.append(
            pv.series.Line(
                x="freq",
                y=mag_col,
                name=f"R = {R} Ω",
            )
        )
        ph_series.append(
            pv.series.Line(
                x="freq",
                y=ph_col,
            )
        )

    fig = pv.Figure(
        title=TITLE,
        plots=[
            pv.Plot(
                series=mag_series,
                x_axis=pv.Axis(
                    scale="Frequency (Hz)", ticks="auto", minor_ticks="auto"
                ),  # references the x-axis scale of the second plot
                y_axis=pv.Axis(title="Magnitude (dB)", ticks="auto", grid="auto"),
            ),
            pv.Plot(
                series=ph_series,
                x_axis=pv.Axis(
                    title="Frequency (Hz)",
                    scale="log",
                    ticks="auto",
                    minor_ticks="auto",
                ),
                y_axis=pv.Axis(title="Phase (radians)", ticks="pi", grid="auto"),
            ),
        ],
        legend="right",
    )
    fig.show(data_source=data_source, style="macchiato")
