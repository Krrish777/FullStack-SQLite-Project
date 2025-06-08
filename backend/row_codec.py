import json
from utils.logger import get_logger

logger = get_logger(__name__)

def encode_row(row: dict) -> bytes:
    logger.debug(f"Encoding row: {row}")
    try:
        encoded = json.dumps(row).encode("utf-8")
        logger.debug(f"Encoded bytes: {encoded}")
        logger.info("Row successfully encoded.")
        return encoded
    except (TypeError, ValueError) as e:
        logger.error(f"Failed to encode row {row}: {e}")
        raise

def decode_row(blob: bytes) -> dict:
    if not blob or blob.strip() == b'':
        logger.warning("Cannot decode an empty or whitespace-only blob.")
        raise ValueError("Cannot decode an empty or whitespace-only blob.")
    
    try:
        decoded_str = blob.decode("utf-8")
        logger.debug(f"Decoding blob: {blob} -> '{decoded_str}'")
        row = json.loads(decoded_str)
        logger.debug(f"Decoded row dict: {row}")
        logger.info("Blob successfully decoded to row.")
        return row
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        logger.error(f"Failed to decode blob {blob}: {e}")
        raise
