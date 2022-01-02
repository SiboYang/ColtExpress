import socket


class Network:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ""
        self.port = 5555
        self.serveraddr = (self.server, self.port)
        self.id = self.connect()

    def connect(self):
        try:
            self.socket.connect(self.serveraddr)
            return self.socket.recv(1048)
        except:
            print("Connection failed!")
            pass

    def send(self, data):
        try:
            self.socket.sendall(data)
            return self.socket.recv(1048)
        except socket.error as e:
            print(e)
