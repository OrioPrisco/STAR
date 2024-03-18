import gamesave
import json
import traceback

def decode_gamesave(string, display_error):
	schema = json.load(open("./gamesave-schema.json", "r"))
	try:
		decoded = gamesave.decode_file(string, schema, False, display_error, False)
		pretty = json.dumps(decoded, indent=4)
		return pretty
	except Exception as e:
		display_error("".join(traceback.format_exception(e)))
		raise e

def encode_json(string, display_error):
	schema = json.load(open("./gamesave-schema.json", "r"))
	try:
		encoded = gamesave.encode_file(string, schema, False, display_error, False)
		return encoded
	except Exception as e:
		display_error("".join(traceback.format_exception(e)))
		raise e

#export functions to js

import js

js.encode_json = encode_json
js.decode_gamesave = decode_gamesave
