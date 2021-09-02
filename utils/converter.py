from typing import Optional


def convert_to_32_bit(decimal: str) -> str:
    binary = bin(int(decimal))[2:]
    binary = str(binary).rjust(32, '0')
    return binary


def convert_to_2_bit(decimal: str) -> Optional[str]:
    if int(decimal) > 3:
        return None
    binary = bin(int(decimal))[2:]
    binary = str(binary).rjust(2, '0')
    return binary
