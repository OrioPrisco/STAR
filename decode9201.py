#!/bin/python3

import binascii
import struct
import json
import sys

"""
returns (chars decoded, string)
only prints the data and not the length
it's ascii'
"""
def decode_str(line, index):
	length = int(line[index:index+8], 16) #length is in bytes, one char is 1 nibble
	index += 8 + 6 #num + padding
	data = line[index:index+(length * 2)]
	data_as_str = "".join([chr(int(data[i*2:(i+1)*2], 16)) for i in range(length)])
	return (8 + 6 + length * 2, data_as_str)

"""
returns (char decoded, num)
these are doubles
"""
def decode_num(line, index):
	num = struct.unpack('d', binascii.unhexlify(line[index+6:index+22]))[0]
	return (22, num)

"""
returns (chars decoded, entry)
"""
def	decode_entry(line, index):
	og_index = index
	entry_type = int(line[index:index+2])
	index += 2
	if (entry_type == 0):
		chars,entry = decode_num(line, index)
	elif (entry_type == 1):
		chars,entry = decode_str(line, index)
	else:
		assert False, f"Unknown entry format {line[index-2:index]}"
	index += chars
	return (index - og_index, entry)

def	print_9201(line):
	assert line[0:4] == "9201", f"Unknown header : {line[index:index+4]}, can only decode 9201"
	entries = {}
	index = 4
	length = int(line[index:index+6], 16)
	index += 6
	print(f"{length} key value pairs", file=sys.stderr)
	index += 6 #padding
	for i in range(length):
		chars,key = decode_entry(line, index)
		index += chars
		chars,value =  decode_entry(line, index)
		index += chars
		entries[key] = value
	print(json.dumps(entries, indent = 4))
	print(f"decoded {index} characters, {len(line) - index} remaining", file=sys.stderr)

if __name__ == "__main__":
	line = input()
	print_9201(line)
