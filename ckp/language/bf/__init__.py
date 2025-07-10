def bf_from_bytes(b: bytes) -> str:
    raise NotImplementedError("Not yet implemented!")

def bf_from_text(text: str) -> str:
    return bf_from_bytes(text.encode('utf-8'))