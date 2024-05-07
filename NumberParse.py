import copy
import re
import sys
import numpy as np
import config
from CellInfo import CellInfo

def trimDotZeroes(text):
    if isinstance(text, str):
        text = text.strip()
        if text == "": return 0
        return re.sub("\.0+$", "", text)
    return text
def get_real_value(data_type, row_value):
    if not row_value :
        return None
        # print('data_type: ', data_type, 'row_value:', row_value)
    trizv = trimDotZeroes(row_value)
    try:
        npv = None
        if data_type == 'string':
            value = str(row_value)
            value = value.replace('\\', '\\\\')
            npv = '''{}'''.format(value)
        elif data_type in config.arry32:
            npv = np.int32(trizv) 
        elif data_type in config.arryu32:
            npv = np.uint32(trizv) 
        elif data_type in config.arry64:
            npv = np.int64(trizv) 
        elif data_type in config.arryu64:
            npv = np.uint64(trizv)
        elif data_type == 'float':
            npv = float(row_value)
        elif data_type == 'bool':
            npv = bool(row_value)
        else:
            return None
        return npv
    except ValueError as e:
        print(f"无法将 {trizv} 转换为 uint32 类型，ValueError: {e}")
        return None
def ParseStringToComboList(value, split1, split2):
    vs = []
    arrayv = re.split(split1, value)
    for v in arrayv:
        vs.append(ParsePart(v, split2))
    return vs
def ParsePart(value, split):
    arr = re.split(split, value)
    if len(arr) > 1:
        v1 = int(np.int64(trimDotZeroes(arr[0])))
        v2 = int(np.int32(trimDotZeroes(arr[1])))
        return (v1<<32) | v2

def ParseStringToIntList(value):
    vs = []
    c = config.get_split_char(value)
    if c == '' or c == None:
        return vs
    arrayv = re.split(c, str(value))
    for v in arrayv:
        vv = get_real_value('int', v)
        vs.append(vv)
    return vs

def ParseUint64List(value):
    vs = []
    arrayv = re.split(config.LIST_SPLITCHAR1, value)
    for v in arrayv:
        arrayvalue = ParseStringToComboList(v, config.LIST_SPLITCHAR2, config.ARRAY_SPLITTER)
        vs.append(arrayvalue)
    return vs

def Parse(type, cvalue):
    vs = []
    if cvalue == None or cvalue == '':
        return vs
    value = str(cvalue)
    if  config.CheckDefaultType(type):
        vv = get_real_value(type, value)
        vs.append(vv)
    elif type=="uint32list":
        arrayv = re.split(config.ARRAY_SPLITTER, str(value))
        for v in arrayv:
            vv = get_real_value(type, v)
            vs.append(vv)
    elif type=="uint32#&list":
        vs = ParseStringToComboList(value, config.LIST_SPLITCHAR1, config.ARRAY_SPLITTER)
    elif type=="uint32#|list":
        vs = ParseStringToComboList(value, config.LIST_SPLITCHAR2, config.ARRAY_SPLITTER)
    elif type=="uint32#|&list":
        arrayv = re.split(config.LIST_SPLITCHAR1, value)
        type_data = config.GetCustomTypeValue(type)
        custs = config.GetCustomTypeList(type_data)
        if len(custs) ==1:
            crepeate = custs[0][1]
            ctype = custs[0][2]
            cname = custs[0][3]
            index = 1
            for v in arrayv:
                curcell = CellInfo(ctype, ctype, cname, None,crepeate, True, index)
                curcell.arrayvalue = ParseStringToComboList(v, config.LIST_SPLITCHAR2, config.ARRAY_SPLITTER)
                vs.append(curcell)
                index += 1
    return vs
