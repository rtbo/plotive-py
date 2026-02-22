import numpy as np
import plotive as pv

L = 1e-4  # 100 µH
C = 1e-6  # 1 uF
TITLE = "Bode diagram of RLC circuit\n" + \
        "[size=18;italic;font=serif]L = 0.1 mH / C = 1 µF[/size;italic;font]"


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

    data_src = {"freq": freq}
    mag_series = []
    ph_series = []

    for R, mag_col, ph_col in zip(R_values, mags, phs):
        mag, ph = rlc_freq_response(freq, R, L, C)
        data_src[mag_col] = mag
        data_src[ph_col] = ph
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

    cutoff_freq = 1 / (2 * np.pi * np.sqrt(L * C))
    # compute slope two decades after cutoff frequency for better accuracy
    slope = rlc_freq_response(cutoff_freq * 100, R_values[0], L, C)[0] / 2

    fig = pv.Figure(
        title=TITLE,
        plots=[
            pv.Plot(
                series=mag_series,
                x_axis=pv.Axis(
                    scale="Frequency (Hz)", ticks="auto", minor_ticks="auto"
                ),  # references the x-axis scale of the second plot
                y_axis=pv.Axis(title="Magnitude (dB)", ticks="auto", grid="auto"),
                annotations=[
                    pv.annot.Line(
                        vertical=cutoff_freq,
                        stroke=pv.style.Stroke(color="foreground", pattern=[5, 5]),
                    ),
                    pv.annot.Label(
                        xy=(cutoff_freq, -60),
                        text=f"{cutoff_freq/1000:.2f} kHz",
                        anchor="bottom-left",
                        angle=90,
                    ),
                    pv.annot.Line(
                        two_points=((cutoff_freq, 0), (cutoff_freq * 10, slope)),
                        stroke=pv.style.Stroke(color="foreground", pattern=[5, 5]),
                    ),
                    pv.annot.Label(
                        xy=(cutoff_freq * 10, slope),
                        text=f"{slope:.1f} dB/decade",
                        anchor="bottom-left",
                    ),
                ],
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

    import _common
    _common.process_figure(fig, data_src)
