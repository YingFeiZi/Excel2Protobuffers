import re
import subprocess
import openpyxl
from datetime import date, datetime
import sys
import os
import shutil
import time
import config
import protoTpl 

def getProtocLanguage(language_sign):
	if language_sign == 'cpp':
		return "--cpp_out="
	if language_sign == 'csharp':
		return "--csharp_out="
	if language_sign == 'java':
		return "--java_out="
	if language_sign == 'kotlin':
		return "--kotlin_out="
	if language_sign == 'objc':
		return "--objc_out="
	if language_sign == 'php':
		return "--php_out="
	if language_sign == 'pyi':
		return "--pyi_out="
	if language_sign == 'python':
		return "--python_out="
	if language_sign == 'ruby':
		return "--ruby_out="
	if language_sign == 'rust':
		return "--rust_out="

def excel_to_proto(excel_path):
	wb = openpyxl.load_workbook(excel_path,True, False,True)
	sheet = wb.active
	readsheet(sheet)

def readsheet(sheet):
	variable_dict = {}
	variable_defaultValue_dict = {}
	# sheet_name = sheet.name
	sheet_name = sheet.title
	row_table_name = sheet_name
	group_table_name = f"{sheet_name}"
	data_col_count = sheet.max_column#列数
	for col_num in range(0, data_col_count):
		col_num += 1
		name_datacell = sheet.cell(config.NAME_ROW, col_num)
		if not name_datacell.value:
			continue
		name_data = name_datacell.value
		if name_data == None or name_data.strip() == "": continue
		typecell = sheet.cell(config.TYPE_ROW, col_num)
		if not typecell.value:
			continue
		type_data = typecell.value.split(':')[0]

		# print('表', sheet_name, '字段', name_data, '的数据类型', type_data)
		if type_data == None or type_data.strip() == "": continue
		variable_name = name_data[0].upper() + name_data[1:]
		row_type_data = config.GetCustomTypeValue(type_data)
		if variable_name in variable_dict:
			print('异常退出: ','表', sheet_name, '存在相同的字段名: ', variable_name)
			sys.exit()

		if not config.CheckSupportType(row_type_data):
			print('表', sheet_name, '字段', variable_name, '的数据类型', row_type_data,'不在支持的列表中')
			continue
		variable_dict[variable_name] = row_type_data

		variable_defaultValue_dict[variable_name] = "NULL"

	# 组合变量定义代码字符串
	variables_str = ''
	index=1
	for variable in variable_dict:
		data_type = variable_dict[variable]
		isArry, subType = config.GetEnableArrylistValue(data_type)
		subType = isArry and  subType or data_type
		variables_str += protoTpl.getRowLineCore(subType, variable, index, isArry)
		index += 1
	variables_str = variables_str.strip(' \t\n\t')
	row_data_table_code_str = protoTpl.getRowCode(row_table_name, variables_str)
	# 组合列表代码字符串
	group_data_table_code_str = protoTpl.getGroupcode(group_table_name, row_table_name)
	proto_path = os.path.join(config.GetRootProto(), f"{group_table_name}.{config.scriptExtDict['proto']}")
	write_str = protoTpl.getProtoCode(group_data_table_code_str, row_data_table_code_str)
	writeProto(proto_path, write_str)
 
def writeProto(path, context):
	# 写入文件
	print(path)
	with open(path, 'w') as f:
		f.write(context)


def generate_target_file(protoDir,proto_file, target_path, language_sign):
	filename,ext = config.GetFileNameExt(proto_file)
	languageOut = getProtocLanguage(language_sign)
	command = f"{config.GetProtoc()} --proto_path {protoDir}  {languageOut}{target_path} {filename}{ext}" 
	# print(command)
	subprocess.call(command, shell=True)


def generate_target(language_sign):
	target_path = config.getGenDirByLanguage(language_sign)
	config.clean_directory(target_path)

	protoDir = config.GetRootProto()
	protos = config.GetFilesByExtension(protoDir, config.scriptExtDict['proto'])
	count = len(protos)
	index = 0
	for proto_file in protos:
		index += 1
		generate_target_file(protoDir,proto_file, target_path, language_sign)
		filename = os.path.basename(proto_file)
		name, ext = os.path.splitext(filename)
		ext = config.scriptExtDict[language_sign]
		print(f"[{index}/{count}]  {target_path}\{name}.{ext}")


def genearte_excel_to_proto():
	excels = config.GetFilesByExtension(config.GetRootExcel(), config.scriptExtDict['xlsx'])
	for excel in excels:
		excel_to_proto(config.GetRootExcelFile(excel))


def clean():
	config.clean_directory(config.GetRootProto())
	config.clean_directory(config.GetRootBytes())

def run():
	#print('---------------- 清理旧文件 ----------------')
	clean()

	print('---------------- 生成Proto文件, 生成不同语言代码 ----------------')
	genearte_excel_to_proto()
	print('---------------- 开始生成 python代码 ----------------')
	generate_target('python')	# 生成Python代码是必须的，因为要用来打包数据
	print('---------------- 开始生成 csharp 代码 ----------------')
	generate_target('csharp')