import tkinter as tk
from tkinter import scrolledtext, messagebox
from fix_client import FixClient
from messages.logon import build_logon
from messages.heartbeat import build_heartbeat
from messages.new_order import build_new_order_single
import threading
import time

class FixSimGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("FixSim GUI Client")
        self.client = None
        self.seq_num = 1

        # UI Layout
        self.connect_btn = tk.Button(master, text="Connect", command=self.connect)
        self.connect_btn.grid(row=0, column=0, padx=10, pady=10)

        self.logon_btn = tk.Button(master, text="Send Logon", command=self.send_logon)
        self.logon_btn.grid(row=1, column=0, padx=10, pady=5)

        self.heartbeat_btn = tk.Button(master, text="Send Heartbeat", command=self.send_heartbeat)
        self.heartbeat_btn.grid(row=2, column=0, padx=10, pady=5)

        self.order_btn = tk.Button(master, text="Send New Order", command=self.send_order)
        self.order_btn.grid(row=3, column=0, padx=10, pady=5)

        self.output = scrolledtext.ScrolledText(master, width=70, height=20)
        self.output.grid(row=0, column=1, rowspan=10, padx=10, pady=10)

    def connect(self):
        self.client = FixClient()
        self.client.connect()
        self.log("✅ Connected to FIX server.")

        # Start listener thread
        threading.Thread(target=self.receive_loop, daemon=True).start()

    def send_logon(self):
        msg = build_logon()
        self.client.send_message(msg)
        self.log("📤 Sent Logon")
        self.seq_num += 1

    def send_heartbeat(self):
        msg = build_heartbeat(seq_num=str(self.seq_num))
        self.client.send_message(msg)
        self.log("💓 Sent Heartbeat")
        self.seq_num += 1

    def send_order(self):
        cl_ord_id = "GUIORD" + str(int(time.time()))
        msg = build_new_order_single(
            cl_ord_id=cl_ord_id,
            symbol="AAPL",
            side="1",
            order_qty="50",
            price="190.00",
            seq_num=str(self.seq_num),
        )
        self.client.send_message(msg)
        self.log(f"📦 Sent New Order: {cl_ord_id}")
        self.seq_num += 1

    def receive_loop(self):
        while self.client and self.client.running:
            time.sleep(0.5)  # Let fix_client.py print parsed responses
            # You could expand this to get parsed data from client if needed.

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = FixSimGUI(root)
    root.mainloop()
