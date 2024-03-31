import sys
from pathlib import Path
# from PyQt6.QtCore import *
# from PyQt6.QtGui import *
# from PyQt6.QtWidgets import *
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import Qt, QEventLoop,QObject,pyqtSignal,QTimer
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
)
import config
import generator

class EmittingStr(QObject):
    textWriten = pyqtSignal(str)
    def write(self, text):
        self.textWriten.emit(str(text))
        loop = QEventLoop()
        QTimer.singleShot(10, loop.quit)
        loop.exec()

class FileConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        sys.stdout = EmittingStr()
        sys.stdout.textWriten.connect(self.outputWritten)
        sys.stderr = EmittingStr()
        sys.stderr.textWriten.connect(self.outputWritten)
        config.initIni()
        self.selectdir = config.ini['exceldir']
        self.setWindowTitle("File Converter")
        self.setFixedSize(700, 520)
        # self.setGeometry(0, 0, 700, 520)
        self.searchlist =[]
        self.file_list = []
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
        self.scroll_layout = QVBoxLayout()
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
        button_layout.addWidget(reset_path_button)

        refresh_button = QPushButton("刷新")
        button_layout.addWidget(refresh_button)

        convert_selected_button = QPushButton("转换选中")
        button_layout.addWidget(convert_selected_button)

        convert_all_button = QPushButton("转换全部")
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
        reset_path_button.clicked.connect(self.buttonresetpath)
        refresh_button.clicked.connect(self.buttonrefresh)
        convert_selected_button.clicked.connect(self.convert_selected_files)
        convert_all_button.clicked.connect(self.convert_all_files)

    def searchChange(self, text):
        self.refresh_files(text)

    def buttonresetpath(self):
        # Add your reset path logic here
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        if file_dialog.exec():
            self.selectdir = file_dialog.selectedFiles()[0]
            self.refresh_files()
    def buttonrefresh(self):
        self.refresh_files(self.search_text.text())

    def refresh_files(self, search=""):
        # Add your refresh files logic here
        fs = config.GetFullFilesByExtension(self.selectdir, config.scriptExtDict['xlsx'])
        searchfs = [f for f in fs if search in str(f).split("\\")[-1] or search in str(f).split("\\")[-1].lower()]
        self.searchlist = sorted(searchfs, key=lambda x: Path(x).stat().st_mtime, reverse=False)
        for box in self.file_list:
            self.scroll_layout.removeWidget(box)
        self.file_list.clear()

        for file in self.searchlist:
            item = QCheckBox()
            item.setText(file.name)
            self.file_list.append(item)
            self.scroll_layout.addWidget(item)

    def convert_selected_files(self):
        for item in self.file_list:
            if item.checkState() == Qt.CheckState.Checked:
                self.log_area.append(f"Converting selected file: {item.text()}")
                config.CopyToFolder(self.selectdir + "/" +  item.text())
        generator.DoAllOpreater()

    def convert_all_files(self):
        for item in self.file_list:
            self.log_area.append(f"Converting all files: {item.text()}")
            config.CopyToFolder(item.text())
        generator.DoAllOpreater()

    def outputWritten(self, text):
        cursor = self.log_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)
        self.log_area.setTextCursor(cursor)
        self.log_area.ensureCursorVisible()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter_app = FileConverterApp()
    converter_app.show()
    sys.exit(app.exec())


# import sys
# import os
# import config
# import generator
# from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer,QObject,QEventLoop
# from PyQt6.QtGui import QTextCursor
# from PyQt6.QtWidgets import (
#     QApplication,
#     QCheckBox,
#     QPushButton,
#     QVBoxLayout,
#     QHBoxLayout,
#     QScrollArea,
#     QFileDialog,
#     QLineEdit,
#     QLabel,
#     QWidget,
#     QTextEdit,
# )

# class EmittingStr(QObject):
#     textWriten = pyqtSignal(str)

#     def write(self, text):
#         self.textWriten.emit(str(text))
#         loop = QEventLoop()
#         QTimer.singleShot(10, loop.quit)
#         loop.exec()


# class FileConverterApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         config.initIni()
#         self.selectdir = config.ini['exceldir']
#         self.setWindowTitle("File Converter")
#         self.setFixedSize(700, 520)
#         self.searchlist = []
#         self.file_list = []
#         self.main_layout = QVBoxLayout()
#         self.initUI()
#         sys.stdout = EmittingStr()
#         sys.stdout.textWriten.connect(self.outputWritten)
#         sys.stderr = EmittingStr()
#         sys.stderr.textWriten.connect(self.outputWritten)

#     def initUI(self):
#         # UI components setup
#         search_layout = QHBoxLayout()
#         search_label = QLabel("搜索：")
#         search_label.setFixedWidth(100)
#         search_layout.addWidget(search_label)
#         self.search_text = QLineEdit()
#         self.search_text.textChanged.connect(self.searchChange)
#         search_layout.addWidget(self.search_text)
#         self.main_layout.addLayout(search_layout)

#         self.scroll_area = QScrollArea()
#         self.scroll_widget = QWidget()
#         self.scroll_layout = QVBoxLayout()
#         self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
#         self.refresh_files()
#         self.scroll_widget.setLayout(self.scroll_layout)
#         self.scroll_area.setWidget(self.scroll_widget)
#         self.scroll_area.setWidgetResizable(True)
#         self.main_layout.addWidget(self.scroll_area)

#         self.button_layout = QHBoxLayout()

#         reset_path_button = QPushButton("重选路径")
#         reset_path_button.clicked.connect(self.reset_path)
#         self.button_layout.addWidget(reset_path_button)

#         refresh_button = QPushButton("刷新")
#         refresh_button.clicked.connect(self.refresh_files)
#         self.button_layout.addWidget(refresh_button)

#         convert_selected_button = QPushButton("转换选中")
#         convert_selected_button.clicked.connect(self.convert_selected_files)
#         self.button_layout.addWidget(convert_selected_button)

#         convert_all_button = QPushButton("转换全部")
#         convert_all_button.clicked.connect(self.convert_all_files)
#         self.button_layout.addWidget(convert_all_button)

#         self.main_layout.addLayout(self.button_layout)

#         self.log_area = QTextEdit()
#         self.log_area.setReadOnly(True)
#         log_scroll = QScrollArea()
#         log_scroll.setWidgetResizable(True)
#         log_scroll.setWidget(self.log_area)
#         self.main_layout.addWidget(log_scroll)os
#         self.setLayout(self.main_layout)

#     def searchChange(self, text):
#         self.refresh_files(search=text)

#     def reset_path(self):
#         file_dialog = QFileDialog()
#         file_dialog.setFileMode(QFileDialog.FileMode.Directory)
#         if file_dialog.exec():
#             self.selectdir = file_dialog.selectedFiles()[0]
#             self.refresh_files()

#     def refresh_files(self, search=""):
#         # Simplified and optimized file listing
#         fs = config.GetFullFilesByExtension(self.selectdir, config.scriptExtDict['xlsx'])
#         searchfs = [f for f in fs if search in f or search in f.lower()]
#         self.searchlist = sorted(searchfs, key=os.path.getmtime, reverse=False)
#         self.updateFileList()

#     def updateFileList(self):
#         for box in self.file_list:
#             self.scroll_layout.removeWidget(box)
#         self.file_list.clear()

#         for file in self.searchlist:
#             item = QCheckBox()
#             item.setText(os.path.abspath(file))
#             self.file_list.append(item)
#             self.scroll_layout.addWidget(item)

#     def convert_selected_files(self):
#         selected_files = [file for file in self.file_list if file.checkState() == Qt.CheckState.Checked]
#         self.convert_files(selected_files)

#     def convert_all_files(self):
#         self.convert_files(self.file_list)

#     def convert_files(self, files_to_convert):
#         for file in files_to_convert:
#             self.log_area.append(f"Converting file: {file.text()}")
#             try:
#                 config.CopyToFolder(file.text())
#                 generator.DoAllOpreater()
#             except Exception as e:
#                 self.log_area.append(f"Error converting {file.text()}: {str(e)}")

#     def outputWritten(self, text):
#         cursor = self.log_area.textCursor()
#         cursor.movePosition(QTextCursor.MoveOperation.End)
#         cursor.insertText(text)
#         self.log_area.setTextCursor(cursor)
#         self.log_area.ensureCursorVisible()



# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     converter_app = FileConverterApp()
#     converter_app.show()
#     sys.exit(app.exec())