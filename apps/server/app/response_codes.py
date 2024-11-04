import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESPONSE_CODES_FILE = os.path.join(BASE_DIR, "..", "..", "shared", "response_codes.json")

with open(RESPONSE_CODES_FILE) as f:
    RESPONSE_CODES = json.load(f)
