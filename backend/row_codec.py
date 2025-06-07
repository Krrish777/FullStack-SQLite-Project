import json
def encode_row(row: dict) -> bytes:
    return json.dumps(row).encode("utf-8")

def decode_row(blob: bytes) -> dict:
    if not blob or blob.strip() == b'':
        raise ValueError("Cannot decode an empty or whitespace-only blob.")
    return json.loads(blob.decode("utf-8"))