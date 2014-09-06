Name      : easy_plot.py
Version   : 0.1 (Beta)
Date      : 2014/09/05
Author    : Renaud CARRIERE
Contact   : rcarriere@aldebaran.com
Copyright : Aldebaran Robotics 2014

Requires  : - pyqtgraph library must be install on your computer

Known issue :
    - With -p option, figures dimensions are not equal

Summary : This module permit to plot datas easilier from cvs file

===============================================================================

                            HOW IT WORKS ?

===============================================================================

1) Configure the file describing what you want to plot.
-------------------------------------------------------

A example is provided in easy_plot.cfg

The configuration file structure is following :

[General]
MaxTime         : [maximum time]
Title           : [title]
Anti-aliasing   : [anti aliasing]
LinkXAll        : [link all x axis]

[[row of figure]-[column of figure]]
Title  : [title of figure]
LabelX : [label on X axis]
UnitX  : [unit of X axis]
LabelY : [label on Y axis]
UnitY  : [unit on Y axis]
GridX  : [grid on X]
GridY  : [grid on Y]
MinY   : [minimum Value on Y]
MaxY   : [maximum Value on X]
Link   : [row figure to link location] [col figure to link location]

[[row of figure]-[column of figure]]
Title  : [title of figure]
LabelX : [label on X axis]
UnitX  : [unit of X axis]
LabelY : [label on Y axis]
UnitY  : [unit on Y axis]
GridX  : [grid on X]
GridY  : [grid on Y]
MinY   : [minimum Value on Y]
MaxY   : [maximum Value on Y]
Link   : [row figure to link location] [col figure to link location]

...

[Curves]
[CurveName] : [Row] [Column] [Legend] [Color]
[CurveName] : [Row] [Column] [Legend] [Color]
...

where :
- [maximum time] is the maximum time of each curve
- [title] is the title of the window
- [anti aliasing] is True if you want anti aliasing to be applied to the
  window, False else
- [link all x axis] is True if you want to link all x axis,
  False else
- [[row of figure]-[column of figure]] is the location of the figure on the
  window. For example [1-1] is the first figure
- [title of figure] is the title of the figure
- [label on X axis] is the label on the X axis
- [unit of X axis] is the unity of data on the X axis
- [label on Y axis] is the label on the Y axis
- [unit on Y axis] is the unity of data on the Y axis
- [grid on X] is True if you want grid on X axis, False else
- [grid on Y] is True if you want grid on Y axis, False else
- [minimum Value on Y] is the minimum value of Y axis
- [maximum Value on Y] is the maximum value of Y axis
- [figure to link location] is the coordonate of figure to link
- [CurveName] is the name of the curve. Must be the same as in cvs file.
- [Row] is the row number of the curve. It corresponds on row of figure you
  want to put the curve.
- [Column] is the column number of the curve. It corresponds on columne of
  figure you want to put the curve.
- [Legend] is the legend of the curve
- [Color] is the color of the curve. Must be : * r for red
                                               * g for green
                                               * b for blue
                                               * c for cyan
                                               * m for magenta
                                               * y for yellow
                                               * k for black
                                               * w for white
                                               * hexadecimal color strings;
                                                 may begin with #

_______________________________________________________________________________

2) Launch easy_plotter.
-----------------------

The easy plotter can be use as a program or as an API.

If you use it as a program:

usage: python easy_plot.py [-h] [-c CONFIG_FILE] [-a ABSCISSA] [-p] [DATAFILE]
(Note : On linux, you can replace python easy_plot.py by ./easy_plot.py)

[-h] (optional) display help

[-c CONFIGFILE] (optional) is to specify the path to the configuration file.
        If not specified, the default configuration file is "easy_plot.cfg".

[-a ABSCISSA] (optional) define abscissa of curves. It must be the same as in
        cvs file. If not specified, the default abscissa is Time.

[-r RESOLUTION] (optional) define resolution of window.
        It must be [x resolution]x[y resolution] string.
        For example : 1200x800
        If not specified, the default resolution is 1920x1080.

[-p] (optional) permit to run a full printable version of easy plot.
        You can print all window, and not just one figure.
        (Note: buttons are not available with this option.)

[DATAFILE] is to specify the path to the cvs data file.
        A example is provided in example.cvs

If you use it as an API :
  An example is given in static_example.py for static plot
  An example is given in dynamic_example.py for dynamic plot

*******************************************************************************

If you have detected any bug or if you need a special feature, please contact
the author.
