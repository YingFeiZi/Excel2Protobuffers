import codecs
import csv
from pathlib import Path
import openpyxl
import config

class excel2csv():
    def __init__(self):
        self.output_dir = config.ini['datadir']
        self.input_start = int(config.ini['xlsstar'])
        self.output_start = int(config.ini['csvstar'])

    def get_red(self,text):
        """
        Print text in red color.
        """
        return "\033[91m {}\033[00m".format(text)

    def get_green(self,text):
        """
        Print text in green color.
        """
        return "\033[92m {}\033[00m".format(text)

    def get_yellow(self,text):
        """
        Print text in yellow color.
        """
        return "\033[93m {}\033[00m".format(text)

    def get_blue(self,text):
        """
        Print text in blue color.
        """
        return "\033[94m {}\033[00m".format(text)

    def get_purple(self,text):
        """
        Print text in purple color.
        """
        return "\033[95m {}\033[00m".format(text)

    def get_cyan(self,text):
        """
        Print text in cyan color.
        """
        return "\033[96m {}\033[00m".format(text)

    def get_light_gray(self,text):
        """
        Print text in light gray color.
        """
        return "\033[97m {}\033[00m".format(text)

    def get_dark_gray(self,text):
        """
        Print text in dark gray color.
        """
        return "\033[98m {}\033[00m".format(text)

    def LogTableInfo(self, f, row, col, log=""):
        str1 = f"ERROR:  {row} row {col} col, Value: {log}"
        # print(str1)
        file = open("errorTable.txt", 'a')
        file.write(f"ERROR: {str1}\n")
        file.close()




    # 帮助函数，用于检查表格中是否有逗号错误
    # def check_for_comma_error(worksheet, row, col_num):
    #     cell_value = str(worksheet.cell(row, col_num).value)
    #     if ',' in cell_value:
    #         return True
    #     elif isinstance(cell_value, float):
    #         return not isinstance(cell_value, int)
    #     return False

    def excel_to_csv(self,fileName):
        intPutFileName = str(fileName)  # 输入的文件名
        file_name = Path(fileName).name  # 文件名
        excel_file_name = file_name.split('.')[0]  # Excel文件名
        outPutFileName = str(Path(self.output_dir).joinpath(excel_file_name.split("-")[0] + '.csv'))  # 输出的文件名
        workbook = openpyxl.load_workbook(intPutFileName,True, False,True)
        worksheet = workbook.active
        error_count = 0

        try:
            with codecs.open(outPutFileName, 'w', encoding='utf-8') as f:
                writer = csv.writer(f)
                for row in range(1,self.output_start):
                    writer.writerow([])
                rows = worksheet.rows
                for row_num, raw_value in enumerate(rows):
                    if row_num < (self.input_start - 1):
                        continue
                    rowvalues = []
                    for col_num, col_value in enumerate(raw_value):
                        value = col_value.value
                        if isinstance(value, float):
                            if value == int(value):
                                value = int(value)
                                rowvalues.append(str(value))
                            else:
                                rowvalues.append(str(value))
                        else:
                            rowvalues.append(value)
                    writer.writerow(rowvalues)
        except Exception as e:
                print("  导表失败:" + intPutFileName + "," + " 错误信息:" + str(e))  # 打印导出失败信息
        workbook.close()
        return error_count

    def run(self):
        print('---------------- 将excel生成CSV数据 ----------------')
        excels = config.GetFilesByExtension(config.GEN_DIR_DICT['xlsx'],config.scriptExtDict['xlsx'])
        index =  1
        count = len(excels)
        for excel in excels:
            name, ext = config.GetFileNameExt(excel)
            
            print(f"[{index}/{count}]  {str(Path(self.output_dir).joinpath(name + ''))}.csv")
            self.excel_to_csv(excel)
            index += 1