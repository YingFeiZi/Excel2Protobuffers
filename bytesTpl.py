
import sys

# pythonCode = """
# import sys
# from {pymodule} import {tablepb} as {table}

# dataArray = {table}.{table}ARRAY()

# {allRowCodes}

# with open('{ByteFilePath}', 'wb') as f:
# 	f.write(dataArray.SerializeToString())
# """
pythonCode = """
import sys
from {pymodule} import {tablepb} as {table}

dataArray = {table}.{table}ARRAY()

{allRowCodes}

def Write():
    with open('{ByteFilePath}', 'wb') as f:
        f.write(dataArray.SerializeToString())
"""

addRowCode = """
data{index} = dataArray.rows.add()
{rowcodes}
"""

rowCode = "data{index}.{type} = {variable} \n"

rowCodeRepeated = "data{index}.{type}.append({variable})\n"

def getRowCode(index, type, variable, isString = False, isRepeated = False):
    variable = isString and f"\"{variable}\"" or variable
    if isRepeated:
        return rowCodeRepeated.format(index=index, type=type, variable=variable)
    else:
        return rowCode.format(index=index, type=type, variable=variable)

def getAddRowCode(idx, rowcodes):
    return addRowCode.format(index=idx, rowcodes=rowcodes)

def getPythonCode(module, tablepy, table, allRowCodes, ByteFilePath):
    return pythonCode.format(pymodule = module, tablepb=tablepy, table = table, allRowCodes=allRowCodes, ByteFilePath=ByteFilePath)