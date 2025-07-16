import datetime

SOH = '\x01'

def calculate_checksum(fix_message: str) -> str:
    """Calculate FIX checksum (sum of bytes modulo 256)"""
    total = sum(ord(c) for c in fix_message)
    checksum = total % 256
    return str(checksum).zfill(3)

def get_utc_timestamp() -> str:
    """Return UTC timestamp in FIX format: YYYYMMDD-HH:MM:SS"""
    return datetime.datetime.utcnow().strftime('%Y%m%d-%H:%M:%S')
