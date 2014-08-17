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
import numpy as np


def main():

    # Creation of the window from multi_plotter2.cfg configuration file,
    # and resolution defined before.
    my_window = easy_plot.Window("easy_plot.cfg")

    print my_window.figures

    my_window.run()


main()
