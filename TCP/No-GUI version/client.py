#=========================================================
#=======================Client============================
#=========================================================
import socket
import threading

def receive(sock):

    while True:
        try:
            msg = sock.recv(1024)
            if not msg:
                continue
            print("[SERVER] " + msg.decode())
        except:
            break

def send(sock):

    while True:
        msg = input("")
        if msg.lower() == "exit":
            client.send(msg.encode())
            print("Disconnecting from server...")
            client.close()
        else:
            sock.send(msg.encode())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))



threading.Thread(target=receive, args=(client,), daemon=True).start()
send(client)