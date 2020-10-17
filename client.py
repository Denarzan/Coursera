import socket
import time

"""Client for sending metrics"""


class ClientError(Exception):
    pass


class Client:

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((self.host, self.port), self.timeout)  # creating new socket

    def put(self, metric, value, timestamp=None):
        timestamp = timestamp or int(time.time())  # time when the measurement was taken
        try:  # <command> <request data> <\n>
            self.sock.sendall("put {} {} {}\n".format(metric, value, timestamp).encode("utf-8"))  # sending data
        except (Exception, socket.error):
            raise ClientError
        self.read()

    def get(self, metric):
        try:
            try:
                self.sock.sendall("get {}\n".format(metric).encode("utf-8"))  # sending data
            except (Exception, socket.error):
                raise ClientError
            response_data = self.read()
            data = {}
            if response_data == "":  # if empty data
                return data
            for row in response_data.split("\n"):
                key, value, timestamp = row.split()  # splitting data to metric, value and timestamp
                if key not in data:  # if metric is not on server
                    data[key] = []
                data[key].append((int(timestamp), float(value)))  # adding timestamp and value to metric
                data[key].sort(key=lambda tup: tup[0])  # sorting by timestamp
            return data
        except ValueError:
            raise ClientError

    def read(self):
        try:
            data = b""  # encoding data
            while not data.endswith(b"\n\n"):  # check if the date is not over
                try:
                    data += self.sock.recv(1024)  # taking data from server
                except (Exception, socket.error):
                    raise ClientError
            decoded_data = data.decode()  # decoding data
            status, response_data = decoded_data.split("\n", 1)  # splitting by \n
            response_data = response_data.strip()
            if status != "ok":  # if bad data from server
                raise ClientError
            return response_data
        except ValueError:
            raise ClientError
