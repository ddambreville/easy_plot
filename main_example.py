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

This file aim to explane how to use multi_plotter API with an exemple

===============================================================================
'''

import easy_plot
import time
import threading
import csv


def main():

    my_window = easy_plot.Window("easy_plot.cfg")
    for figure in my_window.figures.values():
        figure.pw.setXRange(0, 20)

    dic_data = csv.DictReader(open("RWristYaw.csv"))

    def loop():
        for row in dic_data:
            x = float(row["Time"])

            for key, value in row.items():
                if key != "Time":
                    y = float(value)
                    my_window.add_point(key, x, y)

            time.sleep(0.2)

    logThread = threading.Thread(target=loop)
    logThread.daemon = True
    logThread.start()

    my_window.run()

main()
