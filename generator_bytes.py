import sys
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
sys.path.append(f"{Path.cwd()}")
# sys.path.append(f"{Path.cwd().joinpath('../Python3.11.7/Lib/site-packages')}")

ARRAY_SPLITTER = '#'
arry32 = ['int', 'int32', 'sint32', 'sfixed32']
arryu32 = ['uint','uint32', 'fixed32']
arry64 =  ['int64', 'double','sint64', 'sfixed64']
arryu64 = ['uint64', 'fixed64']

def get_real_value(data_type, raw_value):
	if not raw_value :
		return None
	# print('data_type: ', data_type, 'raw_value:', raw_value)
	if data_type == 'string':
		value = str(raw_value)
		value = value.replace('\\', '\\\\')
		return '''{}'''.format(value)
	elif data_type in arry32:
		return np.int32(trimDotZeroes(raw_value)) # type: ignore
	elif data_type in arryu32:
		return np.uint32(trimDotZeroes(raw_value)) # type: ignore
	elif data_type in arry64:
		return np.int64(trimDotZeroes(raw_value)) # type: ignore
	elif data_type in arryu64:
		return np.uint64(trimDotZeroes(raw_value)) # type: ignore
	elif data_type == 'float':
		return float(raw_value)
	elif data_type == 'bool':
		return bool(raw_value)
	elif data_type in config.ENABLEARRYLIST:
		return str(raw_value)
	else:
		return None

def trimDotZeroes(text):
	if isinstance(text, str):
		text = text.strip()
		if text == "": return 0
		return re.sub("\.0+$", "", text)
	return text

def get_single_data_code(index, row_data):
	variable_create_code = ''
	for field in row_data:
		fvalue = field['field_value']
		if fvalue == None:
			continue
		ftype = field['field_type']
		fname = field['field_name']

		
  
		if ftype == 'string':
			variable_create_code += bytesTpl.getRowCode(index, fname, fvalue, True)
		elif ftype in config.ENABLEARRYLIST:
			valueArrs = fvalue.split(ARRAY_SPLITTER)
			valueArrsLen = len(valueArrs)
			subType = re.sub(r"\[|\]","", ftype)
			for curIndex in range(valueArrsLen):
				isstring =  subType == 'string'
				variable_create_code += bytesTpl.getRowCode(index, fname, valueArrs[curIndex], isstring, True)
		else:
			variable_create_code += bytesTpl.getRowCode(index, fname, fvalue)

	return variable_create_code

def get_list_data_code(excel_row_list):
	allRowCodes=''
	index=0
	for RowData in excel_row_list:
		rowcodes = get_single_data_code(index,RowData)
		allRowCodes += bytesTpl.getAddRowCode(index, rowcodes)
		index += 1
	return allRowCodes

##############################################################################################################################
def get_list_data_code_new(excel_row_list):
	allRowCodes=''
	index=0
	for RowData in excel_row_list:
		rowcodes = get_single_data_code_new(index,RowData)
		allRowCodes += bytesTpl.getAddRowCode(index, rowcodes)
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
		ftype = data.type
		fname = data.name
		
		isRepeated = data.isRepeated()
		if isRepeated:
			valueArrsLen = len(data.arrayvalue)
			for curIndex in range(valueArrsLen):
				isstring =  ftype == 'string'
				variable_create_code += bytesTpl.getRowCode(index, fname, data.arrayvalue[curIndex], isstring, True)
		else:
			isstring =  ftype == 'string'
			variable_create_code += bytesTpl.getRowCode(index, fname, fvalue, isstring, False)
	return variable_create_code

def byteFormat(parse):
	# 组合变量定义代码字符串)
	mod_name = parse.sheetName
	excel_row_list  = parse.sheet_row_data_list
	bytes_file_root_path = config.GetRootBytes()
	allRowCodes = get_list_data_code_new(excel_row_list)
	byte_file_path = config.GetFullPathExtension(bytes_file_root_path, mod_name,config.scriptExtDict['bytes'])
	byte_file_path = str(byte_file_path).replace('\\', '/')
	code = bytesTpl.getPythonCode(config.GEN_DIR_DICT['python'], f"{mod_name}_pb2",mod_name.upper(), allRowCodes,byte_file_path)

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
		# config.writeFile(f"{mod_name}.py", code)
		exec(code)
	except Exception as e:
		print(e)
		print('生成失败: ', byte_file_path)
		config.writeFile(f"{mod_name}_pb2.py", code)
		# if os.path.exists(f"{mod_name}_pb2.py"):
		# 	os.remove(f"{mod_name}_pb2.py")
		# 	file = open(f"{mod_name}_pb2.py", 'a', encoding='utf-8')
		# 	file.write(code)
		# 	file.close()
def generate_excel_data_new(path):
	parse = ExcelParse(path, config.TYPEROW, config.NAMEROW, config.DATAROW, config.PROTOTYPE, config.PROTOSHOW)
	parse.readExcel()
	if parse.isParseSuccess:
		byteFormat(parse)

##############################################################################################################################

def generate_all_excel_byte_data():
	excels = config.GetFilesByExtension(config.GetRootExcel(), config.scriptExtDict['xlsx'])
	index =  1
	count = len(excels)
	for excel in excels:
		name, ext = excel.stem, excel.suffix
		ext = config.scriptExtDict['bytes']
		print(f"[{index}/{count}]  {config.GetRootBytes()}\\{name}.{ext}")
		generate_excel_data_new(str(excel))
		index += 1

def run():
	print('---------------- 将excel生成Protouf二进制数据 ----------------')
	# for p in sys.path:
	# 	print(p)
	generate_all_excel_byte_data()