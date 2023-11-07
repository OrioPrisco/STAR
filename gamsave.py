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
	#TODO : properly implement
	return value

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

def encode_enum_wrapper(value, debug, **kwargs):
	assert isinstance(value, (int, float, str)), f"number/string required but got {type(value).__name__}"
	kind = get_kind(**kwargs)
	if (kind == None):
		dbg_print(debug, f"Unknown kind {kwargs.get('kind', 'None')}")
	value = en.try_int_from_enum(value, kind)
	assert value != None, f"Couldn't convert {value} to an integer id with kind {kind.__name__ if kind else 'None'}"
	return str(value)

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
	#TODO : implement
	return value

line_handlers = {
	"int" : [int, str],
	"bool" : [int, str],
	"enum" : [int, str],
	"float" : [float, str],
	"string" : [str, str],
	"2E01" : [dc.decode_2E01, en.encode_2E01],
	"9201" : [dc.decode_9201, en.encode_9201],
	"space separated decimal" : [str, str],
	"bitfield" : [int, str],
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
		lines = base64.b64decode("".join(args.input.readlines()))
		lines = lines.decode("utf8").splitlines()
		output = {}
		for key in schema:
			item = lines.pop(0)
			if (args.verbose):
				print(key, item, file=sys.stderr)
			output[key] = line_handlers[schema[key]["type"]][0](item)
		print(json.dumps(output, indent=4))
	else:
		input_dir = json.load(args.input)
		output = []
		for key in schema:
			output.append(line_handlers[schema[key]["type"]][1](input_dir[key]))
		output = "\n".join(output)
		output = base64.b64encode(output.encode("utf8"))
		print(output.decode("utf8"))
