#=========================================================
#======================server=============================
#=========================================================
import socket as sk 
import sys
import threading

def receive(conn,addr):

    print("we connected now with teh client "+str(addr))
    conn.send("you are connected with the server now ...".encode())
    while True:
        try:

            data = conn.recv(1024)
            if not data:
                continue
            
            message = data.decode()
            if message.lower() == "exit":
                print("Client requested disconnect:", addr)
                break
            print(f"[CLIENT {addr}] {message}")
        except:
            print("the client disconected suddenly:", addr)
            break
    conn.close()

def send(conn):
    
    while True:
        msg = input("")
        conn.send(msg.encode())

def clientCon(conn,addr):

    threading.Thread(target=receive,args=(conn,addr), daemon=True).start()
    threading.Thread(target=send,args=(conn,), daemon=True).start()





# ============Main part ===============
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
    threading.Thread(target=clientCon, args=(conn, addr), daemon=True).start()

