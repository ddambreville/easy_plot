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


=========================EXEMPLE FILE==========================================

This file aim to explane how to use easy_plot API in dynamic with an exemple

===============================================================================
"""

import easy_plot
import time
import threading
import csv


def main():
    """MAIN"""

    # Create the window
    my_window = easy_plot.Window(config_file="easy_plot_example.cfg")

    # Set X range for all figures in the window
    for figure in my_window.figures.values():
        figure.plot_widget.setXRange(0, 8)

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
        """Thread loop for real time"""

        # add data points one by one
        for item in zipette:
            (data_x, actuator, sensor, error,
             act_p_e, act_m_e, eps, m_eps) = item

            my_window.add_point("Actuator", data_x, actuator)
            my_window.add_point("Sensor", data_x, sensor)
            my_window.add_point("Actuator+Eps", data_x, act_p_e)
            my_window.add_point("Actuator-Eps", data_x, act_m_e)
            my_window.add_point("Error", data_x, error)
            my_window.add_point("Eps", data_x, eps)
            my_window.add_point("-Eps", data_x, m_eps)

            time.sleep(0.01)

    log_thread = threading.Thread(target=loop)
    log_thread.daemon = True
    log_thread.start()

    # Run application
    my_window.run()

main()
