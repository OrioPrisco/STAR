from pyweb import pydom
import gamesave
import json
from pyscript import window, document
from js import highlight_elem

def clean_output_and_errors():
	pydom["#output"][0].value = ""
	nodes = document.querySelectorAll(".py-error")
	if nodes:
		for node in nodes:
			node.remove()

def decode_gamesave(event):
	clean_output_and_errors()
	schema = json.load(open("./gamesave-schema.json", "r"))
	gamesave_lines = pydom["#input"][0].value
	decoded = gamesave.decode_file(gamesave_lines, schema, False)
	textarea = document.getElementById("output")
	textarea.value = json.dumps(decoded, indent=4)
	textarea.scrollTop = 0
	highlight_elem(textarea)

def encode_json(event):
	clean_output_and_errors()
	schema = json.load(open("./gamesave-schema.json", "r"))
	json_lines = pydom["#input"][0].value
	encoded = gamesave.encode_file(json_lines, schema, False)
	textarea = document.getElementById("output")
	textarea.value = encoded
	textarea.scrollTop = 0
	highlight_elem(textarea)
