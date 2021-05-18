class Kiwoom(QAxWidget):
    def __init__(self, caller):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

        self.caller = caller

    def setrealreg(self, scrnum, trcode, fid, realtype):
        self.dynamicCall("SetRealReg(QString, QString, QString, QString)", scrnum, trcode, fid, realtype)

    def _receive_real_data(self, scode, realtype, realdata):
        if realtype == "주식체결":
            list = []
            # .....
            list.append()

            self.caller.gridview(list)


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.kiwoom = Kiwoom(self)
        self.kiwoom.comm_connect()

    def test(self):
        self.kiwoom.setrealreg(self.getnum(), code_, "9001;10", "0")

    def gridview(self, list):
        print(list)

2
e