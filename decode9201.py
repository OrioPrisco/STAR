#!/bin/python3

#https://stackoverflow.com/questions/5574702/how-do-i-print-to-stderr-in-python/14981125#14981125
import sys
import binascii
import struct

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

"""
returns chars decoded
only prints the data and not the length
it's ascii'
"""
def entry_type01(line, index):
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
def  entry_type00(line, index):
	print(struct.unpack('d', binascii.unhexlify(line[index+6:index+22]))[0], end="")
	return (22)

def	print_entry(line, index):
	og_index = index
	entry_type = int(line[index:index+2])
	index += 2
	if (entry_type == 0):
		index += entry_type00(line, index)
	elif (entry_type == 1):
		index += entry_type01(line, index)
	else:
		eprint("Unknown entry format {line[index-2:index]}")
		exit(1)
	return (index - og_index)

index = 0;
line = input()
if (line[index:index+4] != "9201"):
	eprint(f"Unknown header : {line[index:index+4]}, can only decode 9201")
	exit(1)
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
