import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

clients = {}  

def create_client_window(client_addr, client_name):

    window = tk.Toplevel()
    window.title(f"Client {client_name}")
    window.geometry("400x500")

    chat_box = scrolledtext.ScrolledText(window, state='disabled', wrap=tk.WORD)
    chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    message_entry = tk.Entry(window)
    message_entry.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.X, expand=True)

    def append_message(msg):
        chat_box.config(state='normal')
        chat_box.insert(tk.END, msg + "\n")
        chat_box.config(state='disabled')
        chat_box.yview(tk.END)
        

    def send_message(event=None):
        msg = message_entry.get()
        if msg.strip() != "":
            server.sendto(msg.encode(), client_addr)
            append_message(f"[YOU] {msg}")
            message_entry.delete(0, tk.END)
            if msg.lower() == "exit":
                window.destroy()
                del clients[client_addr]

    send_button = tk.Button(window, text="Send", command=send_message)
    send_button.pack(padx=10, pady=10, side=tk.RIGHT)
    message_entry.bind("<Return>", send_message)

    return append_message


# ================================================================
#                   UDP Server Listener Thread
# ================================================================
def receive_messages():
    while True:
        msg, addr = server.recvfrom(1024)

        msg = msg.decode()

        if addr not in clients:
            clients[addr] = {
                "name": msg,
                "append": create_client_window(addr, msg)
            }
            continue

        append = clients[addr]["append"]
        if msg.lower() == "exit" :
            msg = "Client disconnected"
            del clients[addr]
        append(f"[CLIENT] {msg}")


# ================================================================
#                           Main Server
# ================================================================
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 12345))

print("UDP Server running...")

root = tk.Tk()
root.title("UDP Server Chat")
root.geometry("300x100")

label = tk.Label(root, text="Server is running...\nWaiting for clients...", font=("Arial", 12))
label.pack(padx=10, pady=10)

threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
