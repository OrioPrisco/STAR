import gamesave
import json
from utils import minify_arrays


def decode_gamesave(string, logger, test_run = False):
	with open("./gamesave-schema.json", "rt") as f:
		schema = json.load(f)
	decoded = gamesave.decode_file(string, schema, logger, test_run)
	if test_run:
		return
	pretty = minify_arrays(json.dumps(decoded, indent = 4))
	return pretty


def encode_json(string, logger, test_run = False):
	with open("./gamesave-schema.json", "rt") as f:
		schema = json.load(f)
	encoded = gamesave.encode_file(string, schema, logger, test_run)
	if test_run:
		return
	return encoded


# export functions to js

import js

js.encode_json = encode_json
js.decode_gamesave = decode_gamesave
