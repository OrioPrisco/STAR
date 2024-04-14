import sys


def logger_print(kind):
	def stderr_print_with_title(title, content):
		print(f"{kind}: {title}\n{content}", file = sys.stderr)

	return stderr_print_with_title


def noop(*_):
	pass


class Logger:
	def __init__(self, verbose = False, warnings = False, interactive = True):
		if verbose:
			self.debug = logger_print("Debug")
		else:
			self.debug = noop
		if verbose or warnings:
			self.warn = logger_print("Warning")
		else:
			self.warn = noop
		self.error = logger_print("Error")
		self.interactive = interactive


import json

default_to_minify = [
	"likely unlocks line 4",
	"likely unlocks line 5",
	"likely bestiary data line 6",
	"likely bestiary data line 7",
	"likely bestiary data line 8",
]


def minify_arrays(json_string, to_minify = default_to_minify):
	start = 0
	result = ""
	decoder = json.JSONDecoder()
	while True:
		bracket_index = json_string.find("[", start)
		if bracket_index == -1:
			result += json_string[start:]
			return result
		name_end_index = json_string.rfind('"', start, bracket_index)
		if name_end_index != -1:
			name_begin_index = json_string.rfind('"', start, name_end_index) + 1
		if (
			name_end_index == -1
			or name_begin_index == -1
			or json_string[name_begin_index:name_end_index] in to_minify
		):
			result += json_string[start:bracket_index]
			array, end_array = decoder.raw_decode(json_string, bracket_index)
			result += json.dumps(array)
			start = end_array
		else:
			array, end_array = decoder.raw_decode(json_string, bracket_index)
			result += json_string[start:end_array]
			start = end_array
