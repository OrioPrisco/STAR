#!/bin/python3

import encode as en
import decode as dc
import argparse
import json
import sys
import enums
from utils import Logger

enum_types = {
	"weapon" : enums.Weapon,
	"keyword" : enums.Keyword,
	"upgrade" : enums.Upgrade,
	"cartridge" : enums.Cartridge,
	"bomb" : enums.Bomb,
	"unlock" : enums.Unlock,
}
valid_headers = {"9201", "2E01"}

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", required=False, type=argparse.FileType('r'), default=sys.stdin)
	parser.add_argument("-d", "--decode", required=False, action='store_true', default=False)
	parser.add_argument("-v", "--verbose", required=False, action='store_true', default=False, help="Enables warnings and debug logs")
	parser.add_argument("-w", "--warnings", required=False, action='store_true', default=False, help="Enables warnings")
	parser.add_argument("-t", "--type", required=False, action='store', choices=valid_headers)
	parser.add_argument("-k", "--kind", required=False, action='store', choices=enum_types)
	args = parser.parse_args()
	logger = Logger(args.verbose, args.warnings)
	if args.kind:
		args.kind = enum_types[args.kind]
	if args.kind and args.type == "9201":
		parser.print_usage();
		print(f"{__file__}: error: -k/--kind can only be used with 2E01")
		exit(1)
	if args.kind and not args.type:
		logger.debug(f"{__file__}: Warning: -k/--kind can only be used with 2E01", "")
	if args.decode:
		for line in args.input.readlines():
			output = dc.decode_header(line, args.type, logger, args.kind)
			print(json.dumps(output, indent=4))
	else:
		decoder = json.JSONDecoder();
		inputs = args.input.read().strip();
		while len(inputs):
			json_obj, offset = decoder.raw_decode(inputs)
			logger.debug(f"{offset} characters to decode", "")
			line, err = en.encode_header(json_obj, args.type, logger, args.kind)
			print(line)
			inputs = inputs[offset:].strip()
			logger.debug(f"now decoding `{inputs}`", file=sys.stderr)
