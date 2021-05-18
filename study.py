import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from datetime import datetime

class Sig_cl(QObject):
    sig_ = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def signal_(self, tag):
        self.sig_.emit(tag)

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()
        self.sig_cl = Sig_cl()
        self.dSig = {}          # key-이벤트 구분, value-각 이벤트 별 변수 리스트

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):            # 시그널 슬롯
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveMsg.connect(self._receive_msg)
        self.OnReceiveConditionVer.connect(self._receive_condition_ver)
        self.OnReceiveTrCondition.connect(self._receive_tr_condition)
        self.OnReceiveRealCondition.connect(self._receive_real_condition)
        self.OnReceiveTrData.connect(self._receive_tr_data)
        self.OnReceiveRealData.connect(self._receive_real_data)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)

    # Login 및 연결상태 관련 부분

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret

    def get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret

    # 이벤트 수신 부분

    def _event_connect(self, iErrCode):
        if iErrCode == 0:
            print("connected")
            self.login = True
        else:
            print("disconnected")
            self.login = False

        self.login_event_loop.exit()

    def _receive_msg(self, sScrNo, sRqName, sTrCode, sMsg):
        tag = "receive_msg"
        self.dSig[tag] = [sScrNo, sRqName, sTrCode, sMsg]
        now = datetime.now()
        print(tag, now)
        self.sig_cl.signal_(tag)

    def _receive_condition_ver(self, iRet, sMsg):
        tag = "receive_condition_ver"
        self.dSig[tag] = [iRet, sMsg]
        self.sig_cl.signal_(tag)

    def _receive_tr_condition(self, sScrNo, sStockCodeList, sConditionName, iIndex, iNext):
        tag = "receive_tr_condition"
        self.dSig[tag] = [sScrNo, sStockCodeList, sConditionName, iIndex, iNext]
        self.sig_cl.signal_(tag)

    def _receive_real_condition(self, sStockCode, sType, sConditionName, sConditionIndex):
        tag = "receive_real_condition"
        self.dSig[tag] = [sStockCode, sType, sConditionName, sConditionIndex]
        self.sig_cl.signal_(tag)

    def _receive_tr_data(self, sScrNo, sRqName, sTrCode, sRecordName, sPreNext, unused1, unused2, unused3, unused4):
        tag = "receive_tr_data"
        self.dSig[tag] = [sScrNo, sRqName, sTrCode, sRecordName, sPreNext, unused1, unused2, unused3, unused4]
        now = datetime.now()
        print(tag, now)
        self.sig_cl.signal_(tag)

    def _receive_real_data(self, sJongmokCode, sRealType, sRealData):
        tag = "receive_real_data"
        self.dSig[tag] = [sJongmokCode, sRealType, sRealData]
        self.sig_cl.signal_(tag)

    def _receive_chejan_data(self, sGubun, iItemCnt, sFidList):
        tag = "receive_chejan_data"
        self.dSig[tag] = [sGubun, iItemCnt, sFidList]
        self.sig_cl.signal_(tag)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    # account_number = kiwoom.get_login_info("ACCNO")
    # account_number = account_number.split(';')[0]
    # print(account_number)

main.py
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from kiwoom import *
from datetime import datetime

form_class = uic.loadUiType("basic.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Kiwoom 접속
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

        self.kiwoom.sig_cl.sig_.connect(self._receive_signal)

        if self.kiwoom.login == True:
            self.statusBar().showMessage('로그인 성공')
        else:
            self.statusBar().showMessage('로그인 실패')

        acc_count = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
        accounts = self.kiwoom.get_login_info("ACCNO")
        accounts_list = accounts.split(';')[0:acc_count]
        self.account = accounts_list[0]
        print(self.account)

        self.pushButton_exit.clicked.connect(self.pushButton_exit_clicked)

        self.main()

    def _receive_signal(self, tag):
        print(tag)
        if tag == "receive_msg":
            self.receive_msg(tag)
        elif tag == "receive_condition_ver":
            self.receive_condition_ver(tag)
        elif tag == "receive_tr_condition":
            self.receive_tr_condition(tag)
        elif tag == "receive_real_condition":
            self.receive_real_condition(tag)
        elif tag == "receive_tr_data":
            self.receive_tr_data(tag)
        elif tag == "receive_real_data":
            self.receive_real_data(tag)
        elif tag == "receive_chejan_data":
            self.receive_chejan_data(tag)

    def receive_msg(self, tag):
        now = datetime.now()
        print("msg : ", tag, self.kiwoom.dSig[tag], now)

    def receive_condition_ver(self, tag):
        print("condition_ver : ", tag, self.kiwoom.dSig[tag])

    def receive_tr_condition(self, tag):
        print("tr_condition : ", tag, self.kiwoom.dSig[tag])

    def receive_real_condition(self, tag):
        print("real_condition : ", tag, self.kiwoom.dSig[tag])

    def receive_tr_data(self, tag):
        now = datetime.now()
        print("tr_data : ", tag, self.kiwoom.dSig[tag], now)

    def receive_real_data(self, tag):
        print("real_data : ", tag, self.kiwoom.dSig[tag])

    def receive_chejan_data(self, tag):
        print("chejan_data : ", tag, self.kiwoom.dSig[tag])

    def main(self):
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account)
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opw00018_req", "opw00018", 0, "0151")

    def pushButton_exit_clicked(self):
        myWindow.hide()
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())