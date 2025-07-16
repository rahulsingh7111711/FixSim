from fix_parser import build_fix_message
from fix_utils import get_utc_timestamp

def build_heartbeat(sender_comp_id="CLIENT1", target_comp_id="SERVER", seq_num="2"):
    fields = [
        ("35", "0"),  # MsgType = Heartbeat
        ("34", seq_num),
        ("49", sender_comp_id),
        ("56", target_comp_id),
        ("52", get_utc_timestamp()),
    ]
    return build_fix_message(fields)
