#!/bin/python3

import encode as en
import decode as dc
import argparse
import json
import sys

valid_headers = {"9201", "2E01"}

if __name__ == "__main__":
	deciding_args_parser = argparse.ArgumentParser(add_help=False)
	deciding_args_parser.add_argument("-d", "--decode", required=False, action='store_true', default=False)
	deciding_args, _ = deciding_args_parser.parse_known_args()

	parser = argparse.ArgumentParser(parents=[deciding_args_parser])
	parser.add_argument("-i", "--input", required=False, type=argparse.FileType('r'), default=sys.stdin)
	parser.add_argument("-v", "--verbose", required=False, action='store_true', default=False)
	parser.add_argument("-t", "--type", required=not deciding_args.decode, action='store', choices=valid_headers)
	args = parser.parse_args()
	if args.decode:
		for line in args.input.readlines():
			output = dc.decode_header(line, args.type, args.verbose)
			print(json.dumps(output, indent=4))
	else:
		print(en.encode_header(args.input.read(), args.type))
