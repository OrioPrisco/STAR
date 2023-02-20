#!/bin/python3

import sys
import binascii
import struct
import json
import argparse
import re

hex_regex = r'0x([0-9A-Fa-f]*)'

def	encode_hex_string(data):
	hex_match = re.search(hex_regex, data)
	assert hex_match, f"Not an hex string {data}"
	num = f"{int(hex_match.group(1), 16):016x}".upper()
	assert len(num) == 16, f"Number too big {data}"
	return "00" + "000000" + num

"""
takes a string without qutations marks
returns the encoded representation of that string
"""
def	encode_str(data):
	length = f"{len(data):08x}".upper()
	assert len(length) == 8, f"Error while encoding {data}, length too big"
	data_as_hex = "".join([hex(ord(i))[2:4].upper() for i in data])
	return "01" + length + "000000" + data_as_hex

"""
takes a float
00 + padding + binary representation of float
"""
def	encode_num(data):
	return "00" + "000000" + binascii.hexlify(struct.pack('d', float(data))).decode('utf-8').upper()

def	encode_data(data, **kwargs):
	key = kwargs.pop("key", "")
	if (isinstance(data,str) and "color" in key and re.search(hex_regex, data)):
		return encode_hex_string(data)
	if isinstance(data, str):
		return encode_str(data)
	if isinstance(data, float):
		return encode_num(data)
	assert False, f"Cannot encode {type(data)} : {data}"

def	encode_entry(key, value):
	return encode_data(key) + encode_data(value, key=key)

def	output_all(entries):
	length = f"{len(entries):06x}".upper()
	assert len(length) == 6, f"Error while encoding {data}, length too big"
	print(f"9201{length}000000{''.join(entries)}")

def	encode_all(data):
	json_dict = json.loads(data)
	encoded_dict = []
	for key in json_dict:
		encoded_dict.append(encode_entry(key, json_dict[key]))
	output_all(encoded_dict)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", required=False, type=argparse.FileType('r'), default=sys.stdin)
	args = parser.parse_args()
	encode_all(args.input.read())
