import gamesave
import json
import traceback
import sys
from js import console

#console.log is used instead of print to not have the message displayed as several entries

def decode_gamesave(string, suppress_errors):
	schema = json.load(open("./gamesave-schema.json", "r"))
	try:
		decoded = gamesave.decode_file(string, schema, False, suppress_errors)
		pretty = json.dumps(decoded, indent=4)
		return pretty
	except Exception as e:
		if suppress_errors:
			console.log("".join(traceback.format_exception(e)))
			return None
		raise e

def encode_json(string, suppress_errors):
	schema = json.load(open("./gamesave-schema.json", "r"))
	try:
		encoded = gamesave.encode_file(string, schema, False, suppress_errors)
		return encoded
	except Exception as e:
		if suppress_errors:
			console.log("".join(traceback.format_exception(e)))
			return None
		raise e

#export functions to js

import js

js.encode_json = encode_json
js.decode_gamesave = decode_gamesave
