#!/usr/bin/env python3

import binascii
import struct
import re

hex_regex = re.compile(r"0x([0-9A-Fa-f]*)")


def encode_hex_string(data):
	hex_match = hex_regex.search(data)
	assert hex_match, f"Not an hex string {data}"
	num = f"{int(hex_match.group(1), 16):016x}".upper()
	assert len(num) == 16, f"Number too big {data}"
	return "00" + "000000" + num


def encode_str(data):
	"""
	takes a string without qutations marks
	returns the encoded representation of that string
	"""
	length = f"{len(data):08x}".upper()
	assert len(length) == 8, f"Error while encoding {data}, length too big"
	data_as_hex = "".join([hex(ord(i))[2:4].upper() for i in data])
	return "01" + length + "000000" + data_as_hex


def encode_num(data):
	"""
	takes a float
	00 + padding + binary representation of float
	"""
	return (
		"00"
		+ "000000"
		+ binascii.hexlify(struct.pack("d", float(data))).decode("utf-8").upper()
	)


def encode_data(data, key = ""):
	if isinstance(data, str) and "color" in key and hex_regex.search(data):
		return encode_hex_string(data)
	if isinstance(data, str):
		return encode_str(data)
	if isinstance(data, float):
		return encode_num(data)
	if isinstance(data, int):
		return encode_num(data)
	assert False, f"Cannot encode {type(data)} : {data}"


def encode_entry(key, value):
	return encode_data(key) + encode_data(value, key)


def output_all(entries, header):
	length = f"{len(entries):06x}".upper()
	assert len(length) == 6, f"Error while encoding {entries}, length too big"
	return f"{header}{length}000000{''.join(entries)}"


def encode_9201(json_dict, _logger, _ = None):
	assert isinstance(
		json_dict, dict
	), f"9201 encoder can only encode dicts, not {type(json_dict).__name__}"
	encoded_dict = []
	for key in json_dict:
		encoded_dict.append(encode_entry(key, json_dict[key]))
	return output_all(encoded_dict, "9201"), False


def try_int_from_enum(value, kind = None):
	if isinstance(value, (int, float)):
		return value
	if kind == None:
		return None
	try:
		return kind[value.lower()].value
	except KeyError:
		return None


def encode_2E01(json_array, logger, kind = None):
	assert isinstance(
		json_array, list
	), f"2E01 encoder can only encode arrays, not {type(json_array).__name__}"
	encoded_array = []
	err = []
	for item in json_array:
		item_as_int = try_int_from_enum(item, kind)
		if item_as_int == None:
			err.append(item)
			if logger.interactive:
				logger.warn(f"couldn't convert {item} to an integer value", "")
			else:
				logger.debug(f"couldn't convert {item} to an integer value", "")
		else:
			item = item_as_int
		encoded_array.append(encode_data(item))
	return output_all(encoded_array, "2E01"), err


header_encoders = {
	"9201": encode_9201,
	"2E01": encode_2E01,
}

valid_headers = header_encoders.keys()


def encode_header(data, header, logger, kind = None):
	if header == None:
		if isinstance(data, dict):
			header = "9201"
		elif isinstance(data, list):
			header = "2E01"
	assert (
		header in valid_headers
	), f"Unknown header {header}, expected one of {valid_headers}"
	return header_encoders[header](data, logger, kind)
