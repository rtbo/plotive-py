import plotive as pv
import numpy as np

R = 1     # 1 ohm
L = 1e-4  # 100 µH
C = 1e-6  # 1 uF


# This is not an electronic class, so I won't detail too much
# the calculation of the transfer function.
# Just know that freq is a numpy array of frequencies in Hz, and that
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

    # convert gain to dB, phase to degrees
    return 20 * np.log10(mag), ph * 180 / np.pi


if __name__ == "__main__":
    # Here is our numpy array of frequencies, from 100 Hz to 1 MHz, 200 points per decade
    freq = np.logspace(2, 6, 801)
    # Compute the gain and phase for our RLC circuit
    mag, ph = rlc_freq_response(freq, R, L, C)

    fig = pv.Figure(
        title="A Bode plot",
        plot = pv.Plot(
            # We create two series on the same plot, one for gain and one for phase.
            # To keep things simple, the data is inlined in the series definition, and we don't use a data source.
            series=[
                pv.series.Line(x=freq, y=mag, name="Magnitude"),
                pv.series.Line(x=freq, y=ph, name="Phase"),
            ],
            # Customize the X-axis: logarithmic scale, automatic ticks with minor ticks, and a title.
            x_axis=pv.Axis(
                title="Frequency (Hz)",
                scale="log",
                ticks="auto",
                minor_ticks="auto",
            ),
            y_axis=pv.Axis(title="Magnitude (dB) / Phase (deg)", ticks="auto", grid="auto"),
        ),
        # It is a good practice to include a legend when you have multiple series.
        legend="bottom",
    )

    # Save the figure as a PNG file.
    # You can use `fig.show()` to display it in an interactive window instead,
    # or `fig.save_svg()` to save it as an SVG file.
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else "bode.png"
    fig.save_png(filename)
