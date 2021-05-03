import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *     # QAxWidget 사용
from PyQt5.QtCore import *         # QEventloop()사용
import logging

# logging.basicConfig(filename="log.txt", level=logging.ERROR)    # 테스트가 끝나면 이조건을 설정
logging.basicConfig(level=logging.INFO)

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()

        # 이벤트루프 변수설정
        self.login_event_loop = QEventLoop()

        ## 키움API 인스턴스 생성
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

        ## 이벤트에 슬롯 연결
        self.set_event_slot()

        self.login()

    def set_event_slot(self):
        self.OnEventConnect.connect(self.handler_login)
        self.OnReceiveTrData.connect(self.handler_tr_data)
        # self.OnReceiveRealData.connect(self.handler_real_data)
        self.OnReceiveMsg.connect(self.handler_msg)

    def handler_login(self, errCode):
        logging.info(f"handler login {errCode}")
        if errCode == 0:
            print("연결되었습니다")
        else:
            print("연결되지 않았습니다.")
        self.login_event_loop.exit()

    def handler_tr_data(self):
        pass

    def handler_msg(self, sCcrNo, sRQName, sTrCode, Msg):
        logging.info(f"OnReceiveMsg {sCcrNo} {sRQName} {sTrCode} {Msg}")

    def login(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    app.exec_()
'''
