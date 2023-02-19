#!/bin/python3

import re
import sys
import binascii
import struct

number_regex = r'\s*([0-9]*\.[0-9]*)\s*'
string_regex = r'\s*"(.*)"\s*'
entire_regex = r'\{(.*)\}' #brackets in the data might mess this ?
entry_regex  = r'([^}]*),?' #% (string_regex, string_regex, number_regex)
ending_regex = r'^\s*}'

"""
takes a string without qutations marks
returns the encoded representation of that string
"""
def	encode_str(data):
	length = f"{len(data):08x}".upper()
	assert len(length) == 8, f"Error while encoding {data}, length too big"
	data_as_hex = "".join([hex(ord(i))[2:4].upper() for i in data])
	return "01" + length + data_as_hex

"""
takes a float
00 + padding + binary representation of float
"""
def	encode_number(data):
	return "00" + "000000" + binascii.hexlify(struct.pack('d', float(data))).decode('utf-8')

"""
takes an entry in the following format
"field name" : value
"""
def	encode_entry(data):
	key_match = re.search(r'%s:' % string_regex, data)
	assert key_match, f"Cannot find key in {data}"
	key = encode_str(data[key_match.start(1):key_match.end(1) + 1])
	assert key_match.end() + 1 < len (data), f"No value in {data}"
	value_str = re.search(r'%s,?' % string_regex, data)
	value_num = re.search(r'%s,?' % number_regex, data)
	assert value_str or value_num, f"cannot decode {data}"
	if (value_str):
		value = encode_str(data[value_str.start(1):value_str.end(1) + 1])
	else:
		value = encode_num[data[value_num.start(1):value_num.end(1) + 1]]
	return key + value

def	output_all(entries):
	length = f"{len(entries):06x}".upper()
	assert len(length) == 6, f"Error while encoding {data}, length too big"
	print(f"9201{length}000000{''.join(entries)}")


def	encode_all(data):
	entries = []
	entire_match = re.search(entire_regex, data, flags=re.DOTALL);
	assert entire_match, "Doesnt look like good data"
	to_encode = data[entire_match.start(1):entire_match.end(1) + 1]
	while(1):
		next_entry = re.search(entry_regex, to_encode, flags=re.DOTALL)
		match_end  = re.search(ending_regex, to_encode)
		if (match_end):
			return output_all(entries)
		assert next_entry, f"Malformed data at {to_encode}"
		entries.append(encode_entry(to_encode[next_entry.start(1):next_entry.end(1) + 1]))
		to_encode = to_encode[next_entry.end(1):]

if __name__ == "__main__":
	to_encode = sys.stdin.read()
	encode_all(to_encode)
