#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Communication protocol for easy_plot

Last Update on 2014/09/12

Author:  Jason LETORT
         Emmanuel NALEPA
         Renaud CARRIERE
Contact: jletort@presta.aldebaran-robotics.fr
         enalepa@aldebaran.com
         rcarriere@aldebaran.com
Copyright: Aldebaran Robotics 2014
@pep8 : Complains without rules R0902, R0912, R0913, R0914, R0915 and W0212
"""

import threading
import time
import socket
import sys


def str2Network(s):
    '''Transform string to network format (python v2=str, v3=bytearray)'''
    if sys.version_info >= (3, 0):
        return bytearray(s, 'utf-8')
    return s

DEFAULT_REFRESH_PERIOD = 0.1  # s
# TODO : Find a way to specify the DEFAULT_PORT only one time
DEFAULT_PORT = 4521

# Client -> Server
IS_DATA_AVAILABLE = str2Network("00")
GET_DATA = str2Network("01")

TRY_LOST_CONNEXION = 10
TIME_BETWEEN_TRY = 2  # s

# Server -> Client
DATA_AVAILABLE = str2Network("10")
NO_DATA_AVAILABLE = str2Network("11")
ERASE_CURVES = str2Network("12")


class Client(object):

    """docstring for Client"""

    def __init__(self, window, server_ip, port=DEFAULT_PORT,
                 refresh_period=DEFAULT_REFRESH_PERIOD):
        self.server_ip = server_ip
        self.port = port
        self.win = window

        # Create socket and connect to the server

        cpt = 0
        continu = True
        flag = True
        flag_print = True

        while continu:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                if flag is True:
                    self.sock.connect((socket.gethostbyname(server_ip), port))
                    print(" Connexion OK")
                    flag_print = True
                    flag = False

                while True:
                    self.get_datas()
                    cpt = 0
                    time.sleep(refresh_period)

            except (socket.error, BaseException):
                if flag_print is True:
                    sys.stdout.write(
                        "Try to connect with " + server_ip + " ")
                    flag_print = False
                cpt += 1

                if cpt <= TRY_LOST_CONNEXION:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    flag = True
                    time.sleep(TIME_BETWEEN_TRY)
                else:
                    print(" TIME OUT")
                    continu = False

    def get_datas(self):
        """Retrieve datas from server"""

        if self.is_data_available():
            self.sock.send(GET_DATA)

            str_points_to_add = ""
            while str_points_to_add[-3:] not in ("END", "RAZ"):
                str_points_to_add += self.sock.recv(1024)

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

            # Test if curves have to be erased
            if raw_points_to_add[-1] == "RAZ":
                self.win.curves_erase()

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
        elif server_answer == ERASE_CURVES:
            self.win.curves_erase()
            data_available = False

        return data_available


class Server(object):

    """docstring for Server"""

    def __init__(self, port=DEFAULT_PORT, local_plot=False, max_points=100000):
        # Contains the datas not yet plotted
        self.curves = {}
        self.max_points = max_points

        # Set to True if the server wants to erase all curves
        self.has_to_erase_curves = False

        # Create socket and wait for a client connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Get the ip adress

        self.hostname = socket.gethostname()

        if local_plot is True:
            self.ip_adress = "127.0.0.1"
        else:
            try:
                try:
                    self.ip_adress = socket.gethostbyname(
                        self.hostname + ".local")
                except socket.gaierror:
                    self.ip_adress = socket.gethostbyname(self.hostname)
            except socket.gaierror:
                print("ERROR: Impossible to get host with " + self.hostname)
                print("       or " + self.hostname + ".local")
                exit()

        print (self.hostname + " send datas at " + self.ip_adress)

        # Bind of the socket
        self.sock.bind((self.ip_adress, port))

        # Specify only one client connection is allowed
        self.sock.listen(1)

        # Create thread
        thread = threading.Thread(target=self._wait_for_client)
        thread.daemon = True
        thread.start()

    def _wait_for_client(self):
        """Wait for a client to connnect"""
        while True:
            # sock.accept return a tuple of 2 elements.
            # Only the first one is usefull
            client = self.sock.accept()[0]
            self._client_state_machine(client)

    def _is_data_available(self, client):
        """Check if some datas are ready to be sent to the client"""
        # If the dictionnary id empty, there is no data to snd
        if self.curves == {}:
            client.send(NO_DATA_AVAILABLE)
        # In the contrary, there is data to send
        else:
            client.send(DATA_AVAILABLE)

    def _client_state_machine(self, client):
        """Engage the client state machine"""
        client_problem = False
        while not client_problem:
            client_query = client.recv(2)

            if client_query == IS_DATA_AVAILABLE:
                self._is_data_available(client)
            elif client_query == GET_DATA:
                self._send_datas(client)
            # If client is dead, the function client.recv will return a empty
            # string. In this case, the state machine stop, and the server is
            # waiting for another client.
            else:
                client_problem = True

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
        if self.has_to_erase_curves:
            self.has_to_erase_curves = False
            string_to_send += "RAZ"
        else:
            string_to_send += "END"

        client.send(str2Network(string_to_send))

    def add_point(self, curve_name, data_x, data_y):
        """Public method : Add a point to plot in a curve"""
        if curve_name not in self.curves:
            self.curves[curve_name] = [(data_x, data_y)]
        else:
            self.curves[curve_name].append((data_x, data_y))
            self.curves_limitation()

    def add_list_point(self, time_elapsed, list_tuple_data):
        """
        Public method: multi add_point use.
        list_tuple_data = list of (headerName, data)
        """
        [self.add_point(x[0], time_elapsed, x[1]) for x in list_tuple_data]


    def curves_erase(self):
        """Erase all curves"""
        self.has_to_erase_curves = True

    def curves_limitation(self):
        """Limit number of points to save RAM"""
        for keys in self.curves.keys():
            if len(self.curves[keys]) > self.max_points:
                self.curves[keys].pop(0)
