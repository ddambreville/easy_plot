Name      : easy_plot.py
Version   : Alpha
Date      : 2014/09/05
Author    : Renaud CARRIERE
            Emmanuel NALEPA
            Jason LETORT
Contact   : rcarriere@aldebaran.com
            enalepa@aldebaran.com
            jletort@presta.aldebaran-robotics.fr
Copyright : Aldebaran Robotics 2014

Requires  : - pyqtgraph library must be install on your computer

Known issue :
    - figures dimensions may be not equal

Summary : This module permit to plot datas easilier from cvs file


------------------------------------------------------------------------------
Note: On linux only, you can add the easy_plot path to your bashrc file,
      in order to call easy_plot from everywhere on you computer.

*** How to do that: ***
1) Go in your easy_plot repertory, enter pwd, then copy the answer.

2) Open your bashrc :
                     gedit /home/$USER/.bashrc

3) Put the easy plot path at the end of your bashrc :
                     PATH=$PATH:[answer of pwd]
   Where [answer of pwd] is the answer of pwd command come to step 1)

4) Save your bashrc

==============================================================================

                            HOW IT WORKS ?

==============================================================================

1) Configure the file describing what you want to plot.
-------------------------------------------------------

A example is provided in easy_plot.cfg

The configuration file structure is following :

[General]
MaxTime         : [maximum time]
Title           : [title]
Abscissa        : [abscissa]
LabelX          : [label on X axis]
UnitX           : [unit of X axis]
Anti-aliasing   : [anti aliasing]
LinkXAll        : [link all x axis]

[[row of figure]-[column of figure]]
Title  : [title of figure]
LabelY : [label on Y axis]
UnitY  : [unit on Y axis]
GridX  : [grid on X]
GridY  : [grid on Y]
MinY   : [minimum Value on Y]
MaxY   : [maximum Value on X]
Link   : [row figure to link location] [col figure to link location]

[[row of figure]-[column of figure]]
Title  : [title of figure]
LabelY : [label on Y axis]
UnitY  : [unit on Y axis]
GridX  : [grid on X]
GridY  : [grid on Y]
MinY   : [minimum Value on Y]
MaxY   : [maximum Value on Y]
Link   : [row figure to link location] [col figure to link location]

...

[Curves]
[CurveName] : [Row] [Column] [Legend] [Color] [Width]
[CurveName] : [Row] [Column] [Legend] [Color] [Width]
...

where :
- [maximum time] is the maximum time of each curve
- [title] is the title of the window
- [abscissa] define abscissa of curves. It must be the same as in
        cvs file. If not specified, the default abscissa is Time
- [label on X axis] is the label on the X axis. If not specified, the default
        label is [abscissa]
- [unit of X axis] is the unity of data on the X axis
- [anti aliasing] is True if you want anti aliasing to be applied to the
  window, False else
- [link all x axis] is True if you want to link all x axis,
  False else
- [[row of figure]-[column of figure]] is the location of the figure on the
  window. For example [1-1] is the first figure
- [title of figure] is the title of the figure
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
- [Color] is the color of the curve. Must be : * r or red
                                               * g or green
                                               * b or blue
                                               * c or cyan
                                               * m or magenta
                                               * y or yellow
                                               * k or black
                                               * w or white
                                               * hexadecimal color strings;
                                                 may begin with #
- [Width] is the size of the curve. If not specified, the default width is 1

_______________________________________________________________________________

2) Launch easy_plot.
-----------------------

The easy plotter can be use as a program or as an API.

If you use it as a program:

usage: python easy_plot.py [-h] [-c CONFIG_FILE] [-rx RES_X] [-ry RES_Y]
                    [-i SERVER_IP] [-po PORT] [-r REFRESH_PERIOD]
                    [DATAFILE [DATAFILE ...]]

(Note : On linux, you can replace python easy_plot.py by ./easy_plot.py)


The following options are both for real time and static plotting:
----------------------------------------------------------------
[-h] (optional) display help

[-c CONFIGFILE] (optional) is to specify the path to the configuration file.
        If not specified, the default configuration file is "easy_plot.cfg".

[-rx RESOLUTION] (optional) define resolution in x of window.
        If not specified, the default resolution is 1920.

[-ry RESOLUTION] (optional) define resolution in y of window.
        If not specified, the default resolution is 1080.

[-p] (optional) permit to run a full printable version of easy plot.
        You can print all window, and not just one figure.
        (Note: buttons are not available with this option.)

The following options are for real time plotting only:
------------------------------------------------------
[-i SERVER_IP] define server IP address for real time plotting.
        If not specified, you can't use real time plotting, and you must
        specify [DATAFILE].

[-po PORT] (optional) define server port. If not specified, the default port
        is 4521.

[-r REFRESH_PERIOD]  (optional) define the refresh period. If not specified,
        the default refresh period is 0.1 s.


The following option is for static plotting only:
-------------------------------------------------
[DATAFILE] is to specify the path to the cvs data file, if -i option is not
        specify. A example is provided in example.cvs


If you use it as an API :
  An example is given in example_rt_plot.py

******************************************************************************

If you have detected any bug or if you need a special feature, please contact
one of the authors.
