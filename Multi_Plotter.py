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
    from pyqtgraph.Qt import QtGui, QtCore
    import pyqtgraph as pg
except:
    print "Well that's embarrassing!\nI can't find pyqtgraph on your computer.\nPlease install pyqtgraph."

import Read_cfg as rd

#========================Class Definitions=====================================


class button(object):

    """
    button class
    This class permits the gestion of button on figures
    """

    def __init__(self, layout, row, column):
        self.btn1 = QtGui.QPushButton('Autoscale: OFF')
        self.btn2 = QtGui.QPushButton('Auto Range: ON')

        self.btn1.setStyleSheet(
            "background-color:#000000; border: 2px solid #898989")
        # self.btn1.setFixedSize(100,100)

        self.btn2.setStyleSheet(
            "background-color:#000000; border: 2px solid #898989")
        # self.btn2.setFixedSize(100,100)

        self.autoScale = 0
        self.autoRange = 0

        self.timer_btn1 = QtCore.QTimer()
        self.timer_btn2 = QtCore.QTimer()

        layout.addWidget(self.btn1, row, column)
        layout.addWidget(self.btn2, row, column + 2)

    def _auto_scale_on(self):
        self.btn1.setText("Autoscale: ON")
        self.btn2.setText("Auto Range: OFF")
        self.autoScale = 1
        self.autoRange = 0

    def _auto_scale_off(self):
        self.btn1.setText("Autoscale: OFF")
        self.autoScale = 0

    def _auto_range_on(self):
        self.btn1.setText("Autoscale: OFF")
        self.btn2.setText("Auto Range: ON")
        self.autoRange = 1
        self.autoScale = 0

    def _auto_range_off(self):
        self.btn2.setText("Auto Range: OFF")
        self.autoRange = 0

    def _update(self):
        if self.autoScale == 0:
            self.btn1.clicked.connect(self._auto_scale_on)
        else:
            self.btn1.clicked.connect(self._auto_scale_off)

        if self.autoRange == 0:
            self.btn2.clicked.connect(self._auto_range_on)
        else:
            self.btn2.clicked.connect(self._auto_range_off)


class curve(object):

    """
    curve class
    This class permits the gestion of curves in figures
    """

    def __init__(self, curve_parameters_data):
        self.name = curve_parameters_data.name
        self.legend = curve_parameters_data.legend
        self.color = curve_parameters_data.color

        self.dataCloudX = [0]
        self.dataCloudY = [0]
        self.curve_plot = False

    def update_point(self, dataCloudX, dataCloudY):
        self.dataCloudX = dataCloudX
        self.dataCloudY = dataCloudY

    def show_curve(self, graph):
        if self.curve_plot == False:
            self.curve_plot = graph.plot(
                self.dataCloudX, self.dataCloudY, pen=self.color, name=self.legend)
        else:
            self.curve_plot = graph.plot(
                self.dataCloudX, self.dataCloudY, pen=self.color)


class figure(object):

    """
    figure class
    This class permits the gestion of figures in window
    """

    def __init__(self, layout, max_time, figure_parameters, curves_list):
        self.position_row = figure_parameters.row
        self.position_column = figure_parameters.column

        self.max_time = max_time

        self.title = figure_parameters.title
        self.lablX = figure_parameters.labelX
        self.unitX = figure_parameters.unitX
        self.lablY = figure_parameters.labelY
        self.unitY = figure_parameters.unitY
        self.minY = figure_parameters.minY
        self.maxY = figure_parameters.maxY
        self.gridX = figure_parameters.gridX
        self.gridY = figure_parameters.gridY

        self.curves_list = curves_list

        self.graph = pg.PlotWidget(title=self.title)
        self.graph.setYRange(self.minY, self.maxY)
        self.graph.setLabel('bottom', self.lablX, units=self.unitX)
        self.graph.setLabel('left', self.lablY, units=self.unitY)
        self.graph.showGrid(x=self.gridX, y=self.gridY)

        if len(self.curves_list) > 0:
            self.graph.addLegend()

        # self.graph.hideButtons()

        new_row = self.position_row * 2
        new_col = self.position_column * 3

        layout.addWidget(self.graph, new_row, new_col, 2, 3)
        #self.button = button(layout, new_row, new_col)

    def _action_button(self):
        if self.button.autoScale == 1:
            self.graph.enableAutoRange()
        else:
            self.graph.disableAutoRange()

        if self.button.autoRange == 1:
            if len(self.curves_list) != 0:
                self.graph.setXRange(self.curves_list[0].dataCloudX[0] - int(
                    self.max_time / 2), self.curves_list[0].dataCloudX[0] + int(self.max_time / 2))
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


class window(object):

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
                        curve(parameters.curves_parameters.curve_data[j]))

            self.figure_list.append(
                figure(self.layout, self.max_time, parameters.figures_parameters[i], curves_list))

        self.window.setLayout(self.layout)

        # for i in range(self.nb_figure):
        #     self.figure_list[i].button.timer_btn1.timeout.connect(self.figure_list[i].button._update)
        #     self.figure_list[i].button.timer_btn1.start(10)

        #     self.figure_list[i].button.timer_btn2.timeout.connect(self.figure_list[i]._action_button)
        #     self.figure_list[i].button.timer_btn2.start(10)

        self.window.show()

    def update_one_figure(self, dataListX, dataListY, row, column):
        """
        Update the figure situated on the window at (row;column) coordonate only,
        with dataListX and dataListY datas.
        """

        flag = False

        for i in range(self.nb_figure):
            if self.figure_list[i].position_row == row and self.figure_list[i].position_column == column:
                self.figure_list[i].clear_figure()
                self.figure_list[i].update_figure(dataListX, dataListY)
                flag = True

        if flag is False:
            print "ERROR: Can't Update figure at " + str(row) + "-" + str(column) + " -> Not Found"

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
