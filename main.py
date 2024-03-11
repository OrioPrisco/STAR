from pyweb import pydom
import gamesave
import json

def decode_gamesave(event):
	pydom["#output"][0].html = ""
	schema = json.load(open("./gamesave-schema.json", "r"))
	gamesave_lines = pydom["#input"][0].value
	print(gamesave_lines)
	decoded = gamesave.decode_file(gamesave_lines, schema, False)
	print(decoded)
	pydom["#output"][0].html = json.dumps(decoded, indent=4)

def encode_json(event):
	pydom["#output"][0].html = ""
	schema = json.load(open("./gamesave-schema.json", "r"))
	json_lines = pydom["#input"][0].value
	print(json_lines)
	encoded = gamesave.encode_file(json_lines, schema, False)
	print(encoded)
	pydom["#output"][0].html = encoded
