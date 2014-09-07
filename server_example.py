#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket_connection
import math
import time


def main():
    plot_server = socket_connection.Server(4521)

    t0 = time.time()
    while True:
        current_time = time.time() - t0
        sinus = math.sin(current_time)
        plot_server.add_point("Sinus", current_time, sinus)
        time.sleep(0.1)

if __name__ == '__main__':
    main()
