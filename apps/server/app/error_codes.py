import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ERROR_CODES_FILE = os.path.join(BASE_DIR, '..', '..', 'shared', 'error_codes.json')

with open(ERROR_CODES_FILE) as f:
    ERROR_CODES = json.load(f)
