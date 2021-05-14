import sys
import os
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *     # QAxWidget 사용
from PyQt5.QtCore import *         # QEventloop()사용
import logging

logging.basicConfig(filename="log.txt", level=logging.ERROR)    # 테스트가 끝나면 이조건을 설정
# logging.basicConfig(level=logging.INFO)                           # 테스트용

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()

        # 이벤트루프 설정
        self.login_event_loop = QEventLoop()
        self.tr_event_loop = QEventLoop()
        self.option_data_loop = QEventLoop()

        # 변수 설정
        self.df_stock_info_exist = False

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

    def handler_tr_data(self, scrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        logging.info(f"OnReceiveTrData {scrNo}, {sRQName}, {sTrCode}, {sRecordName}")

        if sRQName == "주식기본정보요청":
            # print("주식기본정보요청입니다.")

            code = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "종목코드").strip()
            data = {}
            data['종목명'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "종목명").strip()
            data['액면가'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "액면가").strip()
            data['자본금'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "자본금").strip()
            data['상장주식'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "상장주식").strip()
            data['신용비율'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "신용비율").strip()
            data['연중최고'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "연중최고").strip()
            data['연중최저'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "시가총액").strip()
            data['결산월'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "결산월").strip()
            data['시가총액비율'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "시가총액비중").strip()
            data['외인소진율'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "외인소진율").strip()
            data['대용가'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "대용가").strip()
            data['PER'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "PER").strip()
            data['EPS'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "EPS").strip()
            data['PBR'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "PBR").strip()
            data['EV'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "EV").strip()
            data['BPS'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "BPS").strip()
            data['매출액'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "매출액").strip()
            data['영업이익'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "영업이익").strip()
            data['당기순이익'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "당기순이익").strip()
            data['250최고'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "250최고").strip()
            data['250최저'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "250최저").strip()
            data['시가'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "시가").strip()
            data['고가'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "고가").strip()
            data['저가'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "저가").strip()
            data['기준가'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "기준가").strip()
            data['현재가'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "현재가").strip()
            data['액면가단위'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "액면가단위").strip()
            data['유통주식'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "유통주식").strip()
            data['유통비율'] = self.dynamicCall("GetCommData(QString, QString, Int, QString)", sTrCode, sRQName, 0, "유통비율").strip()
            print("종목코드: ", code)

            # columns = ['종목코드', '종목명', '액면가', '자본금', '상장주식', '신용비율', '연중최고', '연중최저', '결산월', '시가총액비율', '외인소진비율', '대용가',
            #              'PER', 'EPS', 'PBR', 'EV', 'BPS', '매출액', '영업이익', '당기순이익', '250최고', '250최저', '시가', '고가', '저가', '기준가', '현재가'
            #              '액면가단위', '유통주식', '유통비율']

            # self.stock_info_df =pd.DataFrame(data, index=[code])

            # print('df파일존재여부', self.df_stock_info_exist)

            if self.df_stock_info_exist :
                self.df_stock_info.loc[code] = data

            else:
                self.df_stock_info = pd.DataFrame(data, index=[code])
                self.df_stock_info_exist = True
                print('df파일존재여부', self.df_stock_info_exist )

            # print("데이터프레임: ", self.df_stock_info)
            self.tr_event_loop.exit()


    def handler_msg(self, sCcrNo, sRQName, sTrCode, Msg):
        logging.info(f"OnReceiveMsg {sCcrNo} {sRQName} {sTrCode} {Msg}")

    def login(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()

    def call_basic_info(self, code):
        # print("주식기본정보요청함수.")
        self.dynamicCall("SetInputValue(QStirng, QString)", "종목코드", code)
        self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식기본정보요청", "opt10001", '0', "1000")
        self.tr_event_loop.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    app.exec_()
