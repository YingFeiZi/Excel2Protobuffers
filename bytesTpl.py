
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
from {pymodule} import table_common_pb2 as common
"""

pythonCode = """
import sys
from {pymodule} import {tablepb} as {table}
{iptcommon}
dataArray = [] #{table}.{table}ARRAY()

{allRowCodes}

def Write():
    with open('{ByteFilePath}', 'wb') as f:
        f.write(dataArray.SerializeToString())
"""

addRowCode = """
data{index} = {table}.{table}
{rowcodes}
dataArray.append(data{index})
"""

rowCode = "data{index}.{type} = {variable} \n"

rowCodeRepeated = "data{index}.{type}.append({variable})\n"

def getRowCode(index, type, variable, isString = False, isRepeated = False):
    variable = isString and f"\"{variable}\"" or variable
    if isRepeated:
        return rowCodeRepeated.format(index=index, type=type, variable=variable)
    else:
        return rowCode.format(index=index, type=type, variable=variable)

def getAddRowCode(idx, table,rowcodes):
    return addRowCode.format(index=idx, table = table,rowcodes=rowcodes)

def getPythonCode(module, tablepy, table, allRowCodes, ByteFilePath, iscommon=False):
    iptcom = iscommon and iptcommon or ''
    return pythonCode.format(pymodule = module, tablepb=tablepy, table = table, allRowCodes=allRowCodes, ByteFilePath=ByteFilePath,iptcommon=iptcom)