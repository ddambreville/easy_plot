#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2014/08/08
Last Update on 2014/09/04

Author: Renaud CARRIERE
        Emmanuel NALEPA
Contact: rcarriere@aldebaran.com
         enalepa@aldebaran.com
Copyright: Aldebaran Robotics 2014
"""

DEFAULT_CONFIG_FILE = "easy_plot.cfg"
DEFAULT_ABSCISSA = "Time"

import argparse
import os.path
import csv

import sys

from pyqtgraph.Qt import QtGui, QtCore

try:
    import pyqtgraph as pg
    import read_cfg
except ImportError:
    print "Well that's embarrassing !"
    print "I can't find pyqtgraph on your computer. Please install pyqtgraph."
    print 'You can visit the section "Installation" of www.pyqtgraph.org.'
    print 'If pip is already installed on your computer, you can just type'
    print '"pip install pyqtgraph" in a command line interface.'
    exit()


class Button(object):

    """
    button class
    This class permits the gestion of button on figures
    """

    def __init__(self, layout, row, column):


        self.btn1 = QtGui.QPushButton('Auto Scale: OFF')
        self.btn2 = QtGui.QPushButton('Auto Range: OFF')

        style = "background-color:#121212; border:1px solid #898989; height:15px;"
        font = QtGui.QFont("Arial",10)
        font.setBold(True)

        self.btn1.setStyleSheet(style)
        self.btn2.setStyleSheet(style)
        self.btn1.setFont(font)
        self.btn2.setFont(font)
        self.btn1.setFixedWidth(120)
        self.btn2.setFixedWidth(120)

        self.auto_scale = 0
        self.auto_range = 0

        self.timer_btn1 = QtCore.QTimer()
        self.timer_btn2 = QtCore.QTimer()

        layout.addWidget(self.btn1, row, column)
        layout.addWidget(self.btn2, row, column + 2)

    def _auto_scale_on(self):
        """Private method : Enable Auto Scale"""
        self.btn1.setText("Auto Scale: ON")
        self.btn2.setText("Auto Range: OFF")
        self.auto_scale = 1
        self.auto_range = 0

    def _auto_scale_off(self):
        """Private method : Disable Auto Scale"""
        self.btn1.setText("Auto Scale: OFF")
        self.auto_scale = 0

    def _auto_range_on(self):
        """Pritave method : Enable Auto Range"""
        self.btn1.setText("Auto Scale: OFF")
        self.btn2.setText("Auto Range: ON")
        self.auto_range = 1
        self.auto_scale = 0

    def _auto_range_off(self):
        """Private method : Disable Auto Range"""
        self.btn2.setText("Auto Range: OFF")
        self.auto_range = 0

    def _hide_all(self):
        self.btn1.hide()
        self.btn2.hide()

    def _show_all(self):
        self.btn1.show()
        self.btn2.show()

    def _update(self):

        if self.auto_scale == 0:
            self.btn1.clicked.connect(self._auto_scale_on)
        else:
            self.btn1.clicked.connect(self._auto_scale_off)

        if self.auto_range == 0:
            self.btn2.clicked.connect(self._auto_range_on)
        else:
            self.btn2.clicked.connect(self._auto_range_off)


class Curve(object):

    """
    curve class
    This class permits the gestion of curves in figures
    """

    def __init__(self, legend, color, plot):
        self.legend = legend
        self.color = color
        self.plot = plot

        self.datas = {}


class Figure(object):

    """
    Figure class
    This class permits the gestion of figures in window
    """

    def __init__(self, window, row, column, max_time, title, label_x, unit_x,
                 label_y, unit_y, min_y, max_y, grid_x, grid_y,
                 link=None, link_button=None, printable = False):


        # Figure parameters
        self.row = row
        self.column = column
        self.max_time = max_time
        self.title = title
        self.label_x = label_x
        self.unit_x = unit_x
        self.label_y = label_y
        self.unit_y = unit_y
        self.min_y = min_y
        self.max_y = max_y
        self.grid_x = grid_x
        self.grid_y = grid_y

        self._printable = printable
        self.link = link

        self.curves_list = []
        # Figure graphicals parameters

        if printable is not False:
            self.pw = window.addPlot(title=self.title,
                                     row=self.row-1,
                                     col=self.column-1)
        else:
            self.pw = pg.PlotWidget(title=self.title)

        self.vb = self.pw.getViewBox()
        self.vb.register(name = self.title)
        #self.vb.setBackgroundColor('k')

        if self.min_y != None and self.max_y != None:
            self.pw.setYRange(self.min_y, self.max_y)

        self.pw.setLabel('bottom', self.label_x, units=self.unit_x)
        self.pw.setLabel('left', self.label_y, units=self.unit_y)
        self.pw.showGrid(x=self.grid_x, y=self.grid_y)
        self.pw.addLegend(offset=(0,1))

        if printable is False:
            new_row = self.row * 2
            new_col = self.column * 3

            window.addWidget(self.pw, new_row, new_col, 2, 3)
            self.button = Button(window, new_row, new_col)

    def define_link(self):
            self.vb.linkView(axis=self.vb.XAxis, view=self.link)

            if self._printable is False:
                self.button._hide_all()

    def unlink(self):
            self.vb.linkView(axis=self.vb.XAxis, view=None)

            if self._printable is False:
                self.button._show_all()

    def _action_button(self):

        if self.button.auto_scale == 1:
            self.pw.enableAutoRange()
        else:
            self.pw.disableAutoRange()

        if self.button.auto_range == 1:
            if len(self.curves_list) != 0:
                self.pw.setXRange(max(self.curves_list[0].datas.keys()) - 10,
                                  max(self.curves_list[0].datas.keys()) + 10)
            else:
                self.pw.setXRange(0, self.max_time)
        else:
            pass

        # if self.button.auto_scale == 1 or self.button.auto_range == 1:
        #     self.unlink()





class Window(object):

    """
    Window class
    This class permits the gestion of all the window
    """

    def __init__(self, config_file, res_x=1920, res_y=1080, printable = False):
        parameters = read_cfg.Parameters(config_file)

        self.app = QtGui.QApplication([])

        self.max_time = parameters.max_time
        self.title = parameters.title
        self.anti_aliasing = parameters.anti_aliasing
        self.link_x_all = parameters.link_x_all

        pg.setConfigOption('background', 'k')# #101010')
        pg.setConfigOption('foreground', 'w')

        if printable is not False:
            self.window = pg.GraphicsWindow(title = self.title, border=True)
        else:
            self.window = QtGui.QWidget()
            self.window.setStyleSheet("QWidget {background-color: #111111 }")
            self.layout = QtGui.QGridLayout()

        self.window.setWindowTitle(self.title)
        self.window.resize(res_x, res_y)


        pg.setConfigOptions(antialias=self.anti_aliasing)

        # A figure contains 0 or more curves
        self.figures = {}

        # A curve belong to exactly one figure
        self.curves = {}

        # Populate the figures dictionnary
        for pos, figure_param in parameters.figures.items():
            row = pos[0]
            column = pos[1]

            if printable is not False:
                win = self.window
            else:
                win = self.layout

            self.figures[pos] = Figure(win, row, column, self.max_time,
                                       figure_param.title,
                                       figure_param.label_x,
                                       figure_param.unit_x,
                                       figure_param.label_y,
                                       figure_param.unit_y,
                                       figure_param.min_y,
                                       figure_param.max_y,
                                       figure_param.grid_x,
                                       figure_param.grid_y,
                                       printable=printable)

        for pos, figure_param in parameters.figures.items():
            row = pos[0]
            column = pos[1]

            if self.link_x_all is False :
                if figure_param.link is not None:
                    try:
                        self.figures[pos].link = self.figures[figure_param.link].vb
                        self.figures[pos].define_link()
                    except:
                        print "ERROR: Figure ("+str(row)+"-"+str(column)+") can be linked"
                        print "       with figure "+str(figure_param.link)+" because this"
                        print "       figure doesn't exist"
                        print "       Please, check configuration file"
            else:
                try:
                    self.figures[pos].link = vb_prec
                    self.figures[pos].define_link()
                    self.figures[pos].button.is_link = True
                except:
                    pass

                vb_prec = self.figures[pos].vb


        # Populate the curves dictionnary
        for name, curve_param in parameters.curves.items():
            curve_row = curve_param.row
            curve_column = curve_param.column

            try:
                figure = self.figures[(curve_row, curve_column)]
            except KeyError:
                print "ERROR: Curve " +name+" is define at "+str(curve_row)+" - "+str(curve_column)
                print "       but there is no figure at these coordonates"
                print "       Please, check configuration file"
                exit()

            plot = figure.pw.plot(pen=curve_param.color,
                                  name=curve_param.legend)

            curve = Curve(curve_param.legend, curve_param.color, plot)

            self.curves[name] = curve
            self.figures[(curve_row, curve_column)].curves_list.append(curve)

        if printable is False:
            self.window.setLayout(self.layout)

            for pos, fig in self.figures.items():
                fig.button.timer_btn1.timeout.connect(fig.button._update)
                fig.button.timer_btn1.start(10)

                fig.button.timer_btn2.timeout.connect(fig._action_button)
                fig.button.timer_btn2.start(10)

        self.window.show()

    def add_point(self, curve_name, x, y, has_to_plot=True):
        #Test if curve name exist in config file
        if curve_name in self.curves.keys():
            curve = self.curves[curve_name]

            curve.datas[x] = y

            if has_to_plot:
                datas_x, datas_y = self._dico_to_list(curve_name)
                curve.plot.setData(datas_x, datas_y)

    def curve_display(self, curve_name):
        curve = self.curves[curve_name]

        datas_x, datas_y = self._dico_to_list(curve_name)

        curve.plot.setData(datas_x, datas_y)

    def _dico_to_list(self, curve_name):
        curve = self.curves[curve_name]

        datas_x = curve.datas.keys()
        datas_x.sort()
        datas_y = [curve.datas[x] for x in datas_x]

        return datas_x, datas_y

    def run(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            self.app.instance().exec_()
            pg.exit()


def main():
    """Read the configuration file, the data file and plot"""
    parser = argparse.ArgumentParser(description="Plot datas from a CSV file")

    parser.add_argument("data_file_list", metavar="DATAFILE", nargs="+",
                        help="Input CSV data files")

    parser.add_argument("-c", "--configFile", dest="config_file",
                        default=DEFAULT_CONFIG_FILE,
                        help="configuration plot file\
                        (default: "+DEFAULT_CONFIG_FILE+")")

    parser.add_argument("-a", "--abscissa", dest="abscissa",
                        default=DEFAULT_ABSCISSA,
                        help="asbcissa name\
                        (default: "+DEFAULT_ABSCISSA+")")

    parser.add_argument("-p", "--printable", dest="printable", action="store_const",
                        const=True, default=False,
                        help="add option to run printable easy_plotter")




    args = parser.parse_args()

    config_file = args.config_file
    data_file_list = args.data_file_list
    abscissa = args.abscissa
    printable = args.printable

    # Test if configuration file exists
    if not os.path.isfile(config_file):
        print 'ERROR : File "' + config_file + '" cannot be found'
        exit()

    # Test if all data files exist
    for data_file in data_file_list:
        if not os.path.isfile(data_file):
            print 'ERROR : File "' + data_file + '" cannot be found'
            exit()

    win = Window(config_file=args.config_file,printable=printable)

    for data_file in data_file_list:
        dic_data = csv.DictReader(open(data_file))

        for index, row in enumerate(dic_data):
            #Test if abscissa key exist in dic_data
            if not index:
                if abscissa not in row:
                    print 'ERROR : "%s" not find in File "%s"' % (abscissa, data_file)
                    exit()
            x = float(row[abscissa])

            for key, value in row.items():
                if key != abscissa:
                    y = float(value)
                    win.add_point(key, x, y, False)

        for curve in win.curves:
            win.curve_display(curve)

    win.run()


if __name__ == '__main__':
    main()
