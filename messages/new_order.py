from fix_parser import build_fix_message
from fix_utils import get_utc_timestamp

def build_new_order_single(
    cl_ord_id="12345",
    symbol="AAPL",
    side="1",  # 1 = Buy, 2 = Sell
    order_qty="100",
    price="150.00",
    sender_comp_id="CLIENT1",
    target_comp_id="SERVER",
    seq_num="3"
):
    fields = [
        ("35", "D"),  # MsgType = NewOrderSingle
        ("34", seq_num),
        ("49", sender_comp_id),
        ("56", target_comp_id),
        ("52", get_utc_timestamp()),
        ("11", cl_ord_id),  # ClOrdID
        ("21", "1"),  # HandlInst (1 = Automated execution)
        ("55", symbol),  # Symbol
        ("54", side),  # Side
        ("38", order_qty),  # OrderQty
        ("40", "2"),  # OrdType = Limit
        ("44", price),  # Price
        ("59", "0"),  # TimeInForce = Day
    ]
    return build_fix_message(fields)
