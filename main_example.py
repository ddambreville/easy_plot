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

import Multi_Plotter as mp
import numpy as np


def main():

    change = 0
    listx = []
    listy = []

    # definition of window's resolution
    res_X = 1920
    res_Y = 1080

    # Creation of the window from multi_plotter2.cfg configuration file,
    # and resolution defined before.
    my_window = mp.Window("multi_plotter.cfg", res_X, res_Y)

    # Creation of exemple data list, to put on figures
    # structure of a list is following:
    #[                                 Window                ]
    #[[        Figure 1       ],...,[         Figure n      ]]
    #[[[Curve 1],...,[Curve n]],...,[[Curve 1],...,[Curve n]]]

    bigX = np.linspace(0, 2 * np.pi, 1000)

    for i in range(my_window.nb_figure):
        x = []
        y = []

        for j in range(len(my_window.figure_list[i].curves_list)):
            x.append(bigX)

            if change == 0:
                y.append(np.sin(x[j]))
            else:
                y.append(np.cos(x[j]))

            change = 1 - change

        listx.append(x)
        listy.append(y)
    # -------------------------------------------------------------------------#

    # update all the window with data created before
    my_window.update_all_window(listx, listy)

    # Creation of exemple data list, to put on just one figure

    # -------------------------------------------------------------------------#
    x = []
    y = []

    for i in range(len(my_window.figure_list[3].curves_list)):
        x.append(bigX)
        y.append(np.cos(x[i]))
    # -------------------------------------------------------------------------#

    my_window.update_one_figure(x, y, 2, 2)

    my_window.run()


main()
