from fix_parser import build_fix_message
from fix_utils import get_utc_timestamp

def build_logon(sender_comp_id="CLIENT1", target_comp_id="SERVER"):
    fields = [
        ("35", "A"),  # MsgType = Logon
        ("34", "1"),  # MsgSeqNum
        ("49", sender_comp_id),  # SenderCompID
        ("56", target_comp_id),  # TargetCompID
        ("52", get_utc_timestamp()),  # SendingTime
        ("98", "0"),  # Encryption (0 = None)
        ("108", "30"),  # HeartBtInt (in seconds)
    ]
    return build_fix_message(fields)
