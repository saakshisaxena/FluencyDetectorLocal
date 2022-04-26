import socket
import importlib
from tagAndAnalyze import tagAndAnalyze

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind(('127.0.0.1', 8000)) # keep the port number same for server and client
serv.listen(5)

while True:
    conn, addr = serv.accept()
    from_client=''

    # keep the connection open for other requests while handling one request from client
    while True:
        data = conn.recv(4096)
        data = data.decode()
        if not data:
            break
        from_client = data
        print(from_client)

        # run tagger and Analyzer code that uses Deep Disfluency Library
        d=tagAndAnalyze()
        d.run()

        myStr = "msg : Done \n -From server \n"
        byt = myStr.encode() # send the finish message back to the client
        conn.send(byt)

    conn.close()
    print('client disconnected')
