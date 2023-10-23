import os, sys, json

#------------------------------------------------------------------------------------------------- 
class Tag():
    ## 생성자
    def __init__(self) -> None:
        # file_tag는 편의상 파일이름으로 표기하고, 실제값은 경로+파일+확장자로 넣음(같은 이름의 파일이 존재할 수 있으므로)
        self.file_tag = {}              # {'파일이름1':[태그1, 태그2, ..], '파일이름2': [태그1, 태그2, ...]}
        self.keyword_tag = {}           # {'태그1': [파일이름1, 파일이름2, ...], '태그2': [파일이름1, 파일이름2, ...]}

        # JSON 파일 경로 설정
        ## (search_file)file_tag_list.json 파일 경로 -> file_tag_path
        ## (search_file)keyword_tag_list.json 파일 경로 -> keyword_tag_path
        self.file_tag_path, self.keyword_tag_path = self._readJsonTag()
        self._setTag()


    ## Json 파일 경로 설정 함수
    def _readJsonTag(self) -> (os.path, os.path):
        # 실행 파일이 있는 디렉토리
        if getattr(sys, 'frozen', False):
            # PyInstaller로 패키징된 실행 파일
            current_dir = sys._MEIPASS
        else:
            # 일반적인 Python 스크립트
            current_dir = os.path.dirname(os.path.abspath(__file__))

        # 저장할 파일 이름과 경로
        file_json = "(search_file)file_tag_list.json"
        keyword_json = "(search_file)keyword_tag_list.json"

        file_tag_path = os.path.join(current_dir, file_json)
        keyword_tag_path = os.path.join(current_dir, keyword_json)

        return file_tag_path,keyword_tag_path

    ## self.name_tag 와 self.keyword_tag 초기화
    def _setTag(self) -> None:
        # JSON 파일 읽기
        ## self.file_tag_path로 json 열기 -> self.file_tag 초기화
        try:
            with open(self.file_tag_path, 'r') as json_file:
                self.file_tag = json.load(json_file)
        except:
            self.file_tag = {}

        ## keyword_tag_path json 열기 -> self.keyword_tag 초기화
        try:
            with open(self.keyword_tag_path, 'r') as json_file:
                self.keyword_tag = json.load(json_file)
        except:
            self.keyword_tag = {}


    
    def save(self, file_name, tags) -> None:
        self.file_tag[file_name] = [tag.strip() for tag in tags.split(',')]
        for tag in tags.split(','):
            tag = tag.strip()  # 앞뒤 공백을 제거
            if tag in self.keyword_tag:
                # 이미 존재하는 키인 경우
                self.keyword_tag[tag].append(file_name)  # new_data는 추가하려는 데이터
            else:
                # 존재하지 않는 키인 경우, 새로운 키와 데이터를 생성
                self.keyword_tag[tag] = [file_name]


        with open(self.file_tag_path, 'w') as json_file:
            json.dump(self.file_tag, json_file)

        with open(self.keyword_tag_path, 'w') as json_file:
            json.dump(self.keyword_tag, json_file)

