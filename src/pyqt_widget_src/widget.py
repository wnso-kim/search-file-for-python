from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.uic import loadUiType

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from search_src import fileFolder
from search_src import tag

#--------------------------------------------------------------------------
# UI Path 지정
def resource_path(relative_path):
    current_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(current_path, relative_path)

main_form = resource_path("searchFileMainUi.ui")
Main_form = loadUiType(main_form)[0]

tag_form = resource_path("searchFileTagUi.ui")
Tag_Form = loadUiType(tag_form)[0]

#--------------------------------------------------------------------------
# Main Window ui
class WindowClass(QMainWindow, Main_form):
    ## 생성자
    def __init__(self):                                            
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("파일 탐색 프로그램")

        ## Tag 객체
        self.tag = tag.Tag()

        # 사용자 정의 시그널 - 슬롯 연결
        self.notification_signal = NotificationSignal()
        self.notification_signal.created.connect(self.notification) 

        ## 옵저버 - 파일 생성 감지
        self.observer = None
        self.event_handler = Handler(self, self.notification_signal)

        ## 시그널 - 슬롯 연결
        self.searchButton.clicked.connect(self.btn_fn_search)
        self.searchComboBox.currentIndexChanged.connect(self.cb_fn_setSearchLineText)
        self.pathButton.clicked.connect(self.btn_fn_setPath)
        self.fileList.itemClicked.connect(self.clk_fn_setFileInfo)
        self.tagSaveButton.clicked.connect(self.btn_fn_save)
        self.changePathButton.clicked.connect(self.btn_fn_setChangePath)
        self.changeDetectionButton.clicked.connect(self.btn_fn_stopChangeDetection)

    #--------------------------------------------------------------------------
    # 슬롯
    ## 알림창 팝업 함수 - notification_signal.created 사용자 시그널과 연결
    def notification(self, path):
        notification_dialog = NewFileDialog(path, self, self.tag)
        notification_dialog.exec()
        
    ## 검색 함수 - searchButton.clicked 시그널과 연결
    def btn_fn_search(self):
        searchWord = self.searchLine.text()
        searchType = self.searchComboBox.currentText()
        searchPath = self.pathLine.text()

        # 지정된 검색어 또는 경로가 없을 시 경고
        if(searchWord == "" or searchPath == ""):
            QMessageBox.about(self, "Warning", f'{searchType} 또는 탐색 경로를 지정해주세요')

        # 타입에 따라 경로에서 검색
        else:
            self.fileList.clear()
            self.file_folder = fileFolder.Files(searchWord, searchType, searchPath, self.tag)
            self.file_folder.search()

            for file in self.file_folder.files:
                self.fileList.addItem(f'[파일] {file.full_name}')
            for file in self.file_folder.folders:
                self.fileList.addItem(f'[폴더] {file.full_name}')
            self.fileList.setCurrentRow(0)
    
    ## 검색어 Placeholder 설정 함수 - searchComboBox.currentIndexChanged 시그널과 연결
    def cb_fn_setSearchLineText(self):
        searchType = self.searchComboBox.currentText()
        self.searchLine.setPlaceholderText(f'여기에 {searchType}을 입력하세요')

    ## 경로 설정 함수 - pathButton.clicked 시그널과 연결
    def btn_fn_setPath(self):
        pName=QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.pathLine.setText(pName)

    ## 파일 선택 함수 - fileList.itemClicked 시그널과 연결
    def clk_fn_setFileInfo(self):
        index = self.fileList.currentRow()
        try:
            file = self.file_folder.files[index]
            self.setInfo(file)
        except:
            index = index - len(self.file_folder.files)
            folder = self.file_folder.folders[index]
            self.setInfo(folder)

    ## 태그 저장 함수 - tagSaveButton.cliecked 시그널과 연결
    def btn_fn_save(self):
        try:
            file_name = self.path_info.text()
            tags = self.tag_info.text()
            if file_name != "":
                self.tag.save(file_name, tags)
            else:
                QMessageBox.about(self, "Warning", f'파일을 선택하세요')

        except Exception as e:
            print(f"태그 저장 실패 {e}")

    ## 경로 설정 및 변경 감시 함수 - changePathButton.clicked 시그널과 연결
    def btn_fn_setChangePath(self):
        pName=QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.changePathLine.setText(pName)
        self.changeDetectionButton.setEnabled(True)
        self.changeDetectionButton.setText('파일 생성 감지중')
        self.changeDetectionButton.setStyleSheet("background-color: lightgray; color : black;border-radius:5px;")

        # 기존 감시 중지
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.unschedule_all()
            print("옵저버 취소")
            
        # 옵저버 실행
        folder_to_watch = pName  
        self.observer = Observer()  # 새로운 Observer 객체 생성
        self.observer.schedule(self.event_handler, folder_to_watch, recursive=True)
        self.observer.start()
        print("옵저버 실행")

    ## 변경 감시 취소 함수
    def btn_fn_stopChangeDetection(self):
        self.changePathLine.clear()
        self.changeDetectionButton.setDisabled(True)
        self.changeDetectionButton.setText("")
        self.changeDetectionButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        
        # 기존 감시 중지
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.unschedule_all()
            print("옵저버 취소")

    #--------------------------------------------------------------------------
    # file info 함수
    ## 파일 정보 출력 함수
    def setInfo(self, f):
        self.setIcon(f)
        self.setName(f)
        self.setTag(f)
        self.setExtension(f)
        self.setSize(f)
        self.setPath(f)
        self.setPath(f)
        self.setCreate_at(f)
        self.setUpdated_at(f)

    ## Setter
    def setIcon(self, file):
        icon_provider = QFileIconProvider()
        file_icon = icon_provider.icon(QFileInfo(file.path))
        self.icon.setPixmap(file_icon.pixmap(50, 50))
    def setName(self, file):
        self.full_name_info.setText(file.full_name)
    def setTag(self, file):
        self.tag_info.setText(' ,'.join(file.tag))
    def setExtension(self, file):
        self.extension_info.setText(file.extension)    
    def setSize(self, file):
        self.size_info.setText(f'{file.byte}byte [{file.byte_unit}]')
    def setPath(self, file):
        self.path_info.setText(file.path)
        self.path_info.setCursorPosition(0)
    def setCreate_at(self, file):
        self.created_at_info.setText(file.created_at.strftime("%Y년%m월%d일 %H시%M분"))
    def setUpdated_at(self, file):
        self.updated_at_info_1.setText(file.updated_at.strftime("수정일: %Y년%m월%d일 %H시%M분"))
        self.updated_at_info_1.setCursorPosition(0)
        self.updated_at_info_2.setText(file.updated_at.strftime("%Y년%m월%d일 %H시%M분"))
        self.updated_at_info_2.setCursorPosition(0)

#--------------------------------------------------------------------------
# 사용자 시그널 객체
class NotificationSignal(QObject):
    ## 파일 생성시 이벤트 생성 
    created = pyqtSignal(str)

# 이벤트 핸들러 - 파일 생성 탐지 
class Handler(FileSystemEventHandler):
    def __init__(self, window_instance, notification_signal):
        self.window_instance = window_instance
        self.notification_signal = notification_signal

    def on_created(self, event):
        if not event.is_directory:
            # 파일이 생성되면 notification_signal.created 시그널 발생
            path = event.src_path
            self.notification_signal.created.emit(path)

#--------------------------------------------------------------------------
# Sub Window Ui
class NewFileDialog(QDialog, Tag_Form):
    ## 생성자
    def __init__(self, path, parent, tag:tag.Tag):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("파일 생성 알림")

        ## Tag 객체
        self.tag = tag

        ## 시그널 - 슬롯 연결
        self.tagSaveButton.clicked.connect(self.btn_fn_save)

        try:
            dir_path = os.path.dirname(path)
            with os.scandir(dir_path) as entries:
                for entry in entries:
                    if entry.path == path:
                        self.file = fileFolder.Files.File(entry, tag)
                        self.setInfo()
        except Exception as e:
            print(f'에러코드: {e}')

    ## 태그 저장 함수 - tagSaveButton.cliecked 시그널과 연결
    def btn_fn_save(self):
        try:
            file_name = self.path_info.text()
            tags = self.tag_info.text()
            if tags != "":
                self.tag.save(file_name, tags)
                QMessageBox.about(self, "알림", f'태그{tags}가 저장되었습니다.')
            else:
                QMessageBox.about(self, "경고", '태그를 입력하세요')

        except Exception as e:
            print(f"태그 저장 실패 {e}")

    ## 새로운 파일 정보 Setter
    def setInfo(self):
        icon_provider = QFileIconProvider()
        file_icon = icon_provider.icon(QFileInfo(self.file.path))
        self.icon.setPixmap(file_icon.pixmap(50, 50))                           # icon
        self.full_name_info.setText(self.file.full_name)                        # full_name
        self.full_name_info.setCursorPosition(0)
        self.extension_info.setText(self.file.extension)                        # extension
        self.size_info.setText(f'{self.file.byte}byte [{self.file.byte_unit}]') # size
        self.path_info.setText(self.file.path)                                  # path
        self.path_info.setCursorPosition(0)
        # updated_at
        self.updated_at_info.setText(self.file.updated_at.strftime("수정일: %Y년%m월%d일 %H시%M분"))  
        self.updated_at_info.setCursorPosition(0)