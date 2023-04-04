#!/bin/python3

import binascii
import struct
import json
import sys
import argparse

"""
returns (chars decoded, string)
"""
def decode_str(line, index):
	length = int(line[index:index+8], 16) #length is in bytes, one char is 1 nibble
	index += 8 + 6 #num + padding
	data = line[index:index+(length * 2)]
	data_as_str = "".join([chr(int(data[i*2:(i+1)*2], 16)) for i in range(length)])
	return (8 + 6 + length * 2, data_as_str)

"""
returns (char decoded, num)
"""
def decode_num(line, index):
	num = struct.unpack('d', binascii.unhexlify(line[index+6:index+22]))[0]
	return (22, num)

"""
returns (char decoded, hex_str)
"""
def decode_hex_str(line, index):
	return (22, "0x"+line[index+6:index+22])

"""
returns (chars decoded, data)
"""
def	decode_data(line, index, key = ""):
	og_index = index
	entry_type = int(line[index:index+2])
	index += 2
	if (entry_type == 0):
		if ("color" in key):
			chars,entry = decode_hex_str(line, index)
		else:
			chars,entry = decode_num(line, index)
	elif (entry_type == 1):
		chars,entry = decode_str(line, index)
	else:
		assert False, f"Unknown entry format {line[index-2:index]}"
	index += chars
	return (index - og_index, entry)

"""
returns (chars decoded, key, value)
"""
def	decode_entry(line, index):
		og_index = index
		chars,key = decode_data(line, index)
		index += chars
		chars,value =  decode_data(line, index, key)
		index += chars
		return (index - og_index, key, value)

def	decode_9201(line, debug = False):
	index = 0
	assert line[0:4] == "9201", f"Incorrect header : {line[index:index+4]}, expected 9201"
	entries = {}
	index = 4
	length = int(line[index:index+6], 16)
	index += 6
	if debug:
		print(f"{length} key value pairs", file=sys.stderr)
	index += 6 #padding
	for i in range(length):
		chars,key,value = decode_entry(line, index)
		entries[key] = value
		index += chars
	if debug:
		print(f"decoded {index} characters, {len(line) - index} remaining", file=sys.stderr)
	return entries

def	decode_2E01(line, debug = False):
	index = 0
	assert line[0:4] == "2E01", f"Incorrect header : {line[index:index+4]}, expected 2E01"
	entries = []
	index = 4
	length = int(line[index:index+6], 16)
	index += 6
	if debug:
		print(f"{length} values", file=sys.stderr)
	index+=6 # padding
	for i in range(length):
		chars,value = decode_data(line, index)
		entries.append(value)
		index+= chars
	if debug:
		print(f"decoded {index} characters, {len(line) - index} remaining", file=sys.stderr)
	return entries

header_decoders = {
	"9201" : decode_9201,
	"2E01" : decode_2E01,
}

valid_headers = header_decoders.keys()

def	decode_header(line, header, debug = False):
	assert header in valid_headers, f"Unknown header {header}, expected one of {valid_headers}"
	return header_decoders[header](line, debug)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--debug", required=False, action='store_true', default=False)
	parser.add_argument("-t", "--type", required=False, action='store', choices=valid_headers, default="9201")
	args = parser.parse_args()
	line = input()
	output = decode_header(line, args.type, args.debug)
	print(json.dumps(output, indent=4))
