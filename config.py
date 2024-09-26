from logging import config
from pathlib import Path
import re
from shutil import copyfile
import sys
import subprocess
from IniParse import IniParse

PROTOTYPE = 1
PROTOSHOW = 3
TYPEROW = 2
NAMEROW = 7
DATAROW = 8


ini = {}

# exceldir = ""
# outputbytesdir = ""
# outputcsdir = ""
# outputconfigcsdir = ""
# excelDir = "../../Excel"
# outputBytesDir = "../../Client/Assets/Res/Config/"
# outputCSDir = "../../Client/Assets/Src/Config/ProtoBuffer"
# outputConfigCSDir = "../../Client/Assets/Src/Config"
# inputDir = "excel"
# outputBytesDir = "../UGUI_Project/Assets/Res/Config/ProtoBuffer"
# outputCSDir = "../UGUI_Project/Assets/Src/Config/ProtoBuffer"
def getOutBytesDir():
    return getAndCheckPath(ini['outputbytes'])
def getOutputCSDir():
    return getAndCheckPath(ini['outputcs'])
def getOutputConfigCSDir():
    return getAndCheckPath(ini['outputconfigcs'])

def getAndCheckPath(path):
	mkdir(path)
	return path

# --cpp_out=OUT_DIR           Generate C++ header and source.
#   --csharp_out=OUT_DIR        Generate C# source file.
#   --java_out=OUT_DIR          Generate Java source file.
#   --kotlin_out=OUT_DIR        Generate Kotlin file.
#   --objc_out=OUT_DIR          Generate Objective-C header and source.
#   --php_out=OUT_DIR           Generate PHP source file.
#   --pyi_out=OUT_DIR           Generate python pyi stub.
#   --python_out=OUT_DIR        Generate Python source file.
#   --ruby_out=OUT_DIR          Generate Ruby source file.
#   --rust_out=OUT_DIR          Generate Rust sources.

ProtoOutDir ={
	'cpp': '--cpp_out=',
	'csharp': '--csharp_out=',
	'java': '--java_out=',
	'kotlin': '--kotlin_out=',
	'objc': '--objc_out=',
	'php': '--php_out=',
	'pyi': '--pyi_out=',
	'python': '--python_out=',
	'ruby': '--ruby_out=',
	'rust': '--rust_out='
}

# 脚本文件后缀名
scriptExtDict = {
	'bytes' :'bytes',
	'xlsx' : 'xlsx',
	'proto' : 'proto',
    'configcs':'cs',
	'cpp': 'cc',
	'csharp': 'cs',
	'java': 'java',
	'kotlin': 'kt',
	'objc': 'h',
	'php': 'php',
	'pyi': 'pyi',
	'python': 'py',
	'ruby': 'rb',
	'rust': 'rs',
}

GEN_DIR_DICT ={
	'xlsx' : 'excel',
    'bytes' :'gen_bytes',
    'proto' :'gen_proto',
    'configcs':'gen_configcs',
    'cpp' : 'gen_cpp',
    'csharp': 'gen_csharp',
    'java': 'gen_java',
    'kotlin': 'gen_kotlin',
    'objc': 'gen_objc',
    'php': 'gen_php',
    'pyi': 'gen_pyi',
    # 'python': 'gen_python',
    'python': '',
    'ruby': 'gen_ruby',
    'rust': 'gen_rust'
}
def getGenDirByLanguage(language):
    lp = GEN_DIR_DICT[language]
    isnull = lp == None or lp == ''
    p=''
    if not isnull:
        p = getRootPath(lp)
    return getRootPath(lp)
# 本工具的根目录
work_root = Path.cwd()

def SvnUpdate(path):
    command = f"TortoiseProc.exe /command:update /path:{path}  /closeonend:0"
    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    print('Update over',output)

# protoc.exe所在目录
# protoc = os.path.join(work_root, 'protoc-25.2/bin/protoc.exe')
protoc = work_root.joinpath('protoc-25.2/bin/protoc3.exe')
def GetProtoc():
    return protoc

def getRootPath(folder):
    return GetFullPath(work_root, folder)
def getRootPathFile(folder, file):
	return getRootPath(f"{folder}\\{file}")
def getRootPathFileExtension(folder, file,ext):
	return getRootPath(f"{folder}\\{file}.{ext}")

# 存放excel的目录
def GetRootExcel():
    return getRootPath(GEN_DIR_DICT['xlsx']) 
def GetRootExcelFile(file):
	return getRootPathFile(GEN_DIR_DICT['xlsx'], file)

# 存放excel生成的flatbuffers二进制文件的目录
def GetRootBytes():
    return getGenDirByLanguage('bytes')

# 生成的 proto 文件的目录
def GetRootProto():
    return getGenDirByLanguage('proto')

#自动类型，只要值下面支持的都行
CUSTOM_TYPES = {
    # "num" : "int32",
    # "unum" : "uint32",
    # "str" : "string", 
    # "ilist" : "[int32]", 
    # "uilist" : "[uint32]", 
    # "flist" : "[float]", 
    # "slist" : "[string]",
    # "blist" : "[bool]",
}
def GetCustomTypeValue(value):
    return CUSTOM_TYPES.get(value, value)

def GetCustomTypeList(type):
    section = customini.get_section_options(type)
    customlist = []
    if len(section) > 0:
        index=1
        for op in section.values():
            # op = customini.get_option(v2)
            # repeated#uint64#list
            arr = str(op).split('#')
            # print(op)
            if len(arr) < 3 :
                continue
            customlist.append((index, arr[0], arr[1], arr[2]))
            index += 1
    return customlist

SUPPORT_DATATYPES = [
	'double',	# double
	'float',	# float
	'int32',	# int
	'int64',	# long
	'uint32',	# uint
	'uint64',	# ulong
	'sint32',	# int
	'sint64',	# long
	'fixed32',	# uint
	'fixed64',	# ulong
	'sfixed32',	# int
	'sfixed64',	# long
	'bool',		# bool
	'string',	# string
]

def CheckSupportType(tp):
    return CheckDefaultType(tp) or len(customini.get_section_options(tp))>0

def CheckDefaultType(tp):
     return tp in SUPPORT_DATATYPES #or tp in ENABLEARRYLIST

ENABLEARRYLIST = [
    '[double]',
    '[float]',
    '[int32]',
	'[int64]',
	'[uint32]',
	'[uint64]',
	'[sint32]',
	'[sint64]',
	'[fixed32]',
	'[fixed64]',
	'[sfixed32]',
	'[sfixed64]',
	'[bool]',
 	'[string]',
 ]

def GetEnableArrylistValue(tp):
	if tp in ENABLEARRYLIST:
		subType = re.sub(r"\[|\]","", tp)
		return True, subType
	return False, None

def CheckExcelFile(file):
	return str(file).endswith(scriptExtDict['xlsx'])

def GetFilesByExtension(path, extension):
    return [f for f in Path(path).iterdir() if str(f).endswith(f".{extension}")]
def GetFullFilesByExtension(path, extension):
    return [ f for f in Path(path).iterdir() if str(f).endswith(f".{extension}")]

def GetFullPath(path, file):
	return Path(path).joinpath(file)
def GetFullPathExtension(path, filename, extension):
    return GetFullPath(path, f"{filename}.{extension}")

def GetFileNameExt(file):
	p = Path(file)
	return p.stem, p.suffix

def clean_directory(target_path, isClear = False):
    # 确保目标路径是一个目录
    p = Path(target_path)
    p.mkdir(parents=True, exist_ok=True)
    # 检查路径是否存在并且是个目录
    if not isClear:
         return
    if p.exists() and p.is_dir():
        # 遍历目录下的所有子文件和子目录
        for child in p.glob('*'):
            if child.is_file():
                # 删除文件
                try:
                    child.unlink()
                except OSError as err:
                    print(f"An error occurred while deleting the file '{str(child)}': {err}")
            # elif child.is_dir():
            #     # 递归删除子目录
            #     clean_directory(child)
        
        # # 清空目录后删除该目录
        # p.rmdir()
####################################################################################################################
ARRAY_SPLITTER = '#'
LIST_SPLITCHAR1 = '&'
LIST_SPLITCHAR2 = '|'
LIST_SPLITCHAR3 = r'[\|&]'
LIST_SPLITAll = r'[#\|&]'
SPLITLIST = ['#', '-', '|', '&']
arry32 = ['int', 'int32', 'sint32', 'sfixed32']
arryu32 = ['uint','uint32', 'fixed32']
arry64 =  ['int64', 'double','sint64', 'sfixed64']
arryu64 = ['uint64', 'fixed64']

def get_split_char(value):
    for c in SPLITLIST:
        if c in str(value):
            return c
    return None



####################################################################################################################

def writeFile(path, context):
	# 写入文件
	# print(path)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(str(path), 'w', encoding='utf-8') as f:
        f.write(context)

def initIni():

    # confini = iniParse.ConfigParser()
    # confini.read('config.ini')
    # # if confini.has_section('Path'):
    # #     exceldir = confini.get('Path', 'exceldir')
    # #     outputBytesDir = confini.get('Path', 'outputBytesDir')
    # #     outputCSDir = confini.get('Path', 'outputCSDir')
    # #     outputConfigCSDir = confini.get('Path', 'outputConfigCSDir')
	# # # 遍历所有section和选项
    # for section in confini.sections():
    #     for option, value in confini.items(section):
    #         # print(f"Section: {section}, Option: {option}, Value: {value}")
    #         ini[option] = value
    confini = IniParse('config.ini')
    global ini
    ini = confini.Allini
    global TYPEROW
    TYPEROW = int(ini['typerow'])
    global NAMEROW
    NAMEROW = int(ini['namerow'])
    global DATAROW
    DATAROW = int(ini['datarow'])
    global PROTOTYPE
    PROTOTYPE = int(ini['prototype'])
    global PROTOSHOW
    PROTOSHOW = int(ini['protoshow'])
    global customini
    customini = IniParse('customType.ini')
    global CUSTOM_TYPES
    CUSTOM_TYPES = customini.get_section_options('customType')
    # for section in customini.sections():
    #     for option, value in customini.items(section):
    #         CUSTOM_TYPES[option] = value
    cleanExcel()
    # sys.path.append(f"{Path.cwd()}")
    
def cleanExcel():
    clean_directory(getRootPath(GEN_DIR_DICT['xlsx']), True)

def mkdir(path):
    p = Path(path)
    if not p.exists():
        p.mkdir(parents=True)

excelKeyDict = {}

def Quit():
	sys.exit(0)

def GetIniFiles(ext):
    return GetFullFilesByExtension(ini['exceldir'], ext)
def CopyToFolder(file):
    name, ext = GetFileNameExt(file)
    ext = ext.split(".")[1]
    outputf = GetFullPathExtension(GEN_DIR_DICT['xlsx'], name, ext)
    outdir = outputf.parent.mkdir(parents=True, exist_ok=True)
    copyfile(file, outputf)
    
def Init(names):
	initIni()
	excelKeyDict = {}
	try:
		mkdir(GEN_DIR_DICT['xlsx'])
	except FileExistsError:
		pass
	ext = scriptExtDict['xlsx']
	excels = GetFilesByExtension(ini['exceldir'], ext)
	for file in excels:
		name, ext = GetFileNameExt(file)
		ext = ext.split(".")[1]
		if (len(names)>0 and not name in names) or name.startswith('~'):
			continue
		inputf = file
		outputf = GetFullPathExtension(GEN_DIR_DICT['xlsx'], name, ext)
		# print(name, ext, input, outputf)
		copyfile(inputf, outputf)