#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2014/08/08
Last Update on 2014/08/13

Author: Renaud CARRIERE
Contact: rcarriere@presta.aldebaran-robotics.fr
Copyright: Aldebaran Robotics 2014
"""

try:
    import pyqtgraph as pg
except ImportError:
    print "Well that's embarrassing !"
    print "I can't find pyqtgraph on your computer. Please install pyqtgraph."
    print 'You can visit the section "Installation" of www.pyqtgraph.org.'
    print 'If pip is already installed on your computer, you can just type'
    print '"pip install pyqtgraph" in a command line interface.'

    exit()

from pyqtgraph.Qt import QtGui, QtCore

import read_cfg

#========================Class Definitions=====================================


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

    def __init__(self, legend, color):
        self.legend = legend
        self.color = color

        self.data_cloud_x = [0]
        self.data_cloud_y = [0]
        self.curve_plot = False

    def update_point(self, data_cloud_x, data_cloud_y):
        self.data_cloud_x = data_cloud_x
        self.data_cloud_y = data_cloud_y

    def show_curve(self, graph):
        if self.curve_plot == False:
            self.curve_plot = graph.plot(
                self.data_cloud_x, self.data_cloud_y, pen=self.color,
                name=self.legend)
        else:
            self.curve_plot = graph.plot(
                self.data_cloud_x, self.data_cloud_y, pen=self.color)


class Figure(object):

    """
    Figure class
    This class permits the gestion of figures in window
    """

    def __init__(self, layout, row, column, max_time, title, label_x, unit_x,
                 label_y, unit_y, min_y, max_y, grid_x, grid_y):

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

        self.curves = {}

        self.graph = pg.PlotWidget(title=self.title)
        self.graph.setYRange(self.min_y, self.max_y)
        self.graph.setLabel('bottom', self.label_x, units=self.unit_x)
        self.graph.setLabel('left', self.label_y, units=self.unit_y)
        self.graph.showGrid(x=self.grid_x, y=self.grid_y)

        # If there is at least one curve in the figure
        if self.curves != {}:
            self.graph.addLegend()

        # self.graph.hideButtons()

        new_row = self.row * 2
        new_col = self.column * 3

        layout.addWidget(self.graph, new_row, new_col, 2, 3)
        #self.button = button(layout, new_row, new_col)

    def _action_button(self):
        if self.button.auto_scale == 1:
            self.graph.enableAutoRange()
        else:
            self.graph.disableAutoRange()

        if self.button.auto_range == 1:
            if len(self.curves_list) != 0:
                self.graph.setXRange(self.curves_list[0].data_cloud_x[0] -
                                     int(self.max_time / 2),
                                     self.curves_list[0].data_cloud_x[0] +
                                     int(self.max_time / 2))
            else:
                self.graph.setXRange(0, self.max_time)
        else:
            pass

    def update_figure(self, dataListX, dataListY):
        for i in range(len(self.curves_list)):
            self.curves_list[i].update_point(dataListX[i], dataListY[i])
            self.curves_list[i].show_curve(self.graph)

    def clear_figure(self):
        self.graph.clear()


class Window(object):

    """
    Window class
    This class permits the gestion of all the window
    """

    def __init__(self, config_file, res_x=1920, res_y=1080):
        self.app = QtGui.QApplication([])

        parameters = read_cfg.Parameters(config_file)

        self.max_time = parameters.max_time
        self.nb_row = parameters.nb_row
        self.nb_col = parameters.nb_column
        self.nb_figure = self.nb_row * self.nb_col
        self.title = parameters.title
        self.anti_aliasing = parameters.anti_aliasing

        self.window = QtGui.QWidget()
        self.window.setStyleSheet("QWidget {background-color: #111111 }")
        self.window.resize(res_x, res_y)
        self.window.setWindowTitle(self.title)
        self.layout = QtGui.QGridLayout()
        self.figure_list = []

        pg.setConfigOptions(antialias=self.anti_aliasing)

        # A figure contains 0 or more curves
        self.figures = {}

        # A curve belong to exactly one figure
        self.curves = {}

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

        for name, curve_param in parameters.curves.items():
            curve = Curve(curve_param.legend, curve_param.color)
            self.curves[name] = curve

            curve_row = curve_param.row
            curve_column = curve_param.column

            # A curve belong to exactly one figure
            curve.figure = self.figures[(curve_row, curve_column)]

            # A figure contains 0 or more curves
            self.figures[(curve_row, curve_column)].curves[name] = curve

        self.window.setLayout(self.layout)

        self.window.show()

    def update(self, curve_name, list_x, list_y):
        self.curves[curve_name]

    def update_one_figure(self, data_list_X, dataListY, row, column):
        """
        Update the figure situated on the window at (row;column) coordonate
        only, with data_list_X and dataListY datas.
        """

        flag = False

        for i in range(self.nb_figure):
            if self.figure_list[i].position_row == row and \
                self.figure_list[i].position_column == column:
                self.figure_list[i].clear_figure()
                self.figure_list[i].update_figure(data_list_X, dataListY)
                flag = True

        if not flag:
            print "ERROR: Can't Update figure at " + str(row) + "-" + \
                str(column) + " -> Not Found"

    def update_all_window(self, dataListListX, dataListListY):
        """
        Update all figures situated on the window, with dataListListX and
        dataListListY datas.
        """

        for i in range(self.nb_figure):
            self.figure_list[i].clear_figure()
            self.figure_list[i].update_figure(
                dataListListX[i], dataListListY[i])

    def run(self):
        self.app.exec_()  # Execution of the application
