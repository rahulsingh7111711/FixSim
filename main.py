from fix_client import FixClient
from messages.logon import build_logon
from messages.heartbeat import build_heartbeat
from messages.new_order import build_new_order_single
import time

def print_menu():
    print("\n=== FixSim Client Menu ===")
    print("1. Send Logon")
    print("2. Send Heartbeat")
    print("3. Send New Order")
    print("4. Exit")

def main():
    client = FixClient("localhost", 9898)
    client.connect()
    seq_num = 1

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            msg = build_logon()
        elif choice == "2":
            msg = build_heartbeat(seq_num=str(seq_num))
        elif choice == "3":
            cl_ord_id = input("Enter ClOrdID (e.g., ORD1002): ")
            symbol = input("Enter Symbol (e.g., AAPL): ")
            side = input("Enter Side (1 = Buy, 2 = Sell): ")
            qty = input("Enter Quantity (e.g., 100): ")
            price = input("Enter Price (e.g., 150.00): ")
            msg = build_new_order_single(
                cl_ord_id=cl_ord_id,
                symbol=symbol,
                side=side,
                order_qty=qty,
                price=price,
                seq_num=str(seq_num),
            )
        elif choice == "4":
            print("Exiting FixSim...")
            client.disconnect()
            break
        else:
            print("❌ Invalid choice.")
            continue

        client.send_message(msg)
        seq_num += 1
        time.sleep(1)

if __name__ == "__main__":
    main()
