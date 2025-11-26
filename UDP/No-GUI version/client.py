#=========================================================
#=======================Client (UDP)======================
#=========================================================
import socket
import threading

def receive(sock):
    while True:
        try:
            msg, addr = sock.recvfrom(1024)
            if not msg:
                continue
            print("[SERVER] " + msg.decode())
        except:
            break

def send(sock, server_addr):
    while True:
        msg = input("")
        sock.sendto(msg.encode(), server_addr)
        if msg.lower() == "exit":
            print("Disconnecting...")
            break

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_addr = ("127.0.0.1", 12345)

# Send initial hello to register with server
client.sendto("hello".encode(), server_addr)

threading.Thread(target=receive, args=(client,), daemon=True).start()
send(client, server_addr)
