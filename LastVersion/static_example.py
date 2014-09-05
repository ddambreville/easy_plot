#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2014/09/05

Author: Renaud CARRIERE
Contact: rcarriere@aldebaran.com
Copyright: Aldebaran Robotics 2014

=========================EXEMPLE FILE==========================================

This file aim to explane how to use easy_plot in static API with an exemple

Note : The program here do the same as
                     pyhton easy_plot.py example.csv -p

===============================================================================
"""

import easy_plot
import csv

CONFIG_FILE = "easy_plot.cfg"
DATAS_FILE = "example.csv"
ABSCISSA = "Time"


def main():
    """MAIN"""

    # Create the window (Note : we create here a full printable window)
    # Note: if res_x and res_y are not specified, the default resolution
    #       is 1920 x 1080
    my_window = easy_plot.Window(
        config_file=CONFIG_FILE, res_x=1200, res_y=800, printable=True)

    # Read CSV file
    dic_data = csv.DictReader(open(DATAS_FILE))

    # Extrate curves data from CSV file
    for row in dic_data:
        data_x = float(row[ABSCISSA])

        for curve_name, value in row.items():
            data_y = float(value)

            # Add data points
            my_window.add_point(curve_name, data_x, data_y, False)

    # Display curves
    for curve in my_window.curves:
        my_window.curve_display(curve)

    # Run application
    my_window.run()

main()
