# fix_gui_web.py

import streamlit as st
from fix_client import FixClient
from logon import build_logon
from heartbeat import build_heartbeat
from new_order import build_new_order

st.set_page_config(page_title="FixSim GUI", layout="wide")
st.title("🔁 FixSim – FIX Client Emulator")

# --- Session State for Client ---
if 'client' not in st.session_state:
    st.session_state.client = FixClient('localhost', 5001)

client = st.session_state.client

# --- Connection ---
if st.button("🔌 Connect"):
    client.connect()
    st.success("Connected to server!")

# --- Message Options ---
msg_type = st.selectbox("Select FIX Message Type", ["Logon", "Heartbeat", "New Order"])

if msg_type == "New Order":
    cl_ord_id = st.text_input("ClOrdID", value="123")
    symbol = st.text_input("Symbol", value="AAPL")
    side = st.selectbox("Side", ["Buy", "Sell"])
    order_qty = st.number_input("OrderQty", value=100)
    price = st.number_input("Price", value=150.00)
else:
    cl_ord_id = symbol = side = order_qty = price = None

# --- Send Button ---
if st.button("📤 Send FIX Message"):
    if not client.running:
        st.error("Client not connected.")
    else:
        if msg_type == "Logon":
            msg = build_logon()
        elif msg_type == "Heartbeat":
            msg = build_heartbeat()
        else:
            msg = build_new_order(cl_ord_id, symbol, side, order_qty, price)

        client.send(msg)
        st.code(msg, language='fix')

# --- Output Box ---
st.subheader("📩 Received Messages")
st.text_area("Server Responses", value="\n".join(client.responses[-10:]), height=300)
