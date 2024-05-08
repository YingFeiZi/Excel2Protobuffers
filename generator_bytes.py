import imp
import sys
import google.protobuf.descriptor
import openpyxl
import google.protobuf
from datetime import date, datetime
from pathlib import Path
import re
import numpy as np
from ExcelParse import ExcelParse
import config
import bytesTpl
import importlib
import os
import Encrypted
from ExcelDescriptor import ExcelDescriptor

sys.path.append(f".\\{config.GEN_DIR_DICT['python']}")
# sys.path.append(f"{config.work_root}\\{config.GEN_DIR_DICT['python']}")
# sys.path.append(f"{Path.cwd().joinpath('../Python3.11.7/Lib/site-packages')}")

##############################################################################################################################
def PareProtoDesc(pb2, entry_name):
	module = __import__(pb2)
	proto_desc = []
	# alias FieldDescriptor
	FieldDescriptor = google.protobuf.descriptor.FieldDescriptor
	cls = getattr(module, entry_name)
	DESCRIPTOR = cls.DESCRIPTOR
	for desc in DESCRIPTOR.fields:
		if desc.number > 99:
			continue
		field_name = desc.name
		if field_name[0] == '_':
			continue

		field_number = desc.number
		field_label = desc.label
		field_type = None
		if desc.type == desc.TYPE_INT32 or \
				desc.type == desc.TYPE_INT64 or \
				desc.type == desc.TYPE_SINT32 or \
				desc.type == desc.TYPE_SINT64 or \
				desc.type == desc.TYPE_FIXED32 or \
				desc.type == desc.TYPE_FIXED64 or \
				desc.type == desc.TYPE_UINT32 or \
				desc.type == desc.TYPE_UINT64 or \
				desc.type == desc.TYPE_ENUM :
			field_type = int
		elif desc.type == desc.TYPE_BOOL:
			field_type = bool
		elif desc.type == desc.TYPE_FLOAT:
			field_type = float
		elif desc.type == desc.TYPE_BYTES or \
				desc.type == desc.TYPE_STRING:
			field_type = str
		elif desc.type == desc.TYPE_MESSAGE:
			msg_desc = desc.message_type
			field_type = msg_desc.name
			# if msg_desc.name == "ItemDrop":
				# field_type = table_common_pb2.ItemDrop
			# else:
				# print("bad field type: " + msg_desc.name)

		proto_desc += [(field_name, field_number, field_type, field_label)]
	print("proto_desc = " ,str(proto_desc))


def get_list_data_code_new(excel_row_list, tableName):
	allRowCodes=''
	index=0
	for RowData in excel_row_list:
		rowcodes = get_single_data_code_new(index,RowData)
		allRowCodes += bytesTpl.getAddRowCode(index, tableName.upper(), rowcodes)
		index += 1
	return allRowCodes

def get_single_data_code_new(index, row_data):
	variable_create_code = ''
	for data in row_data:
		if not data.isShow():
			continue
		fvalue = data.value
		if fvalue == None and len(data.arrayvalue) < 1:
			continue
		variable_create_code += data.toByte(index)
		
		# ftype = data.type
		# fname = data.name
		# isRepeated = data.isRepeated()
		# if config.CheckDefaultType(ftype):
		# 	if isRepeated:
		# 		valueArrsLen = len(data.arrayvalue)
		# 		for curIndex in range(valueArrsLen):
		# 			variable_create_code += bytesTpl.getRowCode(index, fname, data.arrayvalue[curIndex], True)
		# 	else:
		# 		variable_create_code += bytesTpl.getRowCode(index, fname, fvalue, False)
		# else:
		# 	# print(ftype)
		# 	datas = config.GetCustomTypeList(ftype)

	return variable_create_code

def byteFormat(parse):
	# 组合变量定义代码字符串)
	mod_name = parse.sheetName
	excel_row_list  = parse.sheet_row_data_list
	bytes_file_root_path = config.GetRootBytes()
	allRowCodes = get_list_data_code_new(excel_row_list , mod_name)
	byte_file_path = config.GetFullPathExtension(bytes_file_root_path, mod_name,config.scriptExtDict['bytes'])
	byte_file_path = str(byte_file_path).replace('\\', '/')
	pb = config.GEN_DIR_DICT['python']
	code = bytesTpl.getPythonCode(pb, f"{mod_name}_pb2",mod_name.upper(), allRowCodes,byte_file_path, parse.hasCommon)

	# config.writeFile(f"{mod_name}_pb2.py", code)
	# try:
	# 	module = importlib.import_module(f"{mod_name}_pb2")
	# except ImportError as e:
	# 	print(f"Failed to import {mod_name}_pb2: {e}")
	# else:
	# 	module.Write()
	# return

	try:
		# print(f"{str(Path.cwd())}\\{mod_name}.py")
		config.writeFile(f"{mod_name}_gen.py", code)
		# pbroot = Path.joinpath(config.work_root, pb)
		# os.chdir(pbroot)
		exec(code)
		# PareProtoDesc(f"{config.GEN_DIR_DICT['python']}.{mod_name}_pb2", mod_name.upper())
		# PareProtoDesc(f"{mod_name}_pb2", mod_name.upper())
	except Exception as e:
		print(e)
		print('生成失败: ', byte_file_path)
		config.writeFile(f"{mod_name}_gen.py", code)
		# if os.path.exists(f"{mod_name}_pb2.py"):
		# 	os.remove(f"{mod_name}_pb2.py")
		# 	file = open(f"{mod_name}_pb2.py", 'a', encoding='utf-8')
		# 	file.write(code)
		# 	file.close()
	# os.chdir(config.work_root)
	
def generate_excel_data_new(path):
	parse = ExcelParse(path, config.TYPEROW, config.NAMEROW, config.DATAROW, config.PROTOTYPE, config.PROTOSHOW)
	parse.readExcel()
	if parse.isParseSuccess:
		byteFormat(parse)

def generate_excel_data_desc(path):
	parse = ExcelDescriptor(path, config.TYPEROW, config.NAMEROW, config.DATAROW, config.PROTOTYPE, config.PROTOSHOW)
	parse.readExcel()
	if parse.isParseSuccess:
		byte_file_path = config.GetFullPathExtension(config.GetRootBytes(), parse.sheetName,config.scriptExtDict['bytes'])
		byte_file_path = str(byte_file_path).replace('\\', '/')
		parse.Write(byte_file_path)

##############################################################################################################################

def generate_all_excel_byte_data():
	excels = config.GetFilesByExtension(config.GetRootExcel(), config.scriptExtDict['xlsx'])
	index =  1
	count = len(excels)
	# os.chdir(config.work_root)
	for excel in excels:
		name, ext = excel.stem, excel.suffix
		ext = config.scriptExtDict['bytes']
		print(f"<br>[{index}/{count}]  {config.GetRootBytes()}\\{name}.{ext}")
		# generate_excel_data_new(str(excel))
		generate_excel_data_desc(str(excel))
		index += 1

def run():
	print('<br>---------------- 将excel生成Protouf二进制数据 ----------------')
	# for p in sys.path:
	# 	print(p)
	generate_all_excel_byte_data()