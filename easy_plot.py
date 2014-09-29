#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2014/08/08
Last Update on 2014/09/12

Author: Renaud CARRIERE
        Emmanuel NALEPA
        Jason LETORT
Contact: rcarriere@aldebaran.com
         enalepa@aldebaran.com
         jletort@presta.aldebaran-robotics.fr
Copyright: Aldebaran Robotics 2014
@pep8 : Complains without rules R0902, R0912, R0913, R0914, R0915 and W0212
"""

VERSION = "beta 1.2"

DEFAULT_CONFIG_FILE = "easy_plot.cfg"
DEFAULT_ABSCISSA = "Time"
DEFAULT_RESOLUTION_X = 1920
DEFAULT_RESOLUTION_Y = 1080
DEFAULT_PORT = 4521

DEFAULT_REFRESH_PERIOD = 0.1  # s
DEFAULT_TIME = 10  # s

PERIOD_CHECK_BUTTON = 250  # ms
PERIOD_CHECK_ACTION = 20  # ms

import numpy as np  # math et tableaux
import argparse
import os.path
import csv
import threading
import sys

try:
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtGui, QtCore
except BaseException:
    print ("Well that's embarrassing !")
    print
    print ("I can't find PyQtGraph and/or PyQt on your computer.")
    print ("Please install PyQtGraph.")
    print ("You can visit the section 'Installation' of www.pyqtgraph.org.")
    print ("If pip is already installed on your computer, you can just type")
    print ("'pip install pyqtgraph' in a command line interface.")
    print
    print ("PyQtGraph require PyQt4, Numpy and SciPy to work")
    print ("Please install PyQt4, Numpy and SciPy.")
    print ("For more informations, you can visit the following web pages:")
    print ("http://pyqt.sourceforge.net/Docs/PyQt4/installation.html")
    print ("http://www.scipy.org/scipylib/download.html")
    exit()


try:
    import easy_plot_connection
except ImportError:
    print ("Well that's embarrassing !")
    print ("I can't find easy_plot_connection on your computer.")
    print ("Please put easy_plot_connection.py on easy_plot folder")
    exit()

try:
    import read_cfg
except ImportError:
    print ("Well that's embarrassing !")
    print ("I can't find read_cfg on your computer.")
    print ("Please put read_cfg.py on easy_plot folder")
    exit()


class Button(object):

    """
    button class
    This class permits the gestion of button on figures
    """

    def __init__(self, layout, row, column):

        self.btn1 = QtGui.QPushButton('Auto Scale: OFF')
        self.btn2 = QtGui.QPushButton('Auto Range: OFF')

        style = "background-color:#121212; \
                 border:1px solid #898989; \
                 height:15px;"

        font = QtGui.QFont("Arial", 10)
        font.setBold(True)

        self.btn1.setStyleSheet(style)
        self.btn2.setStyleSheet(style)
        self.btn1.setFont(font)
        self.btn2.setFont(font)
        self.btn1.setFixedWidth(120)
        self.btn2.setFixedWidth(120)

        self.auto_scale = 0
        self.auto_range = 0

        self.timer_btn = QtCore.QTimer()
        self.timer_action = QtCore.QTimer()

        layout.addWidget(self.btn1, row, column)
        layout.addWidget(self.btn2, row, column + 2)

    def _auto_scale_on(self):
        """Private method : Enable Auto Scale"""
        self.btn1.setText("Auto Scale: ON")
        #self.btn2.setText("Auto Range: OFF")
        self.auto_scale = 1
        #self.auto_range = 0

    def _auto_scale_off(self):
        """Private method : Disable Auto Scale"""
        self.btn1.setText("Auto Scale: OFF")
        self.auto_scale = 0

    def _auto_range_on(self):
        """Pritave method : Enable Auto Range"""
        #self.btn1.setText("Auto Scale: OFF")
        self.btn2.setText("Auto Range: ON")
        self.auto_range = 1
        #self.auto_scale = 0

    def _auto_range_off(self):
        """Private method : Disable Auto Range"""
        self.btn2.setText("Auto Range: OFF")
        self.auto_range = 0

    def hide_all(self):
        """Public method : Hide buttons"""
        self.btn1.hide()
        self.btn2.hide()
        self._auto_scale_off()
        self._auto_range_off()

    def show_all(self):
        """Public method : Show buttons"""
        self.btn1.show()
        self.btn2.show()

    def update(self):
        """Public method : Update buttons"""
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
        self.number_of_points = 0
        self.datas = {}


class Data(object):

    """Class Data"""

    def __init__(self, data_x, data_y):
        self.data_x = data_x
        self.data_y = data_y


class Figure(object):

    """
    Figure class
    This class permits the gestion of figures in window
    """

    def __init__(self, window, row, column, max_time, title, label_x, unit_x,
                 label_y, unit_y, min_y, max_y, grid_x, grid_y,
                 link=None, printable=False):

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
            self.plot_widget = window.addPlot(title=self.title,
                                              row=self.row - 1,
                                              col=self.column - 1)
        else:
            self.plot_widget = pg.PlotWidget(title=self.title)

            if self.max_time is not None:
                self.plot_widget.setXRange(0, self.max_time)

        self.viewbox = self.plot_widget.getViewBox()
        self.viewbox.register(name=self.title)

        if self.min_y != None and self.max_y != None:
            self.plot_widget.setYRange(self.min_y, self.max_y)

        self.plot_widget.setLabel('bottom', self.label_x, units=self.unit_x)
        self.plot_widget.setLabel('left', self.label_y, units=self.unit_y)
        self.plot_widget.showGrid(x=self.grid_x, y=self.grid_y)
        self.plot_widget.addLegend(offset=(0, 1))

        if printable is False:
            new_row = self.row * 2
            new_col = self.column * 3

            window.addWidget(self.plot_widget, new_row, new_col, 2, 3)
            self.button = Button(window, new_row, new_col)

    def define_link(self):
        """Public method : Define link with X axes"""
        self.viewbox.linkView(axis=self.viewbox.XAxis, view=self.link.viewbox)

        if self._printable is False:
            self.button.hide_all()

    def unlink(self):
        """Public method : Remove link with X axes"""
        self.viewbox.linkView(axis=self.viewbox.XAxis, view=None)

        if self._printable is False:
            self.button.show_all()

    def action_button(self):
        """Public method : Define actions of buttons"""
        if self.link is not None:
            self.button.auto_scale = self.link.button.auto_scale
            self.button.auto_range = self.link.button.auto_range

        if self.button.auto_scale == 1 and self.button.auto_range == 0:
            self.plot_widget.enableAutoRange()
        elif self.button.auto_scale == 1 and self.button.auto_range == 1:
            self.plot_widget.enableAutoRange(
                axis=self.viewbox.YAxis, enable=True)
        else:
            self.plot_widget.disableAutoRange()

        if self.button.auto_range == 1 and len(self.curves_list) > 0:
            if self.max_time is None:
                time = DEFAULT_TIME
            else:
                time = self.max_time

            if (len(self.curves_list[0].datas.keys()) > 0):

                last_data = max(self.curves_list[0].datas.keys())

                if(self.curves_list[0].datas[last_data].data_x >= time):

                    self.plot_widget.setXRange(
                        self.curves_list[0].datas[last_data].data_x - time,
                        self.curves_list[0].datas[last_data].data_x)
            else:
                self.plot_widget.setXRange(0, time)
        else:
            pass


class Window(object):

    """
    Window class
    This class permits the gestion of all the window
    """

    def __init__(self, config_file=DEFAULT_CONFIG_FILE,
                 res_x=DEFAULT_RESOLUTION_X, res_y=DEFAULT_RESOLUTION_Y,
                 printable=False, is_rt=False):
        parameters = read_cfg.Parameters(config_file)

        self.app = QtGui.QApplication([])
        self.app.setOrganizationName('Aldebaran')
        self.app.setOrganizationDomain('aldebaran.com')
        self.app.setApplicationName('Easy Plot')

        self.max_time = parameters.max_time
        self.title = parameters.title
        self.abscissa = parameters.abscissa
        self.label_x = parameters.label_x
        self.unit_x = parameters.unit_x
        self.anti_aliasing = parameters.anti_aliasing
        self.link_x_all = parameters.link_x_all
        self.printable = printable
        self.is_rt = is_rt

        pg.setConfigOption('background', 'k')  # 101010')
        pg.setConfigOption('foreground', 'w')

        if printable is not False:
            self.window = pg.GraphicsWindow(title=self.title, border=True)
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
                                       self.label_x,
                                       self.unit_x,
                                       figure_param.label_y,
                                       figure_param.unit_y,
                                       figure_param.min_y,
                                       figure_param.max_y,
                                       figure_param.grid_x,
                                       figure_param.grid_y,
                                       printable=printable)

        viewbox_prec = None

        for pos, figure_param in parameters.figures.items():
            row = pos[0]
            column = pos[1]

            if self.link_x_all is False:
                if figure_param.link is not None:
                    try:
                        self.figures[pos].link = self.figures[
                            figure_param.link]  # .viewbox
                        self.figures[pos].define_link()
                    except (IndexError, KeyError):

                        figure1 = "[" + str(row) + "-" + str(column) + "]"
                        figure2 = str(figure_param.link).replace(", ", "-")
                        figure2 = figure2.replace("(", "[")
                        figure2 = figure2.replace(")", "]")

                        print ("ERROR: Figure " + figure1)
                        print ("       can't be linked with figure " + figure2)
                        print ("       because this figure doesn't exist")
                        print ("       Please, check configuration file")
                        pg.exit()
            else:
                if viewbox_prec is not None:
                    self.figures[pos].link = viewbox_prec
                    self.figures[pos].define_link()

                viewbox_prec = self.figures[pos]  # .viewbox

        # Populate the curves dictionnary
        for name, curve_param in parameters.curves.items():
            curve_row = curve_param.row
            curve_column = curve_param.column

            try:
                figure = self.figures[(curve_row, curve_column)]
            except KeyError:
                txt = "[" + str(curve_row) + "-" + str(curve_column) + "]"
                print ("ERROR: Curve " + name + " is define at " + txt)
                print ("       but there is no figure at these coordonates")
                print ("       Please, check configuration file")
                pg.exit()

            plot = figure.plot_widget.plot(pen=curve_param.color,
                                           name=curve_param.legend)

            curve = Curve(curve_param.legend, curve_param.color, plot)

            self.curves[name] = curve
            self.figures[(curve_row, curve_column)].curves_list.append(curve)

        if self.printable is False:
            self.window.setLayout(self.layout)

            if self.is_rt is True:
                for fig in self.figures.values():

                    if fig.link is None:
                        fig.button.btn1.setText("Auto Scale: ON")
                        fig.button.btn2.setText("Auto Range: ON")
                        fig.button.auto_scale = 1
                        fig.button.auto_range = 1

                    fig.button.timer_btn.timeout.connect(fig.button.update)
                    fig.button.timer_btn.start(PERIOD_CHECK_BUTTON)

                    fig.button.timer_action.timeout.connect(fig.action_button)
                    fig.button.timer_action.start(PERIOD_CHECK_ACTION)

        self.window.show()

    def _print_error(self, curve_name):
        """Print Error in case of curve name problem with rt plot """
        if self.is_rt is True:
            print ("ERROR : The curve '" + curve_name + "'' is not present in")
            print (
                "the configuration file, but a point has to be added to this")
            print ("curve.")
            pg.exit()

    def curve_display(self, curve_name):
        """Public method : Display a curve"""
        if curve_name in self.curves.keys():
            curve = self.curves[curve_name]

            datas_x, datas_y = self._dico_to_list(curve_name)

            curve.plot.setData(datas_x, datas_y)
        else:
            self._print_error(curve_name)

    def add_point(self, curve_name, var_x, var_y, has_to_plot=True):
        """Public method : add points on curve"""
        if curve_name in self.curves.keys():
            curve = self.curves[curve_name]
            curve.datas[curve.number_of_points] = Data(var_x, var_y)
            curve.number_of_points += 1

        if has_to_plot is True:
            self.curve_display(curve_name)

    def check_curves_in_csv(self, csv_curve_list):
        """ check if curves from cfg are in csv """
        if self.is_rt is False:
            for name in self.curves.keys():
                if name not in csv_curve_list:
                    print ("WARNING: " + name + " is in cfg but not in csv")

    def curves_erase(self):
        """Public method : Erase all curves of the window"""
        for curve in self.curves.values():
            curve.datas = {}

    def _dico_to_list(self, curve_name):
        """Private method : Put dictionnary in a list"""
        datas_num = self.curves[curve_name].datas.keys()
        datas_num.sort()

        datas_x = []
        datas_y = []

        for num in datas_num:
            datas_x.append(self.curves[curve_name].datas[num].data_x)
            datas_y.append(self.curves[curve_name].datas[num].data_y)

        return datas_x, datas_y

    def run(self):
        """Public method : Run application"""
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            self.app.instance().exec_()
            print
            pg.exit()


def main():
    """Read the configuration file, the data file and plot"""
    parser = argparse.ArgumentParser(description="Plot datas from a CSV file")

    parser.add_argument("data_file_list", metavar="DATAFILE", nargs="*",
                        help="Input CSV data files")

    parser.add_argument("-c", "--configFile", dest="config_file",
                        default=DEFAULT_CONFIG_FILE,
                        help="configuration plot file\
                        (default: " + DEFAULT_CONFIG_FILE + ")")

    parser.add_argument("-p", "--printable", dest="printable",
                        action="store_const",
                        const=True, default=False,
                        help="add option to run printable easy_plotter")

    parser.add_argument("-rx", "--resolution-x", dest="res_x",
                        default=DEFAULT_RESOLUTION_X, type=int,
                        help="X resolution of window\
                        (default: " + str(DEFAULT_RESOLUTION_X) + ")")

    parser.add_argument("-ry", "--resolution-y", dest="res_y",
                        default=DEFAULT_RESOLUTION_Y, type=int,
                        help="Y resolution of window\
                        (default: " + str(DEFAULT_RESOLUTION_Y) + ")")

    parser.add_argument("-i", "--IP", dest="server_ip",
                        default=None,
                        help="server IP address")

    parser.add_argument("-po", "--port", dest="port", default=DEFAULT_PORT,
                        type=int,
                        help="server port (default: " + str(DEFAULT_PORT) + ")")

    parser.add_argument("-r", "--refresh-period", dest="refresh_period",
                        type=float, default=DEFAULT_REFRESH_PERIOD,
                        help="refresh period for real time plot\
                        (default: 0.1s)")

    parser.add_argument("-s", "--sort", dest="sort",
                        action="store_const",
                        const=True, default=False,
                        help="sort datas on abscissa\
                        (automatic with several data files)")

    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s " + VERSION)

    args = parser.parse_args()

    config_file = args.config_file
    data_file_list = args.data_file_list
    res_x = args.res_x
    res_y = args.res_y
    server_ip = args.server_ip
    port = args.port
    refresh_period = args.refresh_period
    printable = args.printable
    sort = args.sort

    if len(data_file_list) > 1:
        print "X datas will be sorted"
        sort = True

    if server_ip and data_file_list:
        print ("Please chose plotting datas from a file OR from a server.")
        print ("If using option '-i' or '--IP', please do not specify a")
        print ("data file to read.'")
        pg.exit()

    # Test if configuration file exists
    if not os.path.isfile(config_file):
        print ("ERROR : File '" + config_file + "' cannot be found")
        pg.exit()

    # Test if all data files exist
    for data_file in data_file_list:
        if not os.path.isfile(data_file):
            print ("ERROR : File '" + data_file + "' cannot be found")
            pg.exit()

    # Create the window
    if server_ip is not None:
        win = Window(config_file=args.config_file, res_x=res_x, res_y=res_y,
                     printable=printable, is_rt=True)
    else:
        win = Window(config_file=args.config_file, res_x=res_x, res_y=res_y,
                     printable=printable, is_rt=False)

    abscissa = win.abscissa

    # Plotting from CSV files
    csv_dic = {}
    element_number = 0
    for data_file in data_file_list:
        dic_data = csv.DictReader(open(data_file))

        element_number = 0
        for index, row in enumerate(dic_data):
            # Test if abscissa key exist in dic_data
            if not index:
                if abscissa not in row:
                    print ("ERROR : '%s' not find in File '%s'\
                    " % (abscissa, data_file))
                    pg.exit()

            test_datax_flag = False
            try:
                data_x = float(row[abscissa])
                test_datax_flag = True
            except BaseException:
                print ("WARNING: a data x value is not a number")

            if test_datax_flag is True:
                for key, value in row.items():
                    test_datay_flag = False
                    if value is not None:
                        try:
                            data_y = float(value)
                            test_datay_flag = True
                        except (TypeError, ValueError):
                            print ("WARNING: " + str(value) + " in " +
                                   str(key) + " is not a number")
                            pg.exit()
                    else:
                        print (
                            "WARNING: None Value in " + str(key))

                    if test_datay_flag is True:
                        data = Data(data_x, data_y)
                        cur_curve = csv_dic.setdefault(key, {})
                        cur_curve.update({element_number: data})
                        element_number += 1

                        # if data_x not in cur_curve:
                        #     cur_curve.update({data_x: [data_y]})
                        # else:
                        #     cur_curve[data_x].append(data_y)
                        #     cur_curve.update(
                        #         {data_x: cur_curve[data_x]})

    if len(data_file_list) > 0:
        win.check_curves_in_csv(csv_dic.keys())

    for curve in csv_dic.keys():

        datas_x = []
        datas_y = []

        datas_num = csv_dic[curve].keys()

        if sort is True:
            datas_dic = {}
            for num in datas_num:
                datas_dic[csv_dic[curve][num].data_x] = csv_dic[
                    curve][num].data_y

            datas_x = datas_dic.keys()
            datas_x.sort()

            for x_value in datas_x:
                datas_y.append(datas_dic[x_value])

        else:
            datas_num.sort()

            for num in datas_num:
                datas_x.append(csv_dic[curve][num].data_x)
                datas_y.append(csv_dic[curve][num].data_y)

        for data_x, data_y in zip(datas_x, datas_y):
            win.add_point(curve, data_x, data_y, False)

    for curve in win.curves:
        win.curve_display(curve)

    # In case of plotting from CSV file(s), hide buttons
    if not server_ip and printable is False:
        for fig in win.figures.values():
            fig.button.hide_all()

    # In case of plotting from a socket, begin to ask (in another thread)
    # if datas are avaible and plot them
    if server_ip is not None:
        thread = threading.Thread(target=easy_plot_connection.Client,
                                  args=(win, server_ip, port, refresh_period))
        thread.daemon = True
        thread.start()

    win.run()

if __name__ == '__main__':
    main()
