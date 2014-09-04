#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2014/08/13

Author: Renaud CARRIERE
Contact: rcarriere@presta.aldebaran-robotics.fr
Copyright: Aldebaran Robotics 2014
"""


'''
=========================EXEMPLE FILE==========================================

This file aim to explane how to use easy_plot API with an exemple

===============================================================================
'''

import easy_plot
import time
import threading
import csv


def main():

    my_window = easy_plot.Window("easy_plot_example.cfg")

    for figure in my_window.figures.values():
        figure.pw.setXRange(0, 8)

    dic_data = csv.DictReader(open("example.csv"))
    list_time = []
    list_actuator = []
    list_sensor = []
    list_error = []
    list_actuator_p_eps = []
    list_actuator_m_eps = []
    list_eps = []
    list_m_eps = []

    for row in dic_data:
        list_time.append(float(row["Time"]))
        list_actuator.append(float(row["Actuator"]))
        list_sensor.append(float(row["Sensor"]))
        list_error.append(float(row["Error"]))
        list_actuator_p_eps.append(float(row["Actuator+Eps"]))
        list_actuator_m_eps.append(float(row["Actuator-Eps"]))
        list_eps.append(float(row["Eps"]))
        list_m_eps.append(float(row["-Eps"]))

    zipette = zip(list_time, list_actuator, list_sensor, list_error,
                  list_actuator_p_eps, list_actuator_m_eps, list_eps,
                  list_m_eps)

    def loop():
        for item in zipette:
            (x, actuator, sensor, error, act_p_e, act_m_e, eps, m_eps) = item

            my_window.add_point("Actuator", x, actuator)
            my_window.add_point("Sensor", x, sensor)
            my_window.add_point("Actuator+Eps", x, act_p_e)
            my_window.add_point("Actuator-Eps", x, act_m_e)
            my_window.add_point("Error", x, error)
            my_window.add_point("Eps", x, eps)
            my_window.add_point("-Eps", x, m_eps)

            time.sleep(0.01)

    logThread = threading.Thread(target=loop)
    logThread.daemon = True
    logThread.start()

    my_window.run()

main()
