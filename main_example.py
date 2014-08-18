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
import math


def main():

    my_window = easy_plot.Window("easy_plot.cfg")

    def loop():
        time.sleep(1)
        t0 = time.time()

        while(True):
            t = time.time() - t0
            y = math.cos(t)
            my_window.add_point("Courbe1", t, y)
            my_window.add_point("Courbe2", t, -y)
            my_window.add_point("Courbe3", t, -y)

            time.sleep(0.05)

    logThread = threading.Thread(target=loop)
    logThread.daemon = True
    logThread.start()

    my_window.run()

main()
