# decoder.py
DNA_REVERSE_MAP = {"A": "00", "T": "01", "G": "10", "C": "11"}

def _dna_to_binary(dna: str) -> str:
    return "".join(DNA_REVERSE_MAP.get(b, "") for b in dna)

def recover_length_from_header(header_bases: str) -> int:
    """
    header_bases should be first 24 bases (48 bits). Returns integer length (chars).
    Majority-vote across the three repeated 16-bit fields.
    """
    header_bases = (header_bases or "").ljust(24, "A")[:24]
    bits48 = _dna_to_binary(header_bases)
    bits48 = bits48.ljust(48, "0")[:48]
    parts = [bits48[0:16], bits48[16:32], bits48[32:48]]
    recovered_bits = []
    for i in range(16):
        column = [p[i] for p in parts]
        recovered_bits.append("1" if column.count("1") >= 2 else "0")
    return int("".join(recovered_bits), 2)

def _binary_to_text(binary: str, length_chars: int) -> str:
    needed = length_chars * 8
    payload = binary[:needed].ljust(needed, "0")
    chars = [chr(int(payload[i:i+8], 2)) for i in range(0, len(payload), 8)]
    return "".join(chars)

def _majority_vote_payload(chunks: list, length_chars: int) -> str:
    """
    chunks: list of payload chunks (each string of bases).
    returns a single payload bases string (length = 4 * length_chars).
    """
    payload_len = 4 * length_chars
    norm = [c.ljust(payload_len, "A")[:payload_len] for c in chunks]
    result = []
    for i in range(payload_len):
        column = [c[i] for c in norm]
        result.append(max(set(column), key=column.count))
    return "".join(result)

def decode_payload_to_text(payload_bases: str, length_chars: int) -> str:
    payload_len = 4 * length_chars
    trim = (payload_bases or "").ljust(payload_len, "A")[:payload_len]
    binary = _dna_to_binary(trim)
    return _binary_to_text(binary, length_chars)

def decode_dna_full(dna_full: str, redundancy: int = 3) -> str:
    """
    Full decode for DNA created by encode_text(text, redundancy).
    """
    if not dna_full:
        return ""
    header = dna_full[:24].ljust(24, "A")[:24]
    length_chars = recover_length_from_header(header)
    if length_chars == 0:
        return ""
    payload_len = 4 * length_chars
    start = 24
    chunks = []
    for r in range(int(max(1, redundancy))):
        s = start + r * payload_len
        chunks.append(dna_full[s:s + payload_len])
    corrected_payload = _majority_vote_payload(chunks, length_chars)
    return decode_payload_to_text(corrected_payload, length_chars)

# debug helper
def get_header_info(dna_full: str):
    header = dna_full[:24].ljust(24, "A")[:24]
    length_chars = recover_length_from_header(header)
    return {"header_bases": header, "recovered_length": length_chars, "expected_payload_bases": 4 * length_chars}
