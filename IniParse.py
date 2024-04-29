# Python 代码文件 IniParse.py 包含一个名为 IniParse 的类，用于解析 INI 配置文件。
# 该类包括初始化方法 __init__，用于读取指定文件的配置信息到 self.ini 字典中；
# get_section_options 方法，用于获取特定 section 下的所有项；
# GetIni 方法，用于返回指定配置项的值；
# GetType 方法，用于返回指定类型的配置项列表。

import sys
import configparser

"""
# 创建IniParse对象
confini = IniParse('customType.ini')
# 获取特定section下的所有项
section_name = 'Uint64List'
options = confini.get_section_options(section_name)
# ini1 = confini.get_option('name')
ini1 = confini.get_option('ilist')
print(options)
print('\n')
print(confini.Allini)
print('\n')
print(ini1)
"""

class IniParse:
    def __init__(self, filename):
        self.Allini = {}
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        for section in self.config.sections():
            for option, value in self.config.items(section):
                self.Allini[option] = value

    def get_section_options(self, section_name):
        dic={}
        if section_name in self.config.sections():
            section = self.config.items(section_name)
            for option, value in section:
                dic[option] = value
        return dic

    def get_option(self, option):
        # return self.ini[option]
        if option in self.Allini:
            return self.Allini[option]
        else:
            return None

