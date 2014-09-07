#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket_connection
import math
import time


def main():
    plot_server = socket_connection.Server(4521)

    time_init = time.time()
    while True:
        elapse_time = time.time() - time_init
        if elapse_time <= 10:
            sinus = math.sin(elapse_time)
            plot_server.add_point("Sinus", elapse_time, sinus)
            time.sleep(0.1)
        else:
            time_init = time.time()
            plot_server.curves_erase()

if __name__ == '__main__':
    main()
