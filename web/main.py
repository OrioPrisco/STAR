import gamesave
import json
import traceback

def decode_gamesave(string, logger):
	schema = json.load(open("./gamesave-schema.json", "r"))
	try:
		decoded = gamesave.decode_file(string, schema, logger)
		pretty = json.dumps(decoded, indent=4)
		return pretty
	except Exception as e:
		logger.error(repr(e), "".join(traceback.format_exception(e)))
		raise e

def encode_json(string, logger):
	schema = json.load(open("./gamesave-schema.json", "r"))
	try:
		encoded = gamesave.encode_file(string, schema, logger)
		return encoded
	except Exception as e:
		logger.error(repr(e), "".join(traceback.format_exception(e)))
		raise e

#export functions to js

import js

js.encode_json = encode_json
js.decode_gamesave = decode_gamesave
