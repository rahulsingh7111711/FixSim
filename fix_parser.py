#from fix_utils import SOH
from fix_utils import SOH, calculate_checksum


def build_fix_message(fields: list) -> str:
    """
    Takes list of (tag, value) tuples and builds a FIX message string.
    Automatically calculates BodyLength and Checksum.
    """
    # Start with header fields (exclude 8, 9, 10 for now)
    header = [("8", "FIX.4.4")]  # BeginString
    body = fields.copy()
    
    # Compose without checksum first
    full_body = header + [("9", "000")] + body
    msg_without_checksum = SOH.join([f"{tag}={value}" for tag, value in full_body]) + SOH

    # Replace real BodyLength
    body_str = SOH.join([f"{tag}={value}" for tag, value in full_body[2:]]) + SOH
    body_length = len(body_str)
    full_body[1] = ("9", str(body_length))

    # Rebuild message with correct BodyLength
    final_body = SOH.join([f"{tag}={value}" for tag, value in full_body])
    checksum = calculate_checksum(final_body + SOH)
    
    # Add checksum field
    return final_body + SOH + f"10={checksum}" + SOH

def parse_fix_message(raw_message: str) -> dict:
    """
    Parses a raw FIX message string into a dictionary {tag: value}
    """
    fields = raw_message.strip().split(SOH)
    parsed = {}
    for field in fields:
        if '=' in field:
            tag, value = field.split('=', 1)
            parsed[tag] = value
    return parsed
