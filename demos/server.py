import socket

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind(('127.0.0.1', 8000))
serv.listen(5)

#########
##signal handling
#######
#DOESN'T WORK!!!!!!!!!!!!
import signal
import sys
import importlib
# from demo2 import demo2
from demo3 import demo3

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
#########
########
while True:
    conn, addr = serv.accept()
    from_client=''

    while True:
        data = conn.recv(4096)
        data = data.decode()
        if not data:
            break
        from_client = data
        print(from_client)

# run demo2 from deep Disfluency
        # importlib.import_module('demo2')
        d=demo3()
        d.run()


        myStr = "I am SERVER \n"
        byt = myStr.encode()
        conn.send(byt)

    conn.close()
    print('client disconnected')
