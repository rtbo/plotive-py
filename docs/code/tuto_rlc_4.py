import plotive as pv
import numpy as np

R = 1     # 1 ohm
L = 1e-4  # 100 µH
C = 1e-6  # 1 uF


# This is not an electronic class, so I won't detail too much
# the calculation of the transfer function.
# Just know that freq is a numpy array of frequencies in hz, and that
# we return a tuple of arrays (gain and phase) of the same length.
def rlc_freq_response(freq, R, L, C):
    """
    Returns the transfer function of a series RLC circuit.
    Transfer function: H(jw) = 1 / (1 - w²LC + jwRC)
    """

    pulse = 2 * np.pi * freq
    num = 1
    den_r = 1 - (pulse**2) * L * C
    den_i = pulse * R * C

    mag = num / np.sqrt(den_r**2 + den_i**2)
    ph = -np.arctan2(den_i, den_r)

    # convert gain to dB, keep phase in radians
    return 20 * np.log10(mag), ph


if __name__ == "__main__":
    # Here is our numpy array of frequencies, from 100 Hz to 1 MHz, 200 points per decade
    freq = np.logspace(2, 6, 801)
    # Compute the gain and phase for our RLC circuit
    mag, ph = rlc_freq_response(freq, R, L, C)

    title = "Bode diagram of a series RLC circuit\n" + \
            "[size=18;italic;font=serif]R = 1 Ω / L = 0.1 mH / C = 1 µF[/size;italic;font]"

    # compute cutoff frequency of the filter
    cutoff_freq = 1 / (2 * np.pi * np.sqrt(L * C))
    # compute slope two decades after cutoff frequency for better accuracy
    slope = rlc_freq_response(cutoff_freq * 100, R, L, C)[0] / 2

    fig = pv.Figure(
        title=title,
        # Multiple plots are specified with the "plots" argument, which takes a list of plot definitions.
        plots=[
            pv.Plot(
                # `subplot` specifies the position of the plot in a grid layout in (row, column) tuple.
                subplot=(1, 1),
                series=[
                    pv.series.Line(x="freq", y="mag"),
                ],
                x_axis=pv.Axis(
                    # For the scale, we reference the scale of the phase plot.
                    # This is how we share axes scales on multiple plots in the same figure.
                    scale="Frequency (Hz)",
                    ticks="auto",
                    minor_ticks="auto",
                ),
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
                subplot=(2, 1),
                series=[
                    pv.series.Line(x="freq", y="ph"),
                ],
                x_axis=pv.Axis(
                    title="Frequency (Hz)",
                    scale="log",
                    ticks="auto",
                    minor_ticks="auto",
                ),
                y_axis=pv.Axis(title="Phase (rad)", ticks="pimultiple", grid="auto"),
            )
        ],
    )

    data_src = {
        "freq": freq,
        "mag": mag,
        "ph": ph,
    }

    # Save the figure as a PNG file.
    # You can use `fig.show()` to display it in an interactive window instead,
    # or `fig.save_svg()` to save it as an SVG file.
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else "bode.png"
    fig.save_png(filename, data_source=data_src, style="catppuccin-macchiato")
