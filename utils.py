import sys

def logger_print(kind):
	def stderr_print_with_title(title, content):
		print(f"{kind}: {title}\n{content}", file=sys.stderr)
	return stderr_print_with_title

def noop(*args):
	pass

class Logger:
	def __init__(self, verbose=False, warnings=False, interactive=True):
		if verbose:
			self.debug = logger_print("Debug")
		else:
			self.debug = noop
		if verbose or warnings:
			self.warn = logger_print("Warning")
		else:
			self.warn = noop
		self.error = logger_print("Error")
		self.interactive=True

import json

def minify_arrays(json_string):
	start = 0
	result = ""
	decoder = json.JSONDecoder()
	while True:
		brakcet_index = json_string.find("[", start)
		if brakcet_index == -1:
			result += json_string[start:]
			return result
		result += json_string[start:brakcet_index]
		array, end_array = decoder.raw_decode(json_string, brakcet_index)
		result += json.dumps(array)
		start = end_array
