import socket
import threading
import tkinter as tk
from tkinter import scrolledtext



def create_client_window(conn, addr):

    try:
        client_name = conn.recv(1024).decode()
    except:
        client_name = str(addr)

    window = tk.Toplevel()
    window.title(f"Client {client_name}")
    window.geometry("400x500")

    chat_box = scrolledtext.ScrolledText(window, state='disabled', wrap=tk.WORD) # the box of each massege
    chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    message_entry = tk.Entry(window)
    message_entry.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.X, expand=True)

    def append_message(msg):
        chat_box.config(state='normal')
        chat_box.insert(tk.END, msg + "\n")
        chat_box.config(state='disabled')
        chat_box.yview(tk.END)

  
    def receive():
        while True:
            try:
                msg = conn.recv(1024).decode()
                if msg:
                    append_message(f"[CLIENT] {msg}")
                if msg.lower() == "exit":
                    append_message("Client disconnected")
                    conn.close()
                    break
            except:
                append_message("Client disconnected unexpectedly")
                break

  
    def send_message(event=None):
        msg = message_entry.get()
        if msg.strip() != "":
            try:
                conn.send(msg.encode())
                append_message(f"[YOU] {msg}")
            except:
                append_message("Failed to send message")
            message_entry.delete(0, tk.END)
            if msg.lower() == "exit":
                conn.close()
                window.destroy()

    send_button = tk.Button(window, text="Send", command=send_message)
    send_button.pack(padx=10, pady=10, side=tk.RIGHT)
    message_entry.bind("<Return>", send_message)# in the case of user using the enter key the app send the massege

    threading.Thread(target=receive, daemon=True).start()


def accept_clients():
    while True:
        conn, addr = server.accept()
        print(f"New client connected: {addr}")
        create_client_window(conn, addr)


##============================ Main ======================

host = "127.0.0.1"
port = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
print(f"Server listening on {host}:{port}")

root = tk.Tk()
root.title("Server Chat")
root.geometry("300x100")

label = tk.Label(root, text="Server is running...\nWaiting for clients...", font=("Arial", 12))
label.pack(padx=10, pady=10)

threading.Thread(target=accept_clients, daemon=True).start()

root.mainloop()
