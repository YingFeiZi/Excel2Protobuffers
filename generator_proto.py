import re
import subprocess
from numpy import array_split
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
			substr ="//"+substr
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

def generate_target_file(protoDir,proto_file, target_path, language_sign):
	filename,ext = config.GetFileNameExt(proto_file)
	languageOut = getProtocLanguage(language_sign)
	command = f"{config.GetProtoc()} --proto_path {protoDir}  {languageOut}{target_path} {filename}{ext}" 
	# print(command)
	# subprocess.call(command, shell=True)
	try:
		output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
		print(output)
	except subprocess.CalledProcessError as e:
		print(f"Command failed : {e.returncode}:")
		print(e.output)

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
def genearte_common_to_proto():
	messages =[]
	for v in config.CUSTOM_TYPES:
		customvalue = config.GetCustomTypeValue(v)
		if not config.CheckDefaultType(customvalue):
			arrys = config.GetCustomTypeList(customvalue)
			if not arrys == None:
				variables_str=''
				for arr in arrys:
					index = arr[0]
					substr = f"{arr[1]} {arr[2]}"
					variables_str += protoTpl.getRowLineCore(substr, arr[3], index)
				messagestr = protoTpl.getRowCode(customvalue, variables_str)
				messages.append(messagestr)

			# section = config.customini.get_section_options(customvalue)
			# if len(section) > 0:
			# 	index=1
			# 	variables_str=''
			# 	for v2 in section:
			# 		op = config.customini.get_option(v2)
			# 		# repeated#uint64#list
			# 		arr = str(op).split('#')
			# 		print(op)
			# 		if len(arr) < 3 :
			# 			continue
			# 		substr = f"{arr[0]} {arr[1]}"
			# 		variables_str += protoTpl.getRowLineCore(substr, arr[2], index)
			# 		index += 1
			# 	messagestr = protoTpl.getRowCode(customvalue, variables_str)
			# 	messages.append(messagestr)
	if len(messages)>0:
		messagestrs =''
		for msg in messages:
			messagestrs += msg
		comproto = protoTpl.getGroupcode2(messagestr, False)
		common = Path(config.GetRootProto()).joinpath(f"table_common.{config.scriptExtDict['proto']}")
		config.writeFile(common, comproto)


def clean():
	config.clean_directory(config.GetRootProto())
	config.clean_directory(config.GetRootBytes())

def run():
	#print('---------------- 清理旧文件 ----------------')
	clean()

	print("---------------- 生成Proto文件, 生成不同语言代码 ----------------")
	genearte_common_to_proto()
	genearte_excel_to_proto()
	print("---------------- 开始生成 python代码 ----------------")
	generate_target('python')	# 生成Python代码是必须的，因为要用来打包数据
	print("---------------- 开始生成 csharp 代码 ----------------")
	generate_target('csharp')
	# print("\n---------------- 开始生成 config csharp 代码 ----------------")
	# generate_target('configcs')