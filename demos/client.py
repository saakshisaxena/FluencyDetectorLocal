import socket

class Client:

    client = ""
    from_server = ""
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.from_server = ""

    def connect(self):
        self.client.connect(('127.0.0.1', 8000)) # host, port

    def sendData(self):
        myString = "I am CLIENT \n"
        byt = myString.encode()
        self.client.send(byt)

    def getData(self):
        self.from_server = self.client.recv(4096)
        self.from_server = self.from_server.decode()

    def closeAndPrint(self):
        self.client.close()
        print(self.from_server)
