import openpyxl
from datetime import date, datetime
import sys
import os
import re
import numpy as np
import config
import bytesTpl



ARRAY_SPLITTER = '#'

arry32 = ['int', 'int32', 'sint32', 'sfixed32']
arryu32 = ['uint','uint32', 'fixed32']
arry64 =  ['int64', 'double','sint64', 'sfixed64']
arryu64 = ['uint64', 'fixed64']
def trimDotZeroes(text):
	if isinstance(text, str):
		text = text.strip()
		if text == "": return 0
		return re.sub("\.0+$", "", text)
	return text

def get_real_value(data_type, raw_value):
	if not raw_value :
		return None
	# print('data_type: ', data_type, 'raw_value:', raw_value)
	if data_type == 'string':
		value = str(raw_value)
		value = value.replace('\\', '\\\\')
		return '''{}'''.format(value)
	elif data_type in arry32:
		return np.int32(trimDotZeroes(raw_value))
	elif data_type in arryu32:
		return np.uint32(trimDotZeroes(raw_value))
	elif data_type in arry64:
		return np.int64(trimDotZeroes(raw_value))
	elif data_type in arryu64:
		return np.uint64(trimDotZeroes(raw_value))
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

def read_excel_sheet(sheet):
	variable_dict = {}
	variable_index = {}
	variable_defaultValue_dict = {}
	sheet_name = sheet.title
	mod_name = sheet_name
	data_col_count = sheet.max_column#列数
	for col_num in range(0, data_col_count):
		col_num += 1
		namecell  = sheet._get_cell(config.NAME_ROW, col_num)
		if not namecell.value:
			continue
		name_data = str(namecell.value)
		if name_data == None or name_data.strip() == "": continue

		if name_data =='getway':
			pass

		typecell  = sheet._get_cell(config.TYPE_ROW, col_num)
		if not typecell.value:
			continue
		type_data = str(typecell.value).split(':')
		if name_data == None or type_data[0].strip() == "": continue

		variable_name = name_data[0].upper() + name_data[1:]
		row_type_data = config.GetCustomTypeValue(type_data[0])
		if variable_name in variable_dict:
			print('存在相同的字段名: ', variable_name)
			print('异常退出')
			sys.exit()
		if not config.CheckSupportType(row_type_data):
			continue
		variable_dict[variable_name] = row_type_data
		variable_index[variable_name] = col_num
		
		typeLen = len(type_data)
		if typeLen == 2:
			variable_defaultValue_dict[variable_name] = type_data[1]
			print(variable_name,"此处有默认值")
		else:
			variable_defaultValue_dict[variable_name] = "NULL"

	data_row_count = sheet.max_row

	sheet_row_data_list = []
	for row_data in sheet.iter_rows(min_row=config.DATA_ROW, max_row=data_row_count, min_col=1, max_col=data_col_count):
		# 存储每一个字段的字段名，数值，类型
		single_row_data = []
		
		for variable_name in variable_dict:
			variable_type = variable_dict[variable_name]
			index = variable_index[variable_name]
			#print(variable_name, variable_type, row_data[index].value)
			variable_value = get_real_value(variable_type, row_data[index -1].value)
			variable_def_calue = variable_defaultValue_dict[variable_name]
			if variable_def_calue == "NULL":
				variable_def_calue = variable_defaultValue_dict[variable_name]
			else:
				variable_def_calue = get_real_value(variable_type, variable_def_calue)
				if variable_def_calue != variable_value:
					variable_def_calue = "NULL"
			# print(variable_name, variable_type, variable_value)
			index += 1
			data_dict = {
				'field_name': variable_name,
				'field_value': variable_value,
				'field_type': variable_type,
				'field_def': variable_def_calue
			}
			single_row_data.append(data_dict)
		sheet_row_data_list.append(single_row_data)
	generate_bytes(mod_name, sheet_row_data_list)

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

def generate_bytes(mod_name, excel_row_list):
	bytes_file_root_path = config.GetRootBytes()
	allRowCodes = get_list_data_code(excel_row_list)
	byte_file_path = config.GetFullPathExtension(bytes_file_root_path, mod_name,config.scriptExtDict['bytes'])
	byte_file_path = byte_file_path.replace('\\', '/')
	code = bytesTpl.getPythonCode(f"{config.GEN_DIR_DICT['python']}.{mod_name}_pb2",mod_name, allRowCodes,byte_file_path)
	# print(code)
	# if os.path.exists(f"{mod_name}_pb.py"):
	# 	os.remove(f"{mod_name}_pb.py")
	# file = open(f"{mod_name}_pb.py", 'a', encoding='utf-8')
	# file.write(code)
	# file.close()
	try:
		exec(code)
		# print('生成成功: ', byte_file_path)
	except Exception as e:
		print(e)
		print('生成失败: ', byte_file_path)
		if os.path.exists(f"{mod_name}_pb.py"):
			os.remove(f"{mod_name}_pb.py")
			file = open(f"{mod_name}_pb.py", 'a', encoding='utf-8')
			file.write(code)
			file.close()




def generate_excel_data(excel_path):
	wb = openpyxl.load_workbook(excel_path,True, False,True)
	sheet = wb.active
	read_excel_sheet(sheet)


def generate_all_excel_byte_data():
	excels = config.GetFilesByExtension(config.GetRootExcel(), config.scriptExtDict['xlsx'])
	index =  1
	count = len(excels)
	for excel in excels:
		filename = os.path.basename(excel)
		name, ext = os.path.splitext(filename)
		ext = config.scriptExtDict['bytes']
		print(f"[{index}/{count}]  {config.GetRootBytes()}\{name}.{ext}")
		generate_excel_data(config.GetRootExcelFile(excel))
		index += 1


def run():
	print('---------------- 将excel生成flatbuffers二进制数据 ----------------')
	generate_all_excel_byte_data()