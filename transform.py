#!/bin/python3

import encode as en
import decode as dc
import argparse
import json
import sys

valid_headers = {"9201", "2E01"}

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", required=False, type=argparse.FileType('r'), default=sys.stdin)
	parser.add_argument("-d", "--decode", required=False, action='store_true', default=False)
	parser.add_argument("-v", "--verbose", required=False, action='store_true', default=False)
	parser.add_argument("-t", "--type", required=False, action='store', choices=valid_headers)
	args = parser.parse_args()
	if args.decode:
		for line in args.input.readlines():
			output = dc.decode_header(line, args.type, args.verbose)
			print(json.dumps(output, indent=4))
	else:
		decoder = json.JSONDecoder();
		inputs = args.input.read().strip();
		while len(inputs):
			json_obj, offset = decoder.raw_decode(inputs)
			if args.verbose:
				print(f"{offset} characters to decode", file=sys.stderr)
			print(en.encode_header(json_obj, args.type))
			inputs = inputs[offset:].strip()
			if args.verbose:
				print(f"now decoding `{inputs}`", file=sys.stderr)
