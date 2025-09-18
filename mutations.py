# mutations.py
import random
BASES = ["A", "T", "G", "C"]

def introduce_mutations(seq: str, num_mutations: int = 1) -> str:
    """Random substitution mutations only (no indels)."""
    if not seq:
        return seq
    seq = list(seq)
    L = len(seq)
    for _ in range(max(0, num_mutations)):
        idx = random.randint(0, L - 1)
        choices = [b for b in BASES if b != seq[idx]]
        seq[idx] = random.choice(choices)
    return "".join(seq)
