import os
import re
from shutil import copyfile


excelDir = "../../Excel"
inputDir = "excel"
outputBytesDir = "../../Client/Assets/Res/Config/FlatBuffer"
outputCSDir = "../../Client/Assets/Src/Config/FlatBuffer"


# 本工具的根目录
work_root = os.getcwd()

# flatc.exe所在目录
protoc = os.path.join(work_root, 'protoc-25.2/bin/protoc.exe')
def GetProtoc():
    return protoc

# 存放excel的目录
excel_root = os.path.join(work_root, inputDir)
def GetRootExcel():
    return excel_root
def GetRootExcelFile(file):
	return os.path.join(excel_root, file)

# 存放excel生成的flatbuffers二进制文件的目录
bytes_root = os.path.join(work_root, 'gen_bytes')

def GetRootBytes():
    return bytes_root

# 生成的 fbs 文件的目录
Proto_root = os.path.join(work_root, 'gen_Proto')
def GetRootProto():
    return Proto_root

# fbs 生成的 python 代码目录
python_root = os.path.join(work_root, 'gen_python')
def GetRootPython():
    return python_root

# fbs 生成的 c# 代码目录
csharp_root = os.path.join(work_root, 'gen_csharp')
def GetRootCSharp():
    return csharp_root

# fbs 生成的 go 代码目录
go_root = os.path.join(work_root, 'gen_go')
def GetRootGo():
    return go_root

# fbs 生成的 rust 代码目录
rust_root = os.path.join(work_root, 'gen_rust')
def GetRootRust():
    return rust_root

# fbs 生成的 lua 代码目录
lua_root = os.path.join(work_root, 'gen_lua')
def GetRootLua():
    return lua_root
#自动类型，只要值下面支持的都行
CUSTOM_TYPES = {
    "num" : "int32",
    "unum" : "uint32",
    "str" : "string", 
    "ilist" : "[int32]", 
    "uilist" : "[uint32]", 
    "flist" : "[float]", 
    "slist" : "[string]",
    "blist" : "[bool]",
}
def GetCustomTypeValue(value):
    return CUSTOM_TYPES.get(value, value)

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

def CheckSupportType(type):
    return type in SUPPORT_DATATYPES or type in ENABLEARRYLIST

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

def GetEnableArrylistValue(type):
	if type in ENABLEARRYLIST:
		subType = re.sub(r"\[|\]","", type)
		return True, subType
	return False, None


excel_ext = 'xlsx'
proto_ext = 'proto'
def CheckExcelFile(file):
	return file.endswith(excel_ext)



def GetFilesByExtension(path, extension):
    return [f for f in os.listdir(path) if f.endswith(f".{extension}")]

def GetFullPath(path, file):
	return os.path.join(path, file)
def GetFullPathExtension(path, filename, extension):
    return GetFullPath(path, f"{filename}.{extension}")

def GetFileNameExt(file):
	filename = os.path.basename(file)
	name, ext = os.path.splitext(filename)
	return re.split(r"\.|-", name)[0], ext

def clean_directory(target_path):
    # 确保目标路径是一个目录
    if not os.path.isdir(target_path):
        os.mkdir(target_path)
    
    try:
        # 遍历目录树删除所有文件
        for root, dirs, files in os.walk(target_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                #print(f'清理文件: {file_path}')
    except OSError:
        # 提供更详细的错误信息
        print('旧数据清理失败，可能有文件正在使用。请关掉已打开的文件并重试。')


def mkdir(path):
	if not os.path.exists(path):
		os.makedirs(path)

def Init(names):
	try:
		mkdir(inputDir)
	except FileExistsError:
		pass
	clean_directory(inputDir)
	excels = GetFilesByExtension(excelDir, excel_ext)
	for file in excels:
		name, ext = GetFileNameExt(file)
		if len(names)>0 and not name in names:
			continue
		input = GetFullPath(excelDir, file)
		output = GetFullPathExtension(inputDir, name, excel_ext)
		copyfile(input, output)