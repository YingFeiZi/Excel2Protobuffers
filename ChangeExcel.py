import config
import openpyxl
import sys
from pathlib import Path

rp = ['uint32list', 'uint32', 'sint32']
def ReplaceType(value):
    # if value == 'uint32list' or value == 'uint32' or value == 'sint32':
    if value in rp:
        return 'int32'
    return value
def do_excel(path):
    wb = openpyxl.load_workbook(path, False, False,True)
    sheet = wb.active
    readRow = 2
    for cell in sheet[readRow]:
        cell.value = ReplaceType(cell.value)

    # wb.close()
    wb.save(path)
    print('change over:', path)

config.initIni()
ext = config.scriptExtDict['xlsx']
excels = config.GetFilesByExtension(config.ini['exceldir'], ext)
for excel in excels:
    do_excel(excel)