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

    fig = pv.Figure(
        title="A Bode plot",
        plot = pv.Plot(
            # We use two Y-axes, we specify that the phase series should use the axis with title "Phase (rad)".
            # (We could also use the axis index or an arbitrary string id.)
            series=[
                pv.series.Line(x=freq, y=mag, name="Magnitude"),
                pv.series.Line(x=freq, y=ph, name="Phase", y_axis="Phase (rad)"),
            ],
            x_axis=pv.Axis(
                title="Frequency (Hz)",
                scale="log",
                ticks="auto",
                minor_ticks="auto",
            ),
            # As gain and phase have different units and scales, we use two Y-axes.
            # For clarity, we only put ticks and grid on the left Y-axis, and a title on each.
            # The phase axis goes on the right side
            y_axes=[ # note that we use "axEs" (plural) to specify multiple axes
                pv.Axis(title="Magnitude (dB)", ticks="auto", grid="auto"),
                # Radians are best scaled with ticks at multiples of pi, which we can specify with "pimultiple".
                pv.Axis(title="Phase (rad)", ticks="pimultiple", side="right", grid="auto"),
            ],
        ),
        legend="bottom",
    )

    # Save the figure as a PNG file.
    # You can use `fig.show()` to display it in an interactive window instead,
    # or `fig.save_svg()` to save it as an SVG file.
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else "bode.png"
    fig.save_png(filename)
