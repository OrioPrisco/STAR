#!/bin/python3

import encode as en
import decode as dc
import argparse
import json
import sys
import os
import enums
import base64


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

def dbg_print(debug, message):
	if (debug):
		print(message, file=sys.stderr)

def decode_int_wrapper(value, debug, **kwargs):
	# TODO : handle length of
	return int(value)

def decode_bool_wrapper(value, debug, **kwargs):
	value = int(value)
	if (debug and (value != 1 and value != 0)):
		dbg_print(debug, f"Warning, {value} is not a boolean value !")
	return value


def decode_enum_wrapper(value, debug, **kwargs):
	kind = get_kind(**kwargs)
	value_as_str = dc.try_str_from_enum(int(value), kind)
	if (value_as_str == None):
		dbg_print(debug, f"Warning, couldn't convert {value} to a string using kind {kind.__name__ if kind else 'None'}")
		return int(value)
	return value_as_str

def decode_float_wrapper(value, debug, **kwargs):
	return float(value)

def decode_string_wrapper(value, debug, **kwargs):
	return value

def decode_2E01_wrapper(value, debug, **kwargs):
	kind = get_kind(**kwargs)
	return dc.decode_2E01(value, debug, kind)


def decode_9201_wrapper(value, debug, **kwargs):
	kind = get_kind(**kwargs)
	return dc.decode_9201(value, debug, kind)

def decode_space_separated_decimal_wrapper(value, debug, **kwargs):
	return [int(i) for i in value.split()]

def decode_bitfield_wrapper(value, debug, **kwargs):
	value = int(value)
	i = 0
	output = []
	while (1 << i) <= value:
		bit_value = (1 << i) & value
		if bit_value:
			output.append(decode_enum_wrapper(i, debug, **kwargs))
		i += 1
	return output

def encode_int_wrapper(value, debug, **kwargs):
	assert isinstance(value, (int, float)), f"number required but got {type(value).__name__}"
	if (isinstance(value, float)):
		dbg_print(debug, f"Warning {value} is a float, it will be truncated as an integer")
	return str(value)

def encode_bool_wrapper(value, debug, **kwargs):
	assert isinstance(value, (int, float)), f"number required but got {type(value).__name__}"
	if (debug and (value != 1 or value != 0)):
		dbg_print(debug, f"Warning, {value} is not a boolean value !")
	return str(value)

def encode_enum(value, debug, **kwargs):
	assert isinstance(value, (int, float, str)), f"number/string required but got {type(value).__name__}"
	kind = get_kind(**kwargs)
	if (kind == None):
		dbg_print(debug, f"Unknown kind {kwargs.get('kind', 'None')}")
	value = en.try_int_from_enum(value, kind)
	assert value != None, f"Couldn't convert {value} to an integer id with kind {kind.__name__ if kind else 'None'}"
	return value

def encode_enum_wrapper(value, debug, **kwargs):
	return str(encode_enum(value, debug, **kwargs))

def encode_float_wrapper(value, debug, **kwargs):
	assert isinstance(value, (int, float)), f"number required but got {type(value).__name__}"
	return str(value)

def encode_string_wrapper(value, debug, **kwargs):
	assert isinstance(value, str), f"string required but got {type(value).__name__}"
	return value

def encode_2E01_wrapper(value, debug, **kwargs):
	kind = get_kind(**kwargs)
	if (kind == None):
		dbg_print(debug, f"Unknown kind {kwargs.get('kind', 'None')}")
	value, err = en.encode_2E01(value, debug, kind)
	assert not kind or not err, f"Couldn't convert {value} to an integer id with kind {kind.__name__ if kind else 'None'}"
	return value

def encode_9201_wrapper(value, debug, **kwargs):
	value, err = en.encode_9201(value, debug)
	return value

def encode_space_separated_decimal_wrapper(value, debug, **kwargs):
	assert isinstance(value, list), f"list required but got {type(value).__name__}"
	for i in value:
		assert isinstance(i, int), f"int required but got {type(value).__name__}"
	return " ".join([str(i) for i in value])


def encode_bitfield_wrapper(value, debug, **kwargs):
	assert isinstance(value, list), f"list required but got {type(value).__name__}"
	output = 0
	for item in value:
		decoded_int = encode_enum(item, debug, **kwargs)
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

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", required=False, type=argparse.FileType('r'), default=sys.stdin)
	parser.add_argument("-d", "--decode", required=False, action='store_true', default=False)
	parser.add_argument("-v", "--verbose", required=False, action='store_true', default=False)
	#option for passing custom schema ?
	args = parser.parse_args()
	script_dir = os.path.abspath( os.path.dirname( __file__ ) )
	schema = json.load(open(os.path.join(script_dir, "gamesave-schema.json"), "r"))
	if args.decode:
		try:
			lines = base64.b64decode("".join(args.input.readlines()))
		except binascii.Error as e:
			print(f"Couldn't decode the base64 file. Corrupted file or did you mean to encode ?", file=sys.stderr)
			raise e
		lines = lines.decode("utf8").splitlines()
		output = {}
		for key in schema:
			item = lines.pop(0)
			if (args.verbose):
				print(key, item, file=sys.stderr)
			output[key] = line_handlers[schema[key]["type"]][0](item, args.verbose, **schema[key])
		print(json.dumps(output, indent=4))
	else:
		try:
			input_dir = json.load(args.input)
		except json.decoder.JSONDecodeError as e:
			print(f"Couldn't decode the json file. Bad json format or did you mean to decode ?", file=sys.stderr)
			raise e
		output = []
		for key in schema:
			if (args.verbose):
				print(key, file=sys.stderr)
			output.append(line_handlers[schema[key]["type"]][1](input_dir[key], args.verbose, **schema[key]))
		output = "\n".join(output)
		output = base64.b64encode(output.encode("utf8"))
		print(output.decode("utf8"))
