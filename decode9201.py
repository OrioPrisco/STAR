#!/bin/python3

import binascii
import struct

"""
returns chars decoded
only prints the data and not the length
it's ascii'
"""
def decode_str(line, index):
	length = int(line[index:index+8], 16) #length is in bytes, one char is 1 nibble
	index += 8 + 6 #num + padding
	data = line[index:index+(length * 2)]
	data_as_str = "".join([chr(int(data[i*2:(i+1)*2], 16)) for i in range(length)])
	print(f"\"{data_as_str}\"", end = "")
	return (8 + 6 + length * 2)

"""
returns char decoded
these are doubles
"""
def decode_num(line, index):
	print(struct.unpack('d', binascii.unhexlify(line[index+6:index+22]))[0], end="")
	return (22)

def	print_entry(line, index):
	og_index = index
	entry_type = int(line[index:index+2])
	index += 2
	if (entry_type == 0):
		index += decode_num(line, index)
	elif (entry_type == 1):
		index += decode_str(line, index)
	else:
		assert false, "Unknown entry format {line[index-2:index]}"
	return (index - og_index)

def	print_9201(line):
	index = 0
	print(line[index:index+4])#header
	index += 4
	entries = int(line[index:index+6], 16)
	index += 6
	print(f"{entries} key value pairs")
	index += 6 #padding
	print("{")
	for i in range(entries):
		index += print_entry(line, index)
		print("\t:\t", end="")
		index += print_entry(line, index)
		if (i != entries - 1):
			print(",")
	print("\n}")
	print(f"decoded {index} characters, {len(line) - index} remaining")

if __name__ == "__main__":
	line = input()
	assert line[0:4] == "9201", f"Unknown header : {line[index:index+4]}, can only decode 9201"
	print_9201(line)
