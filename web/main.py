import gamesave
import json
from utils import minify_arrays

def decode_gamesave(string, logger):
	with open("./gamesave-schema.json", "rt") as f:
		schema = json.load(f)
	try:
		decoded = gamesave.decode_file(string, schema, logger)
		pretty = minify_arrays(json.dumps(decoded, indent=4))
		return pretty
	except Exception as e:
		raise e

def encode_json(string, logger):
	with open("./gamesave-schema.json", "rt") as f:
		schema = json.load(f)
	try:
		encoded = gamesave.encode_file(string, schema, logger)
		return encoded
	except Exception as e:
		raise e

#export functions to js

import js

js.encode_json = encode_json
js.decode_gamesave = decode_gamesave
