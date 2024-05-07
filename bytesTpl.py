import sys

# pythonCode = """
# import sys
# from {pymodule} import {tablepb} as {table}

# dataArray = {table}.{table}ARRAY()

# {allRowCodes}

# with open('{ByteFilePath}', 'wb') as f:
# 	f.write(dataArray.SerializeToString())
# """
iptcommon = """
# from {pymodule} import table_common_pb2 as common
import table_common_pb2 as common
"""

addcommon = """{data} = common.{type}()\n"""

pythonCode = """
import sys
import Encrypted
from io import BytesIO
from google.protobuf.internal.encoder import _EncodeVarint
from google.protobuf.message import Message
# from {pymodule} import {tablepb} as {table}
import {tablepb} as {table}
{iptcommon}
dataArray = [] #{table}.{table}ARRAY()

{allRowCodes}

# print("dataArray :", dataArray)
with open('{ByteFilePath}', 'wb') as f:
    b = BytesIO()
    element_count = int(len(dataArray))
    _EncodeVarint(b.write, element_count)
    for message in dataArray:
        if isinstance(message, Message):  # 确保是protobuf消息对象
            # 计算消息序列化后的字节大小
            size = message.ByteSize()
            _EncodeVarint(b.write, size)
            b.write(message.SerializeToString())
    bytes_to_write = b.getvalue()
    dataencrypt = Encrypted.xor_cipher_default(bytes_to_write)
    f.write(dataencrypt)
    b.close()
"""

addRowCode = """
data{index} = {table}.{table}()
{rowcodes}
dataArray.append(data{index})
"""

rowCode = "data{index}.{type} = {variable} \n"

rowCodeRepeated = "data{index}.{type}.append({variable})\n"

cusrowCode = "{name}{index}.{type} = {variable} \n"
cusrowCodeRepeated = "{name}{index}.{type}.append({variable})\n"

repeateCode = "{name}{index}.{type} = {variable} \n"

def getCommonCode(data, type):
    return addcommon.format(data=data, type=type)

def getRepeateCode(index, name, type, variable):
    return repeateCode.format(index=index, name=name, type=type, variable=variable)

def getCustomRowCode(index, name, type, isstring, variable, isRepeated = False):
    variable = isstring and f"\"{variable}\"" or variable
    if isRepeated:
        return cusrowCodeRepeated.format(index=index, name=name, type=type, variable=variable)
    else:
        return cusrowCode.format(index=index, name=name, type=type, variable=variable)


def getRowCode(index, type, isstring, variable, isRepeated = False):
    variable = isstring and f"\"{variable}\"" or variable
    if isRepeated:
        return rowCodeRepeated.format(index=index, type=type, variable=variable)
    else:
        return rowCode.format(index=index, type=type, variable=variable)

def getAddRowCode(idx, table,rowcodes):
    return addRowCode.format(index=idx, table = table,rowcodes=rowcodes)

def getPythonCode(module, tablepy, table, allRowCodes, ByteFilePath, iscommon=False):
    iptcom = iscommon and iptcommon.format(pymodule = module) or ''
    return pythonCode.format(pymodule = module, tablepb=tablepy, table = table, allRowCodes=allRowCodes, ByteFilePath=ByteFilePath,iptcommon=iptcom)