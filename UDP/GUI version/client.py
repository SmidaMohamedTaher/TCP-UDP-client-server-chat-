import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import time 

server_addr = ("127.0.0.1", 12345)
#########################################################
sended_message = 0
acsept_massage = 0
timeout = 2
start = 0
conter = 0
#########################################################
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(timeout)
client_name = input("Enter your name: ")
client.sendto(client_name.encode(), server_addr)

root = tk.Tk()
root.title(client_name)
root.geometry("400x500")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

message_entry = tk.Entry(root, width=30)
message_entry.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.X, expand=True)

def append_message(msg):
    chat_box.config(state='normal')
    chat_box.insert(tk.END, msg + "\n")
    chat_box.config(state='disabled')
    chat_box.yview(tk.END)

def receive():
    global start
    global conter
    global acsept_massage
    while True:
        try:
            msg, _ = client.recvfrom(1024)
            msg = msg.decode()
            if msg == "ok[massege]":
                end = time.time()
                acsept_massage += 1
                print(f"the Latency = {(end-start)*1000} ms")
            else:
                if msg.lower() == "exit":
                    msg = "you are not connected with the server \n if you want to reconnect , enter your name"
                append_message("[SERVER] " + msg)  
            #################################################################
        except socket.timeout:
            continue
           

def send_message(event=None):
    global sended_message
    global start
    msg = message_entry.get()
    if msg.strip() != "":
        start = time.time()
        client.sendto(msg.encode(), server_addr)
        sended_message += 1 
        append_message("[YOU] " + msg)
        message_entry.delete(0, tk.END)
        ###########################################################
        ############################################################
        if msg.lower() == "exit":
            print(f"Packet Loss average = {((sended_message - acsept_massage)*100)/sended_message}%")
            root.quit()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=10, side=tk.RIGHT)
message_entry.bind("<Return>", send_message)

threading.Thread(target=receive, daemon=True).start()

root.mainloop()
