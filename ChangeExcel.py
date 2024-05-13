import config
import openpyxl
import sys
from pathlib import Path

rp = ['uint32list', 'uint32', 'sint32']
cusrp = ['uint32#&list', 'uint32#|list', 'uint32#|&list']
def ReplaceType(value):
    # if value == 'uint32list' or value == 'uint32' or value == 'sint32':
    if value in rp:
        return 'int32'
    if value == 'uint32#&list':
        return 'int32#&list'
    if value == 'uint32#|list':
        return 'int32#|list'
    if value == 'uint32#|&list':
        return 'int32#|&list'
    return value
def do_excel(path):
    wb = openpyxl.load_workbook(path, False, False,True)
    sheet = wb.active
    readRow = 2
    ischang = False
    for cell in sheet[readRow]:
        if cell.value in cusrp or cell.value in rp:
            cell.value = ReplaceType(cell.value)
            ischang = True

    # wb.close()
    if ischang:
        wb.save(path)
        print('change over:', path)

config.initIni()
ext = config.scriptExtDict['xlsx']
excels = config.GetFilesByExtension(config.ini['exceldir'], ext)
for excel in excels:
    do_excel(excel)