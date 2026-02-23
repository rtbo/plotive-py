.. plotive-py documentation master file, created by
   sphinx-quickstart on Sun Feb 22 20:26:47 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

plotive-py documentation
========================

.. note::

   `plotive-py` are the Python bindings to `plotive`_, a plotting library written in Rust.

   .. _plotive: https://github.com/rtbo/plotive


`plotive` is a data plotting library. It stands for *Declarative plotting*.
The basic concept is that the design of figures is separated from the data
and from the style you apply to the figure.

Supported figure types
----------------------

* XY line plots

* Scatter plots

* Histograms

* Bar plots


Modular architecture
--------------------

- **Declarative design**

   - Design of figure is entirely declarative and decoupled from data and drawing primitives.
   - Sensible defaults.
   - Figure units are decorrelated from pixel size for easy scaling

- **Data sources**

   - Flexible, column-friendly data source system
   - Compatible with `pandas`, `numpy` arrays, lists...

- **Rendering surfaces**

   - Rendering backend is decoupled from drawing. You can render onto:
   - pixel grids, PNG
   - SVG
   - GUI window


Automatic Layout
----------------

- All the layout is done consistently and automatically.

  You can add multiple axes, multiple plots etc.
  Everything will be laid-out consistently, leaving enough space for axis ticks labels, legends etc.
  Your code never need to calculate size of anything.

Advanced typography
-------------------

- Automatic font look-up and text shaping
- Rich text
- Automatic right to left layout using unicode-bidirectional algorithm
- vertical layout

Themes
------

- Change the theme of your figure with a single line of code.
- Buitin themes included


Annotations
-----------

- Annotate your figures, with labels, infinite lines, markers etc.
- Annotations are placed using data space coordinates

Code example for a simple figure
--------------------------------

.. code-block:: python

    import plotive as pv
    import numpy as np

    # We first create the figure design
    # A figure must have at least one plot

    fig = pv.Figure(
        title="Sine Wave",
        # A figure must have at least one plot
        # Multiple plots can be provided with `plots` list property
        plot=pv.Plot(
            series=[
                pv.series.Line(
                    # Data is referred to by column name in the data source
                    # They can also be inline in the figure object
                    x="x",
                    y="y",
                    name="sin(x)",
                )
            ],
            # By default, axis have no tick, no title.
            # Here is how to customize them.
            x_axis=pv.Axis(title="x", ticks="pimultiple", grid="auto"),
            y_axis=pv.Axis(title="sin(x)", ticks="auto", grid="auto"),
            # Legend can be at plot level or figure level.
            # They automatically gather all series that have a name property
            legend="in-top-right",
        ),
    )

    # Now we define the data source
    x = np.linspace(0, 2 * np.pi, 500)
    y = np.sin(x)
    data_src = {"x": x, "y": y}

    # and we can finally show the figure.
    fig.show(data_source=data_src)

The following window should show

.. image:: img/index_sine.png

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:

   gallery

   tuto

   api_ref
