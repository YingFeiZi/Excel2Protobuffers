import sys
import subprocess
from pathlib import Path
# from PyQt6.QtCore import *
# from PyQt6.QtGui import *
# from PyQt6.QtWidgets import *
from PyQt6.QtGui import QTextCursor,QDesktopServices
from PyQt6.QtCore import Qt, QEventLoop,QObject,pyqtSignal,QTimer,QUrl
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTextEdit,
    QHBoxLayout,
    QScrollArea,
    QFileDialog,
    QLineEdit,
    QLabel,
    QSizePolicy,
)
from datetime import datetime
import warnings
import config
import generator

class EmittingStr(QObject):
    textWriten = pyqtSignal(str)
    def write(self, text):
        self.textWriten.emit(str(text))
        loop = QEventLoop()
        QTimer.singleShot(10, loop.quit)
        loop.exec()
    def SetContent(self, content):
        self.textWriten.connect(content)

class FileConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        sys.stdout = EmittingStr()
        sys.stdout.SetContent(self.outputWritten)
        sys.stderr = EmittingStr()
        sys.stderr.SetContent(self.outputWritten)
        config.initIni()
        self.selectdir = config.ini['exceldir']
        self.setWindowTitle(f"File Converter")
        self.resize(700, 520)
        # self.setGeometry(0, 0, 700, 520)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.searchlist =[]
        self.checkList = []
        self.file_list = []
        self.full_files = []
        main_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        search_label = QLabel("搜索：")
        search_label.setLineWidth(80)
        search_layout.addWidget(search_label)
        self.search_text = QLineEdit()
        self.search_text.textChanged.connect(self.searchChange)
        search_layout.addWidget(self.search_text)
        main_layout.addLayout(search_layout)

        # 上方区域：滚动视图包含文件列表，按文件最后修改时间排序
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.refresh_files()
        # scroll_layout.addWidget(self.file_list)

        scroll_widget.setLayout(self.scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # 中间区域：包含四个按钮
        button_layout = QHBoxLayout()

        reset_path_button = QPushButton("重选路径")
        reset_path_button.clicked.connect(self.buttonresetpath)
        button_layout.addWidget(reset_path_button)

        refresh_button = QPushButton("刷新")
        refresh_button.clicked.connect(self.buttonrefresh)
        button_layout.addWidget(refresh_button)

        convert_selected_button = QPushButton("转换选中")
        convert_selected_button.clicked.connect(self.convert_selected_files)
        button_layout.addWidget(convert_selected_button)

        convert_all_button = QPushButton("转换全部")
        convert_all_button.clicked.connect(self.convert_all_files)
        button_layout.addWidget(convert_all_button)

        main_layout.addLayout(button_layout)

        # 下方区域：日志显示区域
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        log_scroll = QScrollArea()
        log_scroll.setWidgetResizable(True)
        log_scroll.setWidget(self.log_area)
        main_layout.addWidget(log_scroll)
        self.setLayout(main_layout)
        
        #connect Signal

    def searchChange(self, text):
        self.refresh_files(text)

    def buttonresetpath(self):
        # Add your reset path logic here
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        if file_dialog.exec():
            self.selectdir = file_dialog.selectedFiles()[0]
            self.refresh_files()
        self.clear_log()
        
    def buttonrefresh(self):
        self.refresh_files(self.search_text.text())
        self.clear_log()

    def clear_log(self):
        self.log_area.clear()

    def refresh_files(self, search=""):
        self.full_files.clear()
        self.full_files = config.GetFullFilesByExtension(self.selectdir, config.scriptExtDict['xlsx'])
        searchfs = self.filter_files_by_search(self.full_files, search)
        self.searchlist = self.sort_files_by_mtime(searchfs)
        self.update_file_list()

    def filter_files_by_search(self, files, search):
        """根据搜索关键字过滤文件列表"""
        if search == None or search == '':
            return files
        search_terms = search.lower().split()
        return [f for f in files if any(term in str(f).lower() for term in search_terms)]

    def sort_files_by_mtime(self, files):
        """根据文件的修改时间对文件列表进行排序"""
        return sorted(files, key=lambda x: Path(x).stat().st_mtime, reverse=True)

    def update_file_list(self):
        """更新文件列表UI"""
        # 先清除旧的文件列表项
        self.clear_file_list()

        # 尝试获取并处理每个文件的信息，优化性能和异常处理
        file_info = self.get_file_info(self.searchlist)

        # 添加新的文件列表项
        index=0
        for file_path, file_name, last_time in file_info:
            index=index+1
            self.add_file_to_list(file_path, file_name, last_time, index)

    def clear_file_list(self):
        """清除文件列表UI"""
        for box in self.file_list:
            self.scroll_layout.removeWidget(box)
        self.file_list.clear()
        self.checkList.clear()

    def get_file_info(self, searchlist):
        """批量获取文件信息，优化性能"""
        file_info = []
        try:
            for file in searchlist:
                pf = Path(file)
                if pf.is_file():
                    lasttime = pf.stat().st_mtime
                    file_info.append((file, pf.name, lasttime))
        except Exception as e:
            print(f"Error accessing file system: {e}")
        return file_info

    def add_file_to_list(self, file_path, file_name, last_time, index):
        """向文件列表UI添加一个文件"""
        layitem = QHBoxLayout()
        layitem.setContentsMargins(4, 0, 4, 0)
        item = QCheckBox()
        item.setText(file_name)
        item.stateChanged.connect(lambda state: self.check_box_state_changed(state, file_name))
        layitem.addWidget(item)
        
        label = QLabel()
        label.setLineWidth(120)
        label.setText(datetime.fromtimestamp(last_time).strftime("%Y-%m-%d %H:%M:%S"))
        layitem.addWidget(label)
        
        btnChange = QPushButton("转换")
        btnChange.setFixedWidth(60)
        btnChange.clicked.connect(lambda checked: self.convert_file(file_name=file_name))
        layitem.addWidget(btnChange)
        
        btnOpen = QPushButton("打开")
        btnOpen.setFixedWidth(60)
        btnOpen.clicked.connect(lambda checked: self.open_folder_with_file(path_to_file=file_path))
        layitem.addWidget(btnOpen)

        widget = QWidget()
        if index%2==0:
            widget.setStyleSheet("background-color: #CDCDCD;")
        else:
            widget.setStyleSheet("background-color: #ffffff;")
        widget.setFixedHeight(30)
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layitem)
        self.file_list.append(widget)
        self.scroll_layout.addWidget(widget)

    def check_box_state_changed(self, state, filename):
        # 状态改变时的操作

        if state:
            self.checkList.append(filename)
        else:
            self.checkList.remove(filename)

    def convert_file(self, file_name):
        # 文件转换操作

        self.log_area.append(f"Converting selected file: {file_name}")
        config.cleanExcel()
        config.CopyToFolder(self.selectdir + "/" +  file_name)
        generator.DoAllOpreater()
        
    def open_folder_with_file(self,path_to_file):
        # 打开包含文件的文件夹

        # folder_path = str(Path(path_to_file).parent)  # 获取文件所在的目录
        # QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))
        command = f"explorer.exe /select, {path_to_file}"
        subprocess.call(command, shell=True)

    def convert_selected_files(self):
        config.cleanExcel()
        if len(self.checkList) < 1:
            print("No files selected for conversion.")
            return
        for item in self.checkList:
            self.log_area.append(f"Converting selected file: {item}")
            config.CopyToFolder(f"{self.selectdir}/{item}")
        generator.DoAllOpreater()

    def convert_all_files(self):
        config.cleanExcel()
        for item in self.full_files:
            p = Path(item)
            self.log_area.append(f"Converting all files: {p.name}")
            config.CopyToFolder(p.name)
        generator.DoAllOpreater()

    def outputWritten(self, text):
        cursor = self.log_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)
        self.log_area.setTextCursor(cursor)
        self.log_area.ensureCursorVisible()

class EmittingWarring(QObject):
    textWriten = pyqtSignal(str)

    def showwarning(self, message, category, filename, lineno, file=None, line=None):
        formatted_message = f"{category.__name__}: {message} \n位置: {filename}:{lineno}"
        self.textWriten.emit(str(formatted_message))
        loop = QEventLoop()
        QTimer.singleShot(10, loop.quit)
        loop.exec()
    def SetContent(self, content):
        self.textWriten.connect(content)
        warnings.showwarning = self.showwarning

if __name__ == '__main__':
    # 或者禁用所有来自某个模块的警告
    warnings.filterwarnings("ignore")

    app = QApplication(sys.argv)
    converter_app = FileConverterApp()
    waring = EmittingWarring()
    waring.SetContent(converter_app.outputWritten)
    converter_app.show()
    sys.exit(app.exec())