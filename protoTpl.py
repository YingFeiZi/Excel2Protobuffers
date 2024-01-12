import os

row_code = """
message %s {
    %s
}
"""

group_code = """
syntax = "proto3";

package Config;

message %sArray {
	repeated %s objs = 1;
}
"""

row_code_normal = "    %s %s = %d;\n"
row_code_repeated = "    repeated %s %s = %d;\n"


def getRowLineCore(data_type, variable, index, isArry):
    if isArry:
        return  row_code_repeated % (data_type, variable, index)
    else:
        return  row_code_normal % (data_type, variable, index)
def getGroupcode(group_table_name, row_table_name):
    return group_code % (group_table_name, row_table_name)

def getRowCode(row_table_name, variables_str):
    return row_code % (row_table_name, variables_str)
def getProtoCode(groupcode, rowcode):
    return f"{groupcode}\n{rowcode}"