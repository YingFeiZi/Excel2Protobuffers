import re
import sys

cscode = """
using Config;
using UnityEngine;

public class {TABLENAME}Config : ConfigBase<{TABLENAME}Array, {TABLENAME}Data?, {keytype}, {TABLENAME}Config>
{{
    protected override string GetConfigPath()
    {{
        return "Config/{TABLENAME}.bytes";
    }}

    protected override {TABLENAME}Array GetTable(byte[] byteBuffer)
    {{
        return {TABLENAME}Array.Parser.ParseFrom(byteBuffer);
    }}

    public override int GetTableCount()
    {{
        return table.Datas.Count;
    }}

    public override {TABLENAME}Data GetTable(int index)
    {{
        return table.Datas[index];
    }}

    protected override {keytype} GetTabelKey({TABLENAME}Data tableRowData)
    {{
        return tableRowData.{keyname};
    }}
}}
"""

def getCsCode(table, keyValue):
    type = re.match(r"\D*",keyValue['field_type']).group()
    return cscode.format(TABLENAME = table, keytype = type, keyname = keyValue['field_name'])