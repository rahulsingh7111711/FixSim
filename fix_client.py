import socket
import threading
from fix_parser import parse_fix_message
from fix_utils import SOH

class FixClient:
    def __init__(self, host='localhost', port=9898):
        self.host = host
        self.port = port
        self.sock = None
        self.running = False

    def connect(self):
        """Establish TCP connection to server"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.running = True
        print(f"Connected to {self.host}:{self.port}")

        # Start listening to server
        thread = threading.Thread(target=self.receive_messages, daemon=True)
        thread.start()

    def send_message(self, message: str):
        """Send FIX message to server"""
        print(f"-> Sending: {message.replace(SOH, '|')}")
        self.sock.sendall(message.encode())

    def receive_messages(self):
        """Listen and parse incoming FIX messages"""
        buffer = ""
        while self.running:
            data = self.sock.recv(1024)
            if not data:
                break
            buffer += data.decode()
            
            # Process complete FIX messages
            while SOH + "10=" in buffer:
                # Assume message ends with 10=XXX<SOH>
                end_index = buffer.find(SOH + "10=")
                if end_index == -1 or len(buffer) < end_index + 7:
                    break
                end = buffer.find(SOH, end_index + 4)
                if end == -1:
                    break

                full_msg = buffer[:end + 1]
                buffer = buffer[end + 1:]
                parsed = parse_fix_message(full_msg)
                print(f"<- Received: {parsed}")

    def disconnect(self):
        """Close the connection"""
        self.running = False
        if self.sock:
            self.sock.close()
            print("Disconnected.")
