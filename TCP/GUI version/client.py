import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

# ===== إعداد الاتصال بالـ Server =====
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(("127.0.0.1", 12345))
except:
    print("Cannot connect to server")
    exit()

# ===== إنشاء واجهة Tkinter =====
root = tk.Tk()
root.title("Chat GUI")
root.geometry("400x500")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

message_entry = tk.Entry(root, width=30)
message_entry.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.X, expand=True)

# ===== دوال =====
def append_message(msg):
    chat_box.config(state='normal')
    chat_box.insert(tk.END, msg + "\n")
    chat_box.config(state='disabled')
    chat_box.yview(tk.END)

def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg:
                append_message("[SERVER] " + msg)
        except:
            append_message("Disconnected from server")
            break

def send_message(event=None):
    msg = message_entry.get()
    if msg.strip() != "":
        client.send(msg.encode())
        append_message("[YOU] " + msg)
        message_entry.delete(0, tk.END)
        if msg.lower() == "exit":
            client.close()
            root.quit()

send_button = tk.Button(root, text="إرسال", command=send_message)
send_button.pack(padx=10, pady=10, side=tk.RIGHT)

message_entry.bind("<Return>", send_message)

# ===== بدء Thread استقبال الرسائل =====
threading.Thread(target=receive, daemon=True).start()

root.mainloop()
