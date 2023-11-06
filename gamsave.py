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
	"Upgrade" : enums.Upgrade,
	"Keyword"  : enums.Keyword,
	"Floor" : enums.Floor,
	"Weapon" : enums.Weapon,
	"Cartridge" : enums.Cartridge,
	"Unique" : enums.Unique,
	"Ship" : enums.Ship,
	"Active" : enums.Active,
	"Unlock" : enums.Unlock,
	"Bomb" : enums.Bomb,
	"Blessing" : enums.Blessing,
	"Blessed" : enums.Blessed,
}

line_decoders = {
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
	lines = base64.b64decode("".join(args.input.readlines()))
	lines = lines.decode("utf8").splitlines()
	output = {}
	for key in schema:
		item = lines.pop(0)
		if (args.verbose):
			print(key, item, file=sys.stderr)
		output[key] = line_decoders[schema[key]["type"]][0](item)
	print(json.dumps(output, indent=4))
