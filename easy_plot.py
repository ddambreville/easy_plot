#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2014/08/08
Last Update on 2014/08/13

Author: Renaud CARRIERE
Contact: rcarriere@presta.aldebaran-robotics.fr
Copyright: Aldebaran Robotics 2014
"""

DEFAULT_CONFIG_FILE = "easy_plot.cfg"
DEFAULT_ABSCISSA = "Time"
DEFAULT_SOCK_PORT = 4521

import argparse
import os.path
import read_cfg
import csv
import socket
import threading
import time

from pyqtgraph.Qt import QtGui, QtCore

try:
    import pyqtgraph as pg
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
        self.btn1 = QtGui.QPushButton('auto_scale: OFF')
        self.btn2 = QtGui.QPushButton('Auto Range: ON')

        self.btn1.setStyleSheet(
            "background-color:#000000; border: 2px solid #898989")

        self.btn2.setStyleSheet(
            "background-color:#000000; border: 2px solid #898989")

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

        #self.datas = {}
        self.datas_x = []
        self.datas_y = []


class Figure(object):

    """
    Figure class
    This class permits the gestion of figures in window
    """

    def __init__(self, layout, row, column, max_time, title, label_x, unit_x,
                 label_y, unit_y, min_y, max_y, grid_x, grid_y):

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

        # Figure graphicals parameters
        self.pw = pg.PlotWidget(title=self.title)

        if self.min_y != None and self.max_y != None:
            self.pw.setYRange(self.min_y, self.max_y)

        self.pw.setLabel('bottom', self.label_x, units=self.unit_x)
        self.pw.setLabel('left', self.label_y, units=self.unit_y)
        self.pw.showGrid(x=self.grid_x, y=self.grid_y)

        # self.pw.hideButtons()

        new_row = self.row * 2
        new_col = self.column * 3

        layout.addWidget(self.pw, new_row, new_col, 2, 3)
        #self.button = button(layout, new_row, new_col)

    def _action_button(self):
        if self.button.auto_scale == 1:
            self.pw.enableAutoRange()
        else:
            self.pw.disableAutoRange()

        if self.button.auto_range == 1:
            if len(self.curves_list) != 0:
                self.pw.setXRange(self.curves_list[0].data_cloud_x[0] -
                                  int(self.max_time / 2),
                                  self.curves_list[0].data_cloud_x[0] +
                                  int(self.max_time / 2))
            else:
                self.pw.setXRange(0, self.max_time)
        else:
            pass


class Window(object):

    """
    Window class
    This class permits the gestion of all the window
    """

    def __init__(self, config_file, res_x=1920, res_y=1080):
        parameters = read_cfg.Parameters(config_file)

        self.app = QtGui.QApplication([])
        self.window = QtGui.QWidget()

        self.max_time = parameters.max_time
        self.nb_row = parameters.nb_row
        self.nb_col = parameters.nb_column
        self.nb_figure = self.nb_row * self.nb_col
        self.title = parameters.title
        self.anti_aliasing = parameters.anti_aliasing
        self.refresh = parameters.update

        self.window.setStyleSheet("QWidget {background-color: #111111 }")
        self.window.resize(res_x, res_y)
        self.window.setWindowTitle(self.title)
        self.layout = QtGui.QGridLayout()
        self.figure_list = []

        # A figure contains 0 or more curves
        self.figures = {}

        # A curve belong to exactly one figure
        self.curves = {}

        pg.setConfigOptions(antialias=self.anti_aliasing)

        # Populate the figures dictionnary
        for pos, figure_param in parameters.figures.items():
            row = pos[0]
            column = pos[1]
            self.figures[pos] = Figure(self.layout, row, column, self.max_time,
                                       figure_param.title,
                                       figure_param.label_x,
                                       figure_param.unit_x,
                                       figure_param.label_y,
                                       figure_param.unit_y,
                                       figure_param.min_y,
                                       figure_param.max_y,
                                       figure_param.grid_x,
                                       figure_param.grid_y)

        # Populate the curves dictionnary
        for name, curve_param in parameters.curves.items():
            curve_row = curve_param.row
            curve_column = curve_param.column

            figure = self.figures[(curve_row, curve_column)]

            plot = figure.pw.plot(pen=curve_param.color,
                                  name=curve_param.legend)

            curve = Curve(curve_param.legend, curve_param.color, plot)

            self.curves[name] = curve

        self.window.setLayout(self.layout)

        self.window.show()

    def add_point(self, curve_name, x, y, has_to_plot=True):
        """Add point to a curve"""
        # Test if curve name exist in config file
        if curve_name in self.curves.keys():
            curve = self.curves[curve_name]

            """
            if x not in curve.datas:
                curve.datas[x] = y
            else:
                print 'curve %s already have data for time %s'\
                    % (curve_name, x)
                exit()
            """

            curve.datas_x.append(x)
            curve.datas_y.append(y)

            if has_to_plot:
                """
                datas_x, datas_y = self._dico_to_list(curve_name)
                curve.plot.setData(datas_x, datas_y)
                """
                curve.plot.setData(curve.datas_x, curve.datas_y)

    def curve_display(self, curve_name):
        curve = self.curves[curve_name]
        #datas_x, datas_y = self._dico_to_list(curve_name)

        curve.plot.setData(curve.datas_x, curve.datas_y)

    def _dico_to_list(self, curve_name):
        curve = self.curves[curve_name]

        datas_x = curve.datas.keys()
        datas_x.sort()
        datas_y = [curve.datas[x] for x in datas_x]

        return datas_x, datas_y

    def run(self):
        self.app.exec_()


def wait_connection(sock, host, window):
    """Wait connection and run sock's thread"""
    port = DEFAULT_SOCK_PORT
    nb_try = 0
    nb_try_max = 5

    while nb_try <= nb_try_max:
        try:
            sock.connect((host, port))
            break
        except (socket.error):
            time.sleep(3)
            nb_try += 1

    if nb_try >= nb_try_max:
        print 'Connection to host "%s" impossible' % host
        exit()
    sock_run(sock, window)


def sock_run(sock, window):
    """allow data transfer with princial window"""
    from socket_connection import NewConnection
    serveur = NewConnection(sock)
    while True:
        # Data dispo
        answer = serveur.is_data_dispo()
        if answer is not None:
            for name, data_x, data_y in answer:
                window.add_point(name, float(data_x), float(data_y))
        time.sleep(window.refresh)


def main():
    """Read the configuration file, the data file and plot"""
    parser = argparse.ArgumentParser(description="Plot datas from a CSV file")

    parser.add_argument("data_file_list", metavar="DATAFILE", nargs="*",
                        help="Input CSV data files")

    parser.add_argument("-c", "--configFile", dest="config_file",
                        default=DEFAULT_CONFIG_FILE,
                        help="configuration plot file\
                        (default: easy_plot.cfg)")

    parser.add_argument("-a", "--abscissa", dest="abscissa",
                        default=DEFAULT_ABSCISSA,
                        help="asbcissa name\
                        (default: Time)")

    parser.add_argument("-s", "--serveur", dest="serveur",
                        default=False,
                        help="serveur address\
                        (default: False)")

    args = parser.parse_args()

    config_file = args.config_file
    data_file_list = args.data_file_list
    abscissa = args.abscissa
    sock_host = args.serveur

    # Test if configuration file exists
    if not os.path.isfile(config_file):
        print 'ERROR : File "' + config_file + '" cannot be found'
        exit()

    # Test if all data files exist
    for data_file in data_file_list:
        if not os.path.isfile(data_file):
            print 'ERROR : File "' + data_file + '" cannot be found'
            exit()

    win = Window(args.config_file)

    if data_file_list:
        # disable connection to serveur if demanded by user
        if sock_host:
            print 'Connection to serveur "%s" abord' % sock_host
            print 'Cannot read csv files and connect to seveur'
            sock_host = False

    csv_dic = {}
    for data_file in data_file_list:
        dic_data = csv.DictReader(open(data_file))

        for index, row in enumerate(dic_data):
            # Test if abscissa key exist in dic_data
            if not index:
                if abscissa not in row:
                    print 'ERROR : "%s" not find in File "%s"'\
                        % (abscissa, data_file)
                    exit()
            x = float(row[abscissa])

            for key, value in row.items():
                if key != abscissa:
                    y = float(value)
                    cur_curve = csv_dic.setdefault(key, {})
                    if x not in cur_curve:
                        cur_curve.update({x: y})
                    else:
                        print 'Error : Curve %s already has value for time %s'\
                            % (key, str(x))
                        exit()

    for curve in csv_dic.keys():
        data_x = csv_dic[curve].keys()
        data_x.sort()
        data_y = [csv_dic[curve][x] for x in data_x]
        for x, y in zip(data_x, data_y):
            win.add_point(curve, x, y, False)

    for curve in win.curves:
        win.curve_display(curve)

    # Test if user want socket connection
    if sock_host:
        # get ip address of host
        host = socket.gethostbyname(sock_host)
        # creat socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        thread_sock = threading.Thread(target=wait_connection,
                                       args=(sock, host, win))
        thread_sock.daemon = True
        thread_sock.start()

    win.run()

    exit()

if __name__ == '__main__':
    main()
