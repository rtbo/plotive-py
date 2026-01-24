import plotive as plt
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

y = list(range(1, 1001))
x = get_n_primes(1000)

data_src = {
    "x": x,
    "y": y,
}

fig = plt.Figure(
    title="Line Plot Example",
    legend="bottom",
    plot=plt.Plot(
        series=[
            plt.series.Line(
                x = "x",
                y = "y",
                name = "1000 Prime Numbers",
                interpolation = "step",
            )
        ],
        x_axis = plt.Axis(title="Index", ticks=plt.Ticks()),
        y_axis = plt.Axis(title="Prime Numbers", ticks=plt.Ticks()),
    )
)

fig.show(data_source=data_src, style="mocha")
