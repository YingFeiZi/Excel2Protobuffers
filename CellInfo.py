import re
import numpy as np
import config
import protoTpl
import bytesTpl

class CellInfo:
    # ARRAY_SPLITTER = '#'
    # LIST_SPLITCHAR1 = '&'
    # LIST_SPLITCHAR2 = '\||'
    # LIST_SPLITCHAR3 = '\||&'
    # arry32 = ['int', 'int32', 'sint32', 'sfixed32']
    # arryu32 = ['uint','uint32', 'fixed32']
    # arry64 =  ['int64', 'double','sint64', 'sfixed64']
    # arryu64 = ['uint64', 'fixed64']
    def __init__(self, type, typename, name, value = None, repeated=None, isshow = 1, index = 0):
        self.type = type
        self.typename = typename
        self.name = name
        self.originaldata = ''
        self.value = value
        self.row = 0
        self.col = 0
        self.index =index
        self.prototype = repeated
        self.protoshow = isshow
        self.arrayvalue = []
    def isRepeated(self):
        return self.prototype == "repeated"
    def isShow(self):
        return  not self.protoshow == None and int(self.protoshow) == 1
    def toProto(self):
        typestr = self.isRepeated() and  f"{self.prototype}  {self.type}" or self.type
        # showstr = self.isShow() and '' or  '//'
        showstr = ''
        if not self.isShow():
            showstr = '//'
        return protoTpl.getRowLineCore(f"{showstr}{typestr}", self.name, self.index)

    def toByte(self, index):
        str=''
        # if self.isRepeated():
        #     str+= bytesTpl.getRepeateCode(index, 'data',self.name, '[]')
        if len(self.arrayvalue) > 0:
            for tv in self.arrayvalue:
                if tv == None:
                    continue
                str += self.getbytestring(index, tv)
                if not self.isRepeated():
                    break
        return str
    
    def getbytestring(self, index, value):
        custs = config.GetCustomTypeList(self.type)
        if len(custs) > 0:
            return self.getCustomType(index, self.name, self.type, value)
        else:
            return self.getstring(index, self.name, self.type, value)
        
    def getstring(self, index, name,type, value):
        isstring = type == 'string'
        return bytesTpl.getRowCode(index, name, isstring, value, self.isRepeated())

    def getCustomType(self, index, name, type, value):
        if len(value.arrayvalue) <1:
            return ''
        data = f"{value.name}{value.index}"
        substr = bytesTpl.getCommonCode(data, type)
        # substr += bytesTpl.getRepeateCode(value.index, value.name, value.name, '[]')
        for vv in value.arrayvalue:
            if vv == None or vv== '':
                continue
            isstring = type == 'string'
            substr += bytesTpl.getCustomRowCode(value.index, value.name, value.name, isstring, vv, value.isRepeated())
        substr += self.getstring(index, name, type, data)
        return substr
    



    # def Parse(self):
    #     if  config.CheckDefaultType(self.type):
    #         if self.isRepeated():
    #             if not self.originaldata == None:
    #                 if '|' in self.originaldata or '&' in self.originaldata:
    #                     arrayv = re.split(CellInfo.LIST_SPLITCHAR3, self.originaldata) #rowcell.value.split(ExcelParse.ARRAY_SPLITTER)
    #                     for v in arrayv:
    #                         self.arrayvalue.append(self.get_repeate_value(self.type, v))
    #                 else:
    #                     arrayv = re.split(CellInfo.ARRAY_SPLITTER, self.originaldata) #rowcell.value.split(ExcelParse.ARRAY_SPLITTER)
    #                     for v in arrayv:
    #                         self.arrayvalue.append(self.get_repeate_value(self.type, v))
    #         else:
    #             cellvalue = self.get_real_value(self.type, self.originaldata)
    #             self.value = cellvalue
    #     else:
    #         self.arrayvalue = self.PareCustomType(self.type, self.originaldata)
    # def trimDotZeroes(self,text):
    #     if isinstance(text, str):
    #         text = text.strip()
    #         if text == "": return 0
    #         return re.sub("\.0+$", "", text)
    #     return text
    # def get_repeate_value(self,data_type, row_value):
    #     arr = re.split(CellInfo.ARRAY_SPLITTER, row_value)
    #     if len(arr) > 1:
    #         if data_type in CellInfo.arryu64:
    #             v1 = int(np.int64(self.trimDotZeroes(arr[0])))
    #             v2 = int(np.int32(self.trimDotZeroes(arr[1])))
    #             return (v1<<32) | v2

    #     else:
    #         return self.get_real_value(data_type, row_value)
    # def get_real_value(self,data_type, row_value):
    #     if not row_value :
    #         return None
    #         # print('data_type: ', data_type, 'row_value:', row_value)
    #     trizv = self.trimDotZeroes(row_value)
    #     try:
    #         npv = None
    #         if data_type == 'string':
    #             value = str(row_value)
    #             value = value.replace('\\', '\\\\')
    #             npv = '''{}'''.format(value)
    #         elif data_type in CellInfo.arry32:
    #             npv = np.int32(trizv) 
    #         elif data_type in CellInfo.arryu32:
    #             npv = np.uint32(trizv) 
    #         elif data_type in CellInfo.arry64:
    #             npv = np.int64(trizv) 
    #         elif data_type in CellInfo.arryu64:
    #             npv = np.uint64(trizv)
    #         elif data_type == 'float':
    #             npv = float(row_value)
    #         elif data_type == 'bool':
    #             npv = bool(row_value)
    #         else:
    #             return None
    #         return npv
    #     except ValueError as e:
    #         print(f"无法将 {trizv} 转换为 uint32 类型，ValueError: {e}")
    #         return None
    # def PareCustomType(self,celltype, cellvalue):
    #     attrs = []
    #     custs = config.GetCustomTypeList(celltype)
    #     # if len(custs) ==1:
    #     for cust in custs:
    #         # crepeate = custs[0][1]
    #         # ctype = custs[0][2]
    #         # cname = custs[0][3]
    #         curcell = CellInfo(cust[2], cust[2],cust[3], None,cust[1])
    #         attrs.append(curcell)
    #     if not self.originaldata == None and ('|' in self.originaldata or '&' in self.originaldata):
    #         arrayv = re.split(CellInfo.LIST_SPLITCHAR3, self.originaldata)
    #         for v in arrayv:
    #             arr = re.split(CellInfo.ARRAY_SPLITTER, v)
                
        
    #     return attrs
