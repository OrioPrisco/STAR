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
def	decode_data(line, index, **kwargs):
	og_index = index
	key = kwargs.pop("key", "")
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
		chars,value =  decode_data(line, index, key=key)
		index += chars
		return (index - og_index, key, value)

def	decode_9201(line, *args, **kwargs):
	assert line[0:4] == "9201", f"Unknown header : {line[index:index+4]}, can only decode 9201"
	debug = kwargs.pop("debug", 0)
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

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--debug", required=False, action='store_true', default=False)
	args = parser.parse_args()
	line = input()
	print(json.dumps(decode_9201(line, debug=args.debug), indent=4))
