import os, sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from search_src.tag import Tag

# Files 클래스
class Files():  
    ## 생성자
    def __init__(self, keyword:str, type:str, path:str, tag:Tag) -> None:
        self.files = [] # List: File                # File 리스트
        self.folders = [] # List: Folder            # Folder 리스트 
        self.keyword = keyword                      # 검색어
        self.type = type                            # 검색 타입: 파일, 확장자, 태그, 내용
        self.path = path                            # 검색 경로
        self.tag = tag                              # 태그 목록

        # 파일 타입
        self.FILE = '파일명'
        self.EXTNESION = '확장자명'
        self.TAG = '태그명'
        self.CONTENTS = '내용'

    #-------------------------------------------------------------------------------------------------
    ## 탐색 함수
    # 탐색 함수 시작점: 키워드의 타입에 따라 search_file, search_extention, search_tag, earch_contents 함수 실행
    def search(self):
        if self.type == self.FILE:
            self.search_file(self.path)
        elif self.type == self.EXTNESION:
            self.search_extension(self.path)
        elif self.type == self.TAG:
            self.search_tag()
        elif self.type == self.CONTENTS:
            self.search_contents(self.path)

    ## 파일 탐색: 키워드의 타입이 FILE인 경우
    def search_file(self, path) -> None:
        try:
            with os.scandir(path) as entries:
                for entry in entries:     
                    file = self.File(entry, self.tag)
                    if entry.is_file():
                        if self.keyword in file.name:
                            self.files.append(file)
                    elif entry.is_dir():
                        file.extension = 'Folder'
                        if self.keyword in file.name:
                            self.folders.append(file)

                        self.search_file(entry.path)
        except Exception as e:
            print(f'{path}에 접근 권한이 없습니다.')
            print(f'에러코드: {e}')

    ## 파일 탐색: 키워드의 타입이 EXTENSION인 경우
    def search_extension(self, path) -> None:
        try:
            with os.scandir(path) as entries:
                for entry in entries:     
                    if entry.is_file():
                        file = self.File(entry, self.tag)
                        if self.keyword in file.extension:
                            self.files.append(file)
                    elif entry.is_dir():
                        self.search_extension(entry.path)
        except:
            print(f'{path}에 접근 권한이 없습니다.')

    ## 파일 탐색: 키워드의 타입이 TAG인 경우
    def search_tag(self) -> None:
        try:
            if self.keyword in self.tag.keyword_tag:
                for tag_path in self.tag.keyword_tag[self.keyword]:
                    path = os.path.dirname(tag_path)
                    with os.scandir(path) as entries:
                        for entry in entries:
                            if entry.path == tag_path:
                                file = self.File(entry, self.tag)
                                self.files.append(file)

        except Exception as e:
            print(f'에러코드: {e}')

    ## 파일 탐색: 키워드의 타입이 CONTENTS인 경우
    def search_contents(self, path) -> None:
        try:
            with os.scandir(path) as entries:
                for entry in entries: 
                    if entry.is_file():
                        file = self.File(entry, self.tag)
                        with open(path+os.sep+file.full_name, 'r', encoding='UTF8') as f:
                            try:                                                        
                                if self.keyword in f.read():                          
                                     self.files.append(file)                                           
                                f.close()
                            except:                                                     
                                pass
                    elif entry.is_dir():
                        self.search_contents(entry.path)
        except Exception as e:
            print(f'{path}에 접근 권한이 없습니다.')
            print(f'오류 : {e}')

    #-------------------------------------------------------------------------------------------------
    # File 클래스
    class File():
        ## 생성자
        def __init__(self, entry, tag:Tag):
            self.full_name = ''                     # 이름
            self.name = ''                          # 이름(확장자 제거)
            self.extension = ''                     # 확장자
            self.tag = []                           # 태그 목록
            self.path = ''                          # 현재 위치(경로)
            self.byte = ''                          # 용량(byte로 표현)
            self.byte_unit = ''                     # 용량(단위별 표현: b, kb, mb, tb)
            self.created_at = ''                    # 생성일
            self.updated_at = ''                    # 수정일(마지막 수정일)

            self.setName(entry)
            self.setExtension(entry)
            self.setPath(entry.path)
            self.setByte(entry.stat().st_size)
            self.setCreated_at(entry.path)
            self.setUpdated_at(entry.stat().st_mtime)
            self.setTag(tag.file_tag)

        ## Setter
        def setName(self, entry):
            self.full_name = entry.name
            self.name = os.path.splitext(entry.name)[0]
        def setExtension(self, entry):
            self.extension = os.path.splitext(entry.name)[1]
        def setPath(self, path):
            self.path = path
        def setByte(self, byte):
            self.byte = byte
            self.__set_byte_unit()
        def setCreated_at(self, path):
            self.created_at = datetime.fromtimestamp(os.path.getmtime(path))
        def setUpdated_at(self, updated_at):
            self.updated_at = datetime.fromtimestamp(updated_at)
        def setTag(self, file_tag):
            if self.path in file_tag:
                self.tag = file_tag[self.path]
        ## 변수 byte_unit의 초기화를 위한 함수
        def __set_byte_unit(self) -> None:
            size_names = ['B', 'KB', 'MB', 'TB']

            if self.byte == 0:
                self.byte_unit = '0B'
                
            else:
                import math 
                square_root = int(math.floor(math.log(self.byte, 1024)))
                square = math.pow(1024, square_root)
                self.byte_unit = f"{round(self.byte / square, 2)}{size_names[square_root]}"


