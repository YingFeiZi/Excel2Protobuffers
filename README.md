# Excel2Protobuffers
tools Excel to Protobuffers

可以讲Excel 转换为 Protobuffers 可以各种代码语言使用

![](image.png)


注意：配置环境是 python3.11.7   第三方python包：openpyxl，openpyxl，numpy，protobuf


## 使用方法：
    1.配置config.ini文件
    excelDir                # excel目录
    outputBytesDir          # 生成的序列化数据目录
    outputCSDir             # 生成的CS目录
    outputConfigCSDir       # 生成的configCS目录

    2.配置customType.ini文件
    type : value            #type 自定义类型，配置在excel表头上的
                            #value 为对应proto支持的值类型 repeated类型的用[]包起来

    3.excel配表：
    如图所示，默认是第二行字段类型，第三行是字段名 
    如需修改，修改config.py的 
        TYPEROW = 2   # 第二行是字段类型
        NAMEROW = 3   # 第三行是字段名
        DATAROW = 4   # 第四行是开始读数据位置数据
        
    4.执行run.bat 自动生成出对应语言代码及序列化的excel数据, 传参，文件名，支持多个， 无参就是整个excel目录 

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

#python 3.11.7 
#package

aiohttp==3.9.3
aiosignal==1.3.1
altgraph==0.17.4
annotated-types==0.6.0
ansicon==1.89.0
anyio==4.2.0
appdirs==1.4.4
astor==0.8.1
asttokens==2.4.1
attrs==23.2.0
backoff==2.2.1
blessed==1.20.0
certifi==2024.2.2
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
comm==0.2.1
configparser==6.0.0
contourpy==1.2.0
cycler==0.12.1
debugpy==1.8.0
decorator==5.1.1
distro==1.9.0
editor==1.6.6
et-xmlfile==1.1.0
executing==2.0.1
filelock==3.13.1
fire==0.6.0
fonttools==4.47.2
frozenlist==1.4.1
fsspec==2023.12.2
git-python==1.0.3
gitdb==4.0.11
GitPython==3.1.41
h11==0.14.0
html2image==2.0.4.3
httpcore==1.0.2
httpx==0.26.0
huggingface-hub==0.20.3
idna==3.6
importlib-metadata==7.0.1
inquirer==3.2.3
install==1.3.5
ipykernel==6.29.0
ipython==8.21.0
jedi==0.19.1
Jinja2==3.1.3
jinxed==1.2.1
jupyter_client==8.6.0
jupyter_core==5.7.1
kiwisolver==1.4.5
litellm==1.20.9
lxml==5.1.0
markdown-it-py==3.0.0
MarkupSafe==2.1.4
matplotlib==3.8.2
matplotlib-inline==0.1.6
mdurl==0.1.2
monotonic==1.6
multidict==6.0.4
nest-asyncio==1.6.0
numpy==1.26.3
open-interpreter==0.2.0
openai==1.10.0
opencv-python-headless==4.9.0.80
openpyxl==3.1.2
packaging==23.2
parso==0.8.3
pdf2docx==0.5.8
pefile==2023.2.7
pillow==10.2.0
platformdirs==4.2.0
posthog==3.3.4
prompt-toolkit==3.0.43
protobuf==3.20.0
psutil==5.9.8
pure-eval==0.2.2
pydantic==2.6.0
pydantic_core==2.16.1
Pygments==2.17.2
pyinstaller==6.3.0
pyinstaller-hooks-contrib==2023.12
PyMuPDF==1.23.26
PyMuPDFb==1.23.22
pyparsing==3.1.1
PyQt6==6.4.2
pyqt6-plugins==6.4.2.2.3
PyQt6-Qt6==6.4.3
PyQt6-sip==13.6.0
pyqt6-tools==6.4.2.3.3
pyreadline3==3.4.1
python-dateutil==2.8.2
python-docx==1.1.0
python-dotenv==1.0.1
pywin32==306
pywin32-ctypes==0.2.2
PyYAML==6.0.1
pyzmq==25.1.2
qt6-applications==6.4.3.2.3
qt6-tools==6.4.3.1.3
readchar==4.0.5
regex==2023.12.25
requests==2.31.0
rich==13.7.0
runs==1.2.2
six==1.16.0
smmap==5.0.1
sniffio==1.3.0
stack-data==0.6.3
termcolor==2.4.0
tiktoken==0.4.0
tokenizers==0.15.1
tokentrim==0.1.13
toml==0.10.2
tornado==6.4
tqdm==4.66.1
traitlets==5.14.1
typing_extensions==4.9.0
urllib3==2.2.0
wcwidth==0.2.13
websocket-client==1.7.0
wget==3.2
xmod==1.8.1
yarl==1.9.4
zipp==3.17.0