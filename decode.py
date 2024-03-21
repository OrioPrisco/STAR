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

def	decode_9201(line, logger, _ = None):
	index = 0
	assert line[0:4] == "9201", f"Incorrect header : {line[index:index+4]}, expected 9201"
	entries = {}
	index = 4
	length = int(line[index:index+6], 16)
	index += 6
	logger.debug(f"decoding 9201 {length} key value pairs", "")
	index += 6 #padding
	for i in range(length):
		chars,key,value = decode_entry(line, index)
		entries[key] = value
		index += chars
	logger.debug(f"decoded {index} characters, {len(line) - index} remaining", "")
	return entries

def	try_str_from_enum(value, kind=None):
	if (isinstance(value, str)):
		return value
	if kind == None:
		return None
	try:
		return kind(value).name
	except ValueError:
		return None

def decode_enum(value, logger, kind, field=""):
	if field:
		field += ": "
	value_as_str = try_str_from_enum(value, kind)
	if (value_as_str == None and kind):
		message = f"{field}Couldn't convert {value} to a string using kind {kind.__name__ if kind else 'None'}"
		if kind.__name__ == "Unique":
			logger.debug(message, "Not all uniques are currently known, this is pretty normal")
		else:
			logger.warn(message, "If You did not modify your save and got this error, please report it")
		return int(value)
	if (value_as_str == None):
		logger.debug(f"{field}Couldn't convert {value} to a string using no kind", "this is most likely normal")
		return int(value)
	return value_as_str

def	decode_2E01(line, logger, kind = None):
	index = 0
	assert line[0:4] == "2E01", f"Incorrect header : {line[index:index+4]}, expected 2E01"
	entries = []
	index = 4
	length = int(line[index:index+6], 16)
	index += 6
	logger.debug(f"decoding 2E01 {length} values", "")
	index+=6 # padding
	for i in range(length):
		chars,value = decode_data(line, index)
		entries.append(decode_enum(value, logger, kind))
		index+= chars
	logger.debug(f"decoded {index} characters, {len(line) - index} remaining", "")
	return entries

header_decoders = {
	"9201" : decode_9201,
	"2E01" : decode_2E01,
}

valid_headers = header_decoders.keys()

def	decode_header(line, header, logger, kind = None):
	if header == None:
		header = line[0:4]
	assert header in valid_headers, f"Unknown header {header}, expected one of {valid_headers}"
	return header_decoders[header](line, logger, kind)
