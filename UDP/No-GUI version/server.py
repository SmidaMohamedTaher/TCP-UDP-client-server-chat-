#=========================================================
#======================Server (UDP)========================
#=========================================================
import socket as sk
import threading

clients = set()   # store (ip, port)

def receive(server):
    while True:
        try:
            data, addr = server.recvfrom(1024)

            if addr not in clients:
                clients.add(addr)
                print("New client:", addr)
                server.sendto("you are connected with the server now ...".encode(), addr)

            message = data.decode()

            if message.lower() == "exit":
                print("Client requested disconnect:", addr)
                clients.discard(addr)
                continue

            print(f"[CLIENT {addr}] {message}")

        except Exception as e:
            print("Error:", e)
            break

def send(server):
    while True:
        msg = input("")
        for c in clients:
            server.sendto(msg.encode(), c)

# ================= Main ================
host = "127.0.0.1"
port = 12345

server = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
server.bind((host, port))

print("UDP server running on port", port)

threading.Thread(target=receive, args=(server,), daemon=True).start()
send(server)
