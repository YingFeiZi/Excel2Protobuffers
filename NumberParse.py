import copy
import re
import sys
from cycler import V
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
        print(f"<br><font color='red'>无法将 {trizv} 转换为 uint32 类型，ValueError: {e}</font>")
        return None
def ParseStringToComboList(value, split1, split2):
    vs = []
    arrayv = value.split(split1)
    for v in arrayv:
        vs.append(ParsePart(v, split2))
    return vs

def ParseStringToList(value, split1):
    vs = []
    arrayv = value.split(split1)
    for v in arrayv:
        vs.append(int(np.int32(trimDotZeroes(v))))
    return vs

def ParseStringToCombo(value):
    arrayv = get_split_value(value)
    if len(arrayv) > 1:
        return MergeToLong(arrayv[0],arrayv[1]) 
    return 0

def CheckSplitChar(value):
    return any((char in value) for char in config.SPLITLIST)

def get_split_value(value):
    pattern = '|'.join(map(re.escape, config.SPLITLIST))
    return re.split(pattern, value)

def ParsePart(value, split):
    arrayv = re.split(split, value)
    if len(arrayv) > 1:
        return MergeToLong(arrayv[0],arrayv[1])
        
def MergeToLong(int1, int2):
    v1 = int(np.int64(trimDotZeroes(int1)))
    v2 = int(np.int32(trimDotZeroes(int2)))
    return (v1<<32) | v2


def ParseStringList(value):
    vs = []
    c = config.get_split_char(value)
    if c == '' or c == None:
        vs.append(value)
        return vs
    vs = re.split(c, value)
    return vs

def ParseStringToIntList(value):
    vs = []
    c = config.get_split_char(value)
    if c == '' or c == None:
        vs.append(value)
        return vs
    arrayv = re.split(c, str(value))
    for v in arrayv:
        vv = get_real_value('int', v)
        vs.append(vv)
    return vs

def ParseInt64List(value):
    vs = []
    arrayv = re.split(config.LIST_SPLITCHAR1, value)
    for v in arrayv:
        arrayvalue = ParseStringToComboList(v, config.LIST_SPLITCHAR2, config.ARRAY_SPLITTER)
        vs.append(arrayvalue)
    return vs

def ParseInt32List(value):
    vs = []
    if config.LIST_SPLITCHAR1 in value:
        arrayv = re.split(config.LIST_SPLITCHAR1, value)
    else:
        arrayv = re.split(config.LIST_SPLITCHAR2, value)
    for v in arrayv:
        arrayvalue = ParseStringToList(v, config.ARRAY_SPLITTER)
        vs.append(arrayvalue)
    return vs

def ParseInt32ListList(value):
    vs = []
    arrayv = re.split(config.LIST_SPLITCHAR1, value)
    for v in arrayv:
        arrayvalue = ParseInt32List(v)
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
