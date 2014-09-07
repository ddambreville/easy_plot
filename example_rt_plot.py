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
"""

import socket_connection
import math
import time


def main():
    """Plot sinus, cosinus, droite, square and erase them every 10 seconds"""
    plot_server = socket_connection.Server(4521)

    time_init = time.time()
    while True:
        elapsed_time = time.time() - time_init
        if elapsed_time <= 10:

            sinus = math.sin(elapsed_time)
            cosinus = math.cos(elapsed_time)
            droite = 2 * elapsed_time - 4
            square = elapsed_time ** 2

            plot_server.add_point("Sinus", elapsed_time, sinus)
            plot_server.add_point("Cosinus", elapsed_time, cosinus)
            plot_server.add_point("Droite", elapsed_time, droite)
            plot_server.add_point("Square", elapsed_time, square)

            time.sleep(0.1)
        else:
            time_init = time.time()
            plot_server.curves_erase()

if __name__ == '__main__':
    main()
