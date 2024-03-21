#!/bin/python3

import encode as en
import decode as dc
import argparse
import json
import sys
import os
import enums
import base64
import binascii
import traceback


enums = {
	"upgrade" : enums.Upgrade,
	"keyword"  : enums.Keyword,
	"floor" : enums.Floor,
	"weapon" : enums.Weapon,
	"cartridge" : enums.Cartridge,
	"unique" : enums.Unique,
	"ship" : enums.Ship,
	"active" : enums.Active,
	"unlock" : enums.Unlock,
	"bomb" : enums.Bomb,
	"blessing" : enums.Blessing,
	"blessed" : enums.Blessed,
	"lethality" : enums.Lethality
}

def get_kind(**kwargs):
	kind_name = kwargs.get("kind", None)
	if (kind_name == None):
		return None
	return enums[kind_name.lower()]

def log_except(logger, title, exception):
	logger.error(f"{title} [{repr(exception)}]", "".join(traceback.format_exception(exception)))

def decode_int_wrapper(value, logger, **kwargs):
	# TODO : handle length of
	return int(value)

def decode_bool_wrapper(value, logger, **kwargs):
	field = kwargs["field"]
	value = int(value)
	if (value != 1 and value != 0):
		logger.warn(f"{field}: {value} is not a boolean value !", "If You did not modify your save and got this error, please report it")
	return value


def decode_enum_wrapper(value, logger, **kwargs):
	kind = get_kind(**kwargs)
	field = kwargs["field"]
	return dc.decode_enum(int(value), logger, kind, field)

def decode_float_wrapper(value, logger, **kwargs):
	return float(value)

def decode_string_wrapper(value, logger, **kwargs):
	return value

def decode_2E01_wrapper(value, logger, **kwargs):
	kind = get_kind(**kwargs)
	return dc.decode_2E01(value, logger, kind)


def decode_9201_wrapper(value, logger, **kwargs):
	kind = get_kind(**kwargs)
	return dc.decode_9201(value, logger, kind)

def decode_space_separated_decimal_wrapper(value, logger, **kwargs):
	return [int(i) for i in value.split()]

def decode_bitfield_wrapper(value, logger, **kwargs):
	value = int(value)
	i = 0
	output = []
	while (1 << i) <= value:
		bit_value = (1 << i) & value
		if bit_value:
			output.append(decode_enum_wrapper(i, logger, **kwargs))
		i += 1
	return output

def encode_int_wrapper(value, logger, **kwargs):
	assert isinstance(value, (int, float)), f"number required but got {type(value).__name__}"
	field = kwargs["field"]
	if (isinstance(value, float)):
		logger.warn(f"{field}: {value} is a float, it will be truncated as an integer", "If You did not modify your save and got this error, please report it")
	return str(value)

def encode_bool_wrapper(value, logger, **kwargs):
	field = kwargs["field"]
	assert isinstance(value, (int, float)), f"number required but got {type(value).__name__}"
	if (value != 1 and value != 0):
		logger.warn(f"{field}: {value} is not a boolean value !", "It should be 1 or 0, Who knows what this will do")
	return str(value)

def encode_enum(value, logger, **kwargs):
	assert isinstance(value, (int, float, str)), f"number/string required but got {type(value).__name__}"
	kind = get_kind(**kwargs)
	field = kwargs["field"]
	if (kind == None):
		logger.debug(f"{field}: Unknown kind", f"These values are not quite known yet, this is quite normal")
	value = en.try_int_from_enum(value, kind)
	assert value != None, f"Couldn't convert {value} to an integer id with kind {kind.__name__ if kind else 'None'}"
	return value

def encode_enum_wrapper(value, logger, **kwargs):
	return str(encode_enum(value, logger, **kwargs))

def encode_float_wrapper(value, logger, **kwargs):
	assert isinstance(value, (int, float)), f"number required but got {type(value).__name__}"
	return str(value)

def encode_string_wrapper(value, logger, **kwargs):
	assert isinstance(value, str), f"string required but got {type(value).__name__}"
	return value

def encode_2E01_wrapper(value, logger, **kwargs):
	kind = get_kind(**kwargs)
	field = kwargs["field"]
	if (kind == None):
		if field == "likely unlocks line 4" or field == "likely unlocks line 5":
			logger.debug(f"{field}: Unknown kind {kwargs.get('kind', 'None')}", f"These values are not quite known yet, this is quite normal")
		elif field == "jukebox musics":
			logger.debug("{field}: Skipping conversion to integer", "Normal but means no validation is performed")
		else:
			logger.warn(f"{field}: Unknown kind {kwargs.get('kind', 'None')}", f"Might cause conversion failures for {value}")
	value, err = en.encode_2E01(value, logger, kind)
	assert not kind or not err, f"Couldn't convert {value} to an integer id with kind {kind.__name__ if kind else 'None'}"
	return value

def encode_9201_wrapper(value, logger, **kwargs):
	value, err = en.encode_9201(value, logger)
	return value

def encode_space_separated_decimal_wrapper(value, logger, **kwargs):
	assert isinstance(value, list), f"list required but got {type(value).__name__}"
	for i in value:
		assert isinstance(i, int), f"int required but got {type(value).__name__}"
	return " ".join([str(i) for i in value])


def encode_bitfield_wrapper(value, logger, **kwargs):
	assert isinstance(value, list), f"list required but got {type(value).__name__}"
	output = 0
	for item in value:
		decoded_int = encode_enum(item, logger, **kwargs)
		assert isinstance(decoded_int, (int, float)), f"Cannot insert non integer value {decoded_int} into a bitfield"
		output |= 1 << decoded_int
	return str(output)

line_handlers = {
	"int" : [decode_int_wrapper, encode_int_wrapper],
	"bool" : [decode_bool_wrapper, encode_bool_wrapper],
	"enum" : [decode_enum_wrapper, encode_enum_wrapper],
	"float" : [decode_float_wrapper, encode_float_wrapper],
	"string" : [decode_string_wrapper, encode_string_wrapper],
	"2E01" : [decode_2E01_wrapper, encode_2E01_wrapper],
	"9201" : [decode_9201_wrapper, encode_9201_wrapper],
	"space separated decimal" : [decode_space_separated_decimal_wrapper, encode_space_separated_decimal_wrapper],
	"bitfield" : [decode_bitfield_wrapper, encode_bitfield_wrapper],
}

def decode_file(b64lines, schema, logger):
	try:
		lines = base64.b64decode(b64lines)
	except binascii.Error as e:
		if (logger.interactive):
			log_except(logger, f"Couldn't decode the base64 (.d13) file. Corrupted file or did you mean to encode ?", e)
		else:
			log_except(logger, f"Couldn't decode the base64 (.d13) file. Corrupted file ?", e)
		raise e
	except ValueError as e:
		logger_except(logger, "Non ascii character in the base64 (.d13) file", e)
		raise e
	output = {}
	try:
		lines = lines.decode("utf8").splitlines()
	except UnicodeDecodeError as e:
		log_except(logger, f"Couldn't decode the base64 file as utf8. Corrupted file ?", e)
		raise e
	for key in schema:
		item = lines.pop(0)
		logger.debug(key, f"value {item}")
		try:
			output[key] = line_handlers[schema[key]["type"]][0](item, logger, field=key, **schema[key])
		except Exception as e:
			log_except(logger, f"Error when decoding field {key}", e)
			raise e
	return output

def encode_file(jsonlines, schema, logger):
	try:
		input_dir = json.loads(jsonlines)
	except json.decoder.JSONDecodeError as e:
		if (logger.interactive):
			log_except(logger, f"Couldn't decode the json file. Bad json format or did you mean to decode ?", e)
		else:
			log_except(logger, f"Couldn't decode the json file. Bad json format ?", e)
		raise e
	output = []
	for key in schema:
		logger.debug(key)
		try:
			output.append(line_handlers[schema[key]["type"]][1](input_dir[key], logger, field=key, **schema[key]))
		except Exception as e:
			log_except(logger, f"Error when encoding field {key}", e)
			raise e
	output = "\n".join(output)
	output = base64.b64encode(output.encode("utf8"))
	return output.decode("utf8")

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

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", required=False, type=argparse.FileType('r'), default=sys.stdin)
	parser.add_argument("-d", "--decode", required=False, action='store_true', default=False)
	parser.add_argument("-v", "--verbose", required=False, action='store_true', default=False, help="Enables warnings and debug logs")
	parser.add_argument("-w", "--warnings", required=False, action='store_true', default=False, help="Enables warnings")
	#option for passing custom schema ?
	args = parser.parse_args()
	script_dir = os.path.abspath( os.path.dirname( __file__ ) )
	schema = json.load(open(os.path.join(script_dir, "gamesave-schema.json"), "r"))
	logger = Logger(args.verbose, args.warnings)
	if args.decode:
		b64lines = "".join(args.input.readlines())
		output = decode_file(b64lines, schema, logger)
		print(json.dumps(output, indent=4))
	else:
		jsonlines = "".join(args.input.readlines())
		output = encode_file(jsonlines, schema, logger)
		print(output)
