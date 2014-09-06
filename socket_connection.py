#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Communication protocol for easy_plot
"""

import threading


class NewConnection(object):

    """Connection protocol for easy_plot"""

    def __init__(self, sock, server=None):
        self.sock = sock
        self.dict_func = None
        self.generate_dict()

        if server is not None:
            from Queue import Queue
            self.queue = Queue(maxsize=0)
            self.first_co = True
            self.thread_client = threading.Thread(target=self.wait_client)
            self.thread_client.daemon = True
            self.thread_client.start()

    def __del__(self):
        """Destroyer"""
        self.sock.close()
        try:
            del self.queue
        except NameError:
            pass

    def generate_dict(self):
        """Generate dictionary for socket connection"""
        self.dict_func = {
            # Client functions
            "00": self.do_nothing,
            "01": self.get_data,
            "02": self.get_datas,

            # Server functions
            "11": self.send_data,
            "12": self.send_datas,
            "13": self.data_dispo
        }

    def is_data_dispo(self):
        """Send command to server to retrieve data"""
        self.sock.send("13")
        return self.dict_func[self.sock.recv(2)]()

    def do_nothing(self):
        """Do nothing"""
        return None

    def data_dispo(self):
        """Server inform that data is available"""
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
        """Receive data form server"""
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
        """server send data to client"""
        while not self.queue.empty():
            self.sock.send(','.join(self.queue.get()))
            self.sock.recv(1)
        self.sock.send("end")

    def send_datas(self):
        """Server sends curve"""
        pass

    def get_datas(self):
        """Client receive curve"""
        pass

    def add_queue(self, name, data_x, data_y):
        """Add Data in server queue"""
        try:
            self.queue.put((str(name), str(data_x), str(data_y)))
        except NameError:
            pass

    def wait_client(self):
        """Wait information from client"""
        from socket import error
        try:
            while True:
                fonc = self.sock.recv(1024)
                self.dict_func[fonc]()
        except (error, KeyError):
            # client quit
            self.__del__()
