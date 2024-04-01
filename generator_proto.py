import re
import subprocess
import openpyxl
from datetime import date, datetime
from pathlib import Path
import shutil
import time
from ExcelParse import ExcelParse
import config
import protoTpl 
import configcsTpl

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

def writeProto(excelparse):
	proto_path = Path(config.GetRootProto()).joinpath(f"{excelparse.sheetName}.{config.scriptExtDict['proto']}")
	write_str = protoFormat(excelparse)
	config.writeFile(proto_path, write_str)
def protoFormat(excelparse):
	# 组合变量定义代码字符串
	variables_str = ''
	index=1
	for variable in excelparse.variableDict:
		data_type = variable.type
		substr = f"{data_type}"
		if variable.isRepeated():
			substr = f"repeated {data_type}"
		if not variable.isShow():
			substr +="//"
		variables_str += protoTpl.getRowLineCore(substr, variable.name, index)
		index += 1

	variables_str = variables_str.strip(' \t\n\t')
	row_table_name = excelparse.rowTableName.upper()
	row_data_table_code_str = protoTpl.getRowCode(row_table_name, variables_str)
	# 组合列表代码字符串
	group_table_name = excelparse.groupTableName.upper()
	group_data_table_code_str = protoTpl.getGroupcode(row_data_table_code_str,group_table_name, row_table_name)
	return group_data_table_code_str
	
def excel_to_protonew(excel_path):
	excelparse = ExcelParse(excel_path, config.TYPEROW, config.NAMEROW, config.DATAROW, config.PROTOTYPE, config.PROTOSHOW)
	excelparse.readExcel()
	if excelparse.isParseSuccess:
		writeProto(excelparse)

"""
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
		name_datacell = sheet.cell(config.NAMEROW, col_num)
		if not name_datacell.value:
			continue
		name_data = name_datacell.value
		if name_data == None or name_data.strip() == "": continue
		typecell = sheet.cell(config.TYPEROW, col_num)
		if not typecell.value:
			continue
		type_data = typecell.value.split(':')[0]

		# print('表', sheet_name, '字段', name_data, '的数据类型', type_data)
		if type_data == None or type_data.strip() == "": continue
		variable_name = name_data[0].upper() + name_data[1:]
		row_type_data = config.GetCustomTypeValue(type_data)
		if variable_name in variable_dict:
			print('异常退出: ','表', sheet_name, '存在相同的字段名: ', variable_name)
			# sys.exit()
			return

		if not config.CheckSupportType(row_type_data):
			print('表', sheet_name, '字段', variable_name, '的数据类型', row_type_data,'不在支持的列表中')
			# continue
			return

		if col_num == 1:
			data_dict = {
				'field_name': variable_name,
				'field_type': row_type_data,
			}
			config.excelKeyDict[sheet_name]=data_dict
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
	row_data_table_code_str = protoTpl.getRowCode(row_table_name.upper(), variables_str)
	# 组合列表代码字符串
	group_data_table_code_str = protoTpl.getGroupcode(row_data_table_code_str, group_table_name.upper(), row_table_name.upper())
	proto_path = Path(config.GetRootProto()).joinpath(f"{group_table_name}.{config.scriptExtDict['proto']}")
	write_str = group_data_table_code_str #protoTpl.getProtoCode(group_data_table_code_str, row_data_table_code_str)
	config.writeFile(proto_path, write_str)
"""
def generate_target_file(protoDir,proto_file, target_path, language_sign):
	filename,ext = config.GetFileNameExt(proto_file)
	languageOut = getProtocLanguage(language_sign)
	command = f"{config.GetProtoc()} --proto_path {protoDir}  {languageOut}{target_path} {filename}{ext}" 
	# print(command)
	subprocess.call(command, shell=True)

def generate_config(mod_name, config_file_root_path):
	configcs_file_path = config.GetFullPathExtension(config_file_root_path, f"{mod_name}Config",config.scriptExtDict['configcs'])
	configcs_file_path = str(configcs_file_path).replace('\\', '/')
	if len(config.excelKeyDict) < 1:
		print('异常退出: ',mod_name, ' 没有找到主键ID类型')
		return
	keyValue = config.excelKeyDict[mod_name]
	code = configcsTpl.getCsCode(mod_name, keyValue)
	config.writeFile(configcs_file_path, code)

def generate_target(language_sign):
	target_path = config.getGenDirByLanguage(language_sign)
	config.clean_directory(target_path)

	protoDir = config.GetRootProto()
	protos = config.GetFilesByExtension(protoDir, config.scriptExtDict['proto'])
	count = len(protos)
	index = 0
	for proto_file in protos:
		index += 1
		name, ext = proto_file.stem, proto_file.suffix
		ext = config.scriptExtDict[language_sign]
		print(f"[{index}/{count}]  {target_path}\\{name}.{ext}")
		if language_sign == 'configcs':
			generate_config(name, target_path)
			name = f"{name}Config"
		else:
			generate_target_file(protoDir,proto_file, target_path, language_sign)


def genearte_excel_to_proto():
	excels = config.GetFilesByExtension(config.GetRootExcel(), config.scriptExtDict['xlsx'])
	index =  1
	count = len(excels)
	for excel in excels:
		name, ext = excel.stem, excel.suffix
		ext = config.scriptExtDict['proto']
		print(f"[{index}/{count}]  {config.GetRootBytes()}\\{name}.{ext}")
		excel_to_protonew(str(excel))
		index += 1

def clean():
	config.clean_directory(config.GetRootProto())
	config.clean_directory(config.GetRootBytes())

def run():
	#print('---------------- 清理旧文件 ----------------')
	clean()

	print("\n---------------- 生成Proto文件, 生成不同语言代码 ----------------")
	genearte_excel_to_proto()
	print("\n---------------- 开始生成 python代码 ----------------")
	generate_target('python')	# 生成Python代码是必须的，因为要用来打包数据
	print("\n---------------- 开始生成 csharp 代码 ----------------")
	generate_target('csharp')
	# print("\n---------------- 开始生成 config csharp 代码 ----------------")
	# generate_target('configcs')