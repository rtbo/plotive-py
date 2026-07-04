import plotive as pv
import numpy as np
import pandas as pd


def get_n_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = all(candidate % p != 0 for p in primes)
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes


if __name__ == "__main__":
    primes = get_n_primes(1000)
    indices = list(range(1, 1001))

    data_src = {
        "primes": primes,
        "indices": indices,
    }

    fig = pv.Figure(
        title="Line Plot Example",
        plot=pv.Plot(
            series=[
                pv.series.Line(
                    x="primes",
                    y="indices",
                    name="1000 Prime Numbers",
                    interpolation="step",
                )
            ],
            x_axis=pv.Axis(title="Prime Numbers", ticks=pv.Ticks()),
            y_axis=pv.Axis(title="Indices", ticks=pv.Ticks()),
            legend="in-top-left",
        ),
    )

    import _common

    _common.process_figure(fig, data_src)
