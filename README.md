# Excel2Protobuffers
tools Excel to Protobuffers

可以讲Excel 转换为 Protobuffers 可以各种代码语言使用


注意：配置环境是 python3.11.7   第三方python包：openpyxl，openpyxl，numpy，protobuf


## 使用方法：
    1.excel配表：
    ![exceltpl](image.png)
    如图所示，默认是第二行字段类型，第三行是字段名 
    如需修改，修改config.py的 
        TYPE_ROW = 2   # 第二行是字段类型
        NAME_ROW = 3   # 第三行是字段名
        DATA_ROW = 4   # 第四行是开始读数据位置数据
        
    2.执行run.bat 自动生成出对应语言代码及序列化的excel数据

## 支持类型：
    1.默认类型 
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

    2.默认数组类型
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
 	'[string]',]
    
    3.自定义类型, 在config.py 的 CUSTOM_TYPES 中可以自定义

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
