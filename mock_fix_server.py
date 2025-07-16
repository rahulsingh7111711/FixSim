import socket
import threading
from fix_parser import parse_fix_message
from fix_utils import SOH, get_utc_timestamp
from fix_parser import build_fix_message

HOST = 'localhost'
PORT = 9898

def handle_client(conn, addr):
    print(f"🔌 Connected by {addr}")
    buffer = ""
    while True:
        data = conn.recv(1024)
        if not data:
            break
        buffer += data.decode()

        while SOH + "10=" in buffer:
            end_index = buffer.find(SOH + "10=")
            if end_index == -1 or len(buffer) < end_index + 7:
                break
            end = buffer.find(SOH, end_index + 4)
            if end == -1:
                break

            full_msg = buffer[:end + 1]
            buffer = buffer[end + 1:]

            parsed = parse_fix_message(full_msg)
            print(f"📥 Received: {parsed}")

            msg_type = parsed.get("35")

            if msg_type == "A":  # Logon
                response = build_fix_message([
                    ("35", "A"),
                    ("34", parsed.get("34", "1")),
                    ("49", parsed.get("56")),
                    ("56", parsed.get("49")),
                    ("52", get_utc_timestamp()),
                    ("98", "0"),
                    ("108", "30"),
                ])
                conn.sendall(response.encode())
            elif msg_type == "0":  # Heartbeat
                print("💓 Heartbeat received.")
            elif msg_type == "D":  # NewOrderSingle
                response = build_fix_message([
                    ("35", "8"),  # Execution Report
                    ("34", parsed.get("34", "2")),
                    ("49", parsed.get("56")),
                    ("56", parsed.get("49")),
                    ("52", get_utc_timestamp()),
                    ("11", parsed.get("11")),  # ClOrdID
                    ("17", "EX12345"),  # ExecID
                    ("150", "0"),  # ExecType (0 = New)
                    ("39", "0"),   # OrdStatus (0 = New)
                    ("55", parsed.get("55")),  # Symbol
                    ("54", parsed.get("54")),  # Side
                    ("38", parsed.get("38")),  # OrderQty
                    ("44", parsed.get("44")),  # Price
                ])
                conn.sendall(response.encode())
                print("✅ Sent execution report.")

    conn.close()
    print(f"❌ Connection closed: {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"🚀 Mock FIX Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
