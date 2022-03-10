import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8888)) # host, port

myString = "I am CLIENT \n"
byt = myString.encode()
client.send(byt)

from_server = client.recv(4096)
from_server = from_server.decode()

client.close()

print(from_server)
