import json
def encode_row(row: dict) -> bytes:
    return json.dumps(row).encode("utf-8")

def decode_row(blob: bytes) -> dict:
    return json.loads(blob.decode("utf-8"))