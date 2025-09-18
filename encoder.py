# encoder.py
DNA_MAP = {
    "00": "A",
    "01": "T",
    "10": "G",
    "11": "C",
}

def _text_to_binary(text: str) -> str:
    """Convert text to a binary string (8 bits per char)."""
    return "".join(format(ord(ch), "08b") for ch in text)

def _binary_to_dna(binary: str) -> str:
    """Convert binary string to DNA bases (2 bits → 1 base). Pads binary to even length."""
    if len(binary) % 2 != 0:
        binary += "0"
    return "".join(DNA_MAP[binary[i:i+2]] for i in range(0, len(binary), 2))

def encode_text(text: str, redundancy: int = 3) -> str:
    """
    Encode text into DNA string with:
      - header: 16-bit length repeated 3x (48 bits => 24 bases)
      - payload: binary -> dna
      - payload repeated `redundancy` times
    """
    # header
    length = len(text)
    header_bits = f"{length:016b}" * 3  # 3 repeats
    header_dna = _binary_to_dna(header_bits)

    # payload
    payload_bits = _text_to_binary(text)
    payload_dna = _binary_to_dna(payload_bits)

    # redundancy
    payload_redundant = payload_dna * max(1, int(redundancy))

    return header_dna + payload_redundant
