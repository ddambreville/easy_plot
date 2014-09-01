#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Communication protocol for easy_plot
"""

import threading


class NewConnection(object):

    """connection protocol for easy_plot"""

    def __init__(self, sock, serveur=None):
        super(NewConnection, self).__init__()
        self.sock = sock
        self.dico_fonc = None
        self.generate_dico()

        if serveur is not None:
            from Queue import Queue
            self.queue = Queue(maxsize=0)
            self.first_co = True
            self.thread_client = threading.Thread(target=self.wait_client)
            self.thread_client.daemon = True
            self.thread_client.start()

    def __del__(self):
        """destructeur"""
        self.sock.close()
        try:
            del self.queue
        except NameError:
            pass

    def generate_dico(self):
        """generate dico for socket connection"""
        self.dico_fonc = {
            # client fonctions
            "00": self.do_notthing,
            "01": self.get_data,
            "02": self.get_datas,

            # serveur fonctions
            "11": self.send_data,
            "12": self.send_datas,
            "13": self.data_dispo
        }

    def is_data_dispo(self):
        """send command to serveur to retrieve data"""
        self.sock.send("13")
        return self.dico_fonc[self.sock.recv(2)]()

    def do_notthing(self):
        """ pass """
        return None

    def data_dispo(self):
        """serveur inform that data is dispo"""
        if self.first_co:
            # send datas
            self.first_co = False
            self.sock.send("02")
        elif self.queue.empty():
            # send data
            self.sock.send("00")
        else:
            # do nothing
            self.sock.send("01")

    def get_data(self):
        """receve data form serveur"""
        answer_list = []
        answer = ""
        self.sock.send("11")
        while answer != "end":
            answer = self.sock.recv(1024)
            if answer != "end":
                answer_list.append(answer.split(','))
                self.sock.send('1')
        return answer_list

    def send_data(self):
        """serveur send data to client"""
        while not self.queue.empty():
            self.sock.send(','.join(self.queue.get()))
            self.sock.recv(1)
        self.sock.send("end")

    def send_datas(self):
        """serveur send curve"""
        pass

    def get_datas(self):
        """client receve curve"""
        pass

    def add_queue(self, name, data_x, data_y):
        """add Data in serveur queue"""
        self.queue.put((str(name), str(data_x), str(data_y)))

    def wait_client(self):
        """Wait information from client"""
        from socket import error
        try:
            while True:
                fonc = self.sock.recv(1024)
                self.dico_fonc[fonc]()
        except (error, KeyError):
            # client quit
            self.__del__()
