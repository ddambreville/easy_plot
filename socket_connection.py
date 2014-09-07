#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Communication protocol for easy_plot
"""

import threading
import time
import socket

DEFAULT_REFRESH_PERIOD = 0.1  # s

# Client -> Server
IS_DATA_AVAILABLE = "13"
GET_DATA = "14"

# Server -> Client
DATA_AVAILABLE = "03"
NO_DATA_AVAILABLE = "04"


class Client(object):

    """docstring for Client"""

    def __init__(self, server_ip, port, window,
                 refresh_period=DEFAULT_REFRESH_PERIOD):
        self.server_ip = server_ip
        self.port = port
        self.win = window

        # Create socket and connect to the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.connect((socket.gethostbyname(server_ip), port))

            while True:
                self.get_datas()
                time.sleep(refresh_period)

        except socket.error:
            print "ERROR : No server is found at adress " + server_ip

    def get_datas(self):
        """Retrieve datas from server"""
        while self.is_data_available():
            self.sock.send(GET_DATA)

            str_points_to_add = ""
            while str_points_to_add[-3:] != "END":
                str_points_to_add += self.sock.recv(255)

            raw_points_to_add = str_points_to_add.split(",")

            list_curves_to_refresh = []

            while len(raw_points_to_add) >= 3:
                (curve_name, str_data_x, str_data_y) = raw_points_to_add[:3]
                data_x = float(str_data_x)
                data_y = float(str_data_y)

                if curve_name not in list_curves_to_refresh:
                    list_curves_to_refresh.append(curve_name)

                raw_points_to_add.pop(0)  # Delete curve
                raw_points_to_add.pop(0)  # Delete data_x
                raw_points_to_add.pop(0)  # Delete data_y

                # Add point and don't plot
                self.win.add_point(curve_name, data_x, data_y, False)

            # Plot curves
            for curve in list_curves_to_refresh:
                self.win.curve_display(curve)

    def is_data_available(self):
        """Ask to the server is some datas are available"""
        self.sock.send(IS_DATA_AVAILABLE)
        server_answer = self.sock.recv(2)

        if server_answer == DATA_AVAILABLE:
            data_available = True
        elif server_answer == NO_DATA_AVAILABLE:
            data_available = False

        return data_available


class Server(object):

    """docstring for Server"""

    def __init__(self, port):
        self.curves = {}
        # Create socket and wait for a client connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind of the socket
        self.sock.bind(("127.0.0.1", port))

        # Specify only one client connection is allowed
        self.sock.listen(1)

        # Create thread
        thread = threading.Thread(target=self._wait_for_client)
        thread.daemon = True
        thread.start()

    def _wait_for_client(self):
        """Wait for a client to connnect"""
        client, address = self.sock.accept()

        while True:
            # print "Wait for client query"
            client_query = client.recv(2)

            if client_query == IS_DATA_AVAILABLE:
                if self.curves == {}:
                    client.send(NO_DATA_AVAILABLE)
                else:
                    client.send(DATA_AVAILABLE)

            elif client_query == GET_DATA:
                self._send_datas(client)

    def _send_datas(self, client):
        """Send available datas to the client"""
        string_to_send = ""
        for curve, datas in self.curves.items():
            for (data_x, data_y) in datas:
                string_to_send += curve + "," + str(data_x) + "," + \
                    str(data_y) + ","

        # Empty the dictionnary
        self.curves = {}

        # TODO : Find a better way to do this, because this is ugly !
        string_to_send += "END"

        client.send(string_to_send)

    def add_point(self, curve_name, data_x, data_y):
        """Public method : Add a point to plot in a curve"""
        if curve_name not in self.curves:
            self.curves[curve_name] = [(data_x, data_y)]
        else:
            self.curves[curve_name].append((data_x, data_y))
