import plotive as plt

def get_n_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = all(candidate % p != 0 for p in primes)
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes


fig = plt.Figure(
    title="Line Plot Example",
    legend="bottom",
    plot=plt.Plot(
        series=[
            plt.series.Line(
                x = list(range(1, 1001)),
                y = get_n_primes(1000),
                name = "1000 Prime Numbers"
            )
        ],
        x_axis = plt.Axis(title="Index", ticks=plt.Ticks()),
        y_axis = plt.Axis(title="Prime Numbers", ticks=plt.Ticks()),
    )
)

fig.show()

# figure = plt.Figure(
#     title="Subplots",
#     space=10,
#     subplots=(2, 1),
#     plots=[
#         plt.Plot(
#             subplot=(1, 1),
#             x_axis=["shared(x)", "Grid"],
#             y_axis=["y1", "Ticks"],
#             series=plt.Series(type="Line", x_data="x1", y_data="y1"),
#         ),
#         plt.Plot(
#             subplot=(2, 1),
#             x_axis=["x", "PiMultipleTicks", "Grid", {"id": "x-axis"}],
#             y_axis=["y2", "Ticks"],
#             series=plt.Series(type="Line", x_data="x2", y_data="y2"),
#         ),
#     ],
# )
