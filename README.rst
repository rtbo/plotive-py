##########
plotive-py
##########

Plotive is a data plotting library, versatile and simple to use.
The main concept is to enable purely declarative construction of figures, abstracted from the data and from rendering surfaces.

Latest documentation is available on `Read The Docs`_.

.. _Read The Docs: https://plotive-py.readthedocs.io/en/latest/

`plotive-py` are the python bindings to the Rust `plotive`_ library.

.. _plotive: https://github.com/rtbo/plotive

Here is a simple yet complete example:

.. code-block:: python

    import plotive as pv
    import numpy as np

    fig = pv.Figure(
        title="Sine Wave",
        plot=pv.Plot(
            series=[
                pv.series.Line(
                    x="x",
                    y="y",
                    name="sin(x)",
                )
            ],
            x_axis=pv.Axis(title="x", ticks="pimultiple", grid="auto"),
            y_axis=pv.Axis(title="sin(x)", ticks="auto", grid="auto"),
            legend="in-top-right",
        ),
    )

    x = np.linspace(0, 2 * np.pi, 500)
    y = np.sin(x)

    fig.show(data_source={"x": x, "y": y})

This example shows the following interactive window:

.. image:: docs/img/index_sine.png


Supported figure types
----------------------

* XY line plots

* Scatter plots

* Histograms

* Bar plots


Modular architecture
--------------------

* **Declarative design**

  * Design of figure is entirely declarative and decoupled from data and drawing primitives.
  * Sensible defaults.
  * Figure units are decorrelated from pixel size for easy scaling

* **Data sources**

  * Flexible, column-friendly data source system
  * Compatible with `pandas`, `numpy` arrays, lists...

* **Rendering surfaces**

  * Rendering backend is decoupled from drawing. You can render onto:
  * pixel grids, PNG
  * SVG
  * GUI window


Automatic Layout
----------------

* All the layout is done consistently and automatically.

  You can add multiple axes, multiple plots etc.
  Everything will be laid-out consistently, leaving enough space for axis ticks labels, legends etc.
  Your code never need to calculate size of anything.

Advanced typography
-------------------

* Automatic font look-up and text shaping
* Rich text
* Automatic right to left layout using unicode-bidirectional algorithm
* vertical layout

Themes
------

* Change the theme of your figure with a single line of code.
* Buitin themes included


Annotations
-----------

* Annotate your figures, with labels, infinite lines, markers etc.
* Annotations are placed using data space coordinates
