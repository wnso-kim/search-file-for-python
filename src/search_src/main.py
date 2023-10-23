import sys, os
from PyQt6.QtWidgets import *

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from pyqt_widget_src import widget


#--------------------------------------------------------------------------
# main 함수
if __name__ == '__main__':
    app = QApplication(sys .argv)
    myWindow = widget.WindowClass( )   # Main Window 생성
    myWindow.show()             # Main Window 실행

    sys.exit(app.exec())

