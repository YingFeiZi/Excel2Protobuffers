import os
import re
from shutil import copyfile

TYPE_ROW = 2
NAME_ROW = 3
DATA_ROW = 4

excelDir = "../../Excel"
inputDir = "excel"
# outputBytesDir = "../../Client/Assets/Res/Config/ProtoBuffer"
# outputCSDir = "../../Client/Assets/Src/Config/ProtoBuffer"
outputBytesDir = "../UGUI_Project/Assets/Res/Config/ProtoBuffer"
outputCSDir = "../UGUI_Project/Assets/Src/Config/ProtoBuffer"


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
    'cpp' : 'gen_cpp',
    'csharp': 'gen_csharp',
    'java': 'gen_java',
    'kotlin': 'gen_kotlin',
    'objc': 'gen_objc',
    'php': 'gen_php',
    'pyi': 'gen_pyi',
    'python': 'gen_python',
    'ruby': 'gen_ruby',
    'rust': 'gen_rust'
}
def getGenDirByLanguage(language):
    return getRootPath(GEN_DIR_DICT[language])
# 本工具的根目录
work_root = os.getcwd()

# protoc.exe所在目录
protoc = os.path.join(work_root, 'protoc-25.2/bin/protoc.exe')
def GetProtoc():
    return protoc

def getRootPath(folder):
    return GetFullPath(work_root, folder)
def getRootPathFile(folder, file):
	return getRootPath(f"{folder}/{file}")


# 存放excel的目录
def GetRootExcel():
    return getRootPath(inputDir) 
def GetRootExcelFile(file):
	return getRootPathFile(inputDir, file)

# 存放excel生成的flatbuffers二进制文件的目录
def GetRootBytes():
    return getGenDirByLanguage('bytes')

# 生成的 proto 文件的目录
def GetRootProto():
    return getGenDirByLanguage('proto')

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

def CheckExcelFile(file):
	return file.endswith(scriptExtDict['xlsx'])

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
	ext = scriptExtDict['xlsx']
	excels = GetFilesByExtension(excelDir, ext)
	for file in excels:
		name, ext = GetFileNameExt(file)
		if len(names)>0 and not name in names:
			continue
		input = GetFullPath(excelDir, file)
		output = GetFullPathExtension(inputDir, name, ext)
		copyfile(input, output)