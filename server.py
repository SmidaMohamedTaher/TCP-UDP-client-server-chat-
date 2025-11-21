import socket as sk 
import sys
import threading

def clientCon(conn,addr):
    print("we connected now with teh client "+str(addr))
    conn.send("you are connected with the server now ...".encode())
    while True:
        data = conn.recv(1024)
        if not data:
            print("the client disconnected:",addr)
            break
        print("client"+str(addr)+" : ",data.decode())
    conn.close()



host = "127.0.0.1"
port = 12345

server = sk.socket(sk.AF_INET,sk.SOCK_STREAM)

try:
    server.bind((host,port))
    server.listen(5)
    print("the server is openning now in the port ",port)
except Exception as e:
    print("server has an error ",e)
    sys.exit(0)


while True:
    conn,addr = server.accept()
    threading.Thread(target=clientCon, args=(conn, addr)).start()

