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

import Read_cfg as rd

#========================Class Definitions=====================================


class button(object):

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

    def __init__(self, curve_parameters_data):
        self.name = curve_parameters_data.name
        self.legend = curve_parameters_data.legend
        self.color = curve_parameters_data.color

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

    def __init__(self, layout, max_time, figure_parameters, curves_list):
        self.position_row = figure_parameters.row
        self.position_column = figure_parameters.column

        self.max_time = max_time

        self.title = figure_parameters.title
        self.label_x = figure_parameters.labelX
        self.unit_x = figure_parameters.unitX
        self.label_y = figure_parameters.labelY
        self.unit_y = figure_parameters.unitY
        self.min_y = figure_parameters.minY
        self.max_y = figure_parameters.maxY
        self.grid_x = figure_parameters.gridX
        self.grid_y = figure_parameters.gridY

        self.curves_list = curves_list

        self.graph = pg.PlotWidget(title=self.title)
        self.graph.setYRange(self.min_y, self.max_y)
        self.graph.setLabel('bottom', self.label_x, units=self.unit_x)
        self.graph.setLabel('left', self.label_y, units=self.unit_y)
        self.graph.showGrid(x=self.grid_x, y=self.grid_y)

        if len(self.curves_list) > 0:
            self.graph.addLegend()

        # self.graph.hideButtons()

        new_row = self.position_row * 2
        new_col = self.position_column * 3

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
    window class
    This class permits the gestion of all the window
    """

    def __init__(self, configs_file, resX, resY):

        self.app = QtGui.QApplication([])

        parameters = rd.defineParameters(configs_file)

        self.max_time = parameters.general_parameters.max_time
        self.nb_row = parameters.general_parameters.number_of_rows
        self.nb_col = parameters.general_parameters.number_of_columns
        self.nb_figure = self.nb_row * self.nb_col
        self.title = parameters.general_parameters.title
        self.anti_aliasing = parameters.general_parameters.anti_aliasing

        self.window = QtGui.QWidget()
        self.window.setStyleSheet("QWidget {background-color: #111111 }")
        self.window.resize(resX, resY)
        self.window.setWindowTitle(self.title)
        self.layout = QtGui.QGridLayout()
        self.figure_list = []

        pg.setConfigOptions(antialias=self.anti_aliasing)

        for i in range(self.nb_figure):

            curves_list = []

            for j in range(parameters.curves_parameters.number_of_curves):
                if (int(parameters.figures_parameters[i].row) == int(parameters.curves_parameters.curve_data[j].row)) and (int(parameters.figures_parameters[i].column) == int(parameters.curves_parameters.curve_data[j].column)):
                    curves_list.append(
                        Curve(parameters.curves_parameters.curve_data[j]))

            self.figure_list.append(Figure(self.layout, self.max_time,
                                           parameters.figures_parameters[i],
                                           curves_list))

        self.window.setLayout(self.layout)

        self.window.show()

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
