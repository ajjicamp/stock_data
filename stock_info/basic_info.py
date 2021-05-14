from trkiwoom.kiwoom import *
import time
from pandas import *
import os
import xlrd

class Basic_info:
    def __init__(self):

        self.kiwoom = Kiwoom()
        self.get_basic_info('kospi')
        self.get_basic_info('kosdaq')

    def get_basic_info(self, market):
        # kospi종목 주식기본정보요청하여 엑셀파일에 저장
        # workbook = xlrd.open_workbook('/stock_info/종목코드.xlsx')
        workbook = xlrd.open_workbook('종목코드.xlsx')
        worksheet = workbook.sheet_by_name(market)
        list = worksheet._cell_values

        cnt = len(list)
        # cnt = 11                              # 테스트용
        for i in range(1, cnt):     # list의 '0'번째는 columns 이므로 제외하여야 함.
            try:
                time.sleep(3.6)      # 키움증권에서 과다조회로 차단방지.
                code = list[i][0]
                self.kiwoom.call_basic_info(code)
                print(f"{i}/{cnt} 번째 데이터 저장중.")
                if i == cnt-1 :
                    self.save_excel(market, i)
            except:                          # 혹시 프로세서가 중단될 경우에 데어터 저장.
                print(f'{i}번데어터 처리 중 에러발생으로 데이터를 엑셀에 저장함.')
                self.save_excel(market, i)

    def save_excel(self,market, i):
        '''
        이 함수는 자료를 dataframe으로 저장하디가 100개가 되면 엑셀파일에 저장하는 방식임. 중간에 시스템이 다운되면 곤란하기 때문에..
        엑셀에 1행씩 바로바로 저장할 수도 있으나 그렇게 하려면 kiwoom파일의 모듈부터 수정하여야 함.
        즉, 키움파일의 tr_date_handler()에서 자료를 얻어올때 전역변수 리스트로 저장하고 그 리스트를 위 for문에서 엑셀에
        바로 저장해야함.
        그리고, 이렇게 저장하면 나중에 엑셀파일의 16개시트 증 마지막 시트 외에는 전부 삭제해야 함.
        차라리 덮어쓰기 하면 안될까.
        :param market: 'kospi'  또는 'kosdaq'
        :param i: 작업진행과정을 알수 있도록 'i'번째 작업임을 표시.
        :return:
        '''

        file_name = "주식기본정보.xlsx"

        # with ExcelWriter(file_name, mode='w', engine='openpyxl') as writer:   # 여기서 인자로 sheet_name까지 전달할 수는 없다.
        #     self.kiwoom.df_stock_info.to_excel(writer, sheet_name=market)  #market = 'kospi' or 'kosdaq'
        #     print(f"{i}번째까지의 자료를 엑셀파일에 저장중...")

        if not os.path.exists(file_name):
            with ExcelWriter(file_name, mode='w', engine='openpyxl') as writer:
                self.kiwoom.df_stock_info.to_excel(writer, sheet_name=market)  #market = 'kospi' or 'kosdaq'
            print(f'{i}번째까지의 자료를 엑셀파일에 저장중...')

        else:
            with ExcelWriter(file_name, mode='a', engine='openpyxl') as writer:
                self.kiwoom.df_stock_info.to_excel(writer, sheet_name=market)
            print(f'{i}번째까지의 자료를 엑셀파일에 저장중...')

        self.kiwoom.df_stock_info_exist = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Basic_info()
    # app.exec_()
