'''
코스피 종목 및 코스닥 종목 전체를 얻어와서 종목명을 찾아서 '종목코드', '종목명' 칼럼으로 엑셀파일에 저장
이 엑셀파일의 종목코드시트는 앞으로 만들어 나갈 모든 자료의 [인덱스키]로만 사용하고 다른 데이터는 포함하지 않는다.
'''
from Get_Code.kiwoom import *
from pandas import *

class Main:
    def __init__(self):
        kiwoom = Kiwoom()

        file_name = "종목코드.xlsx"   # 종목코드를 저장할 엑셀파일명을 저장하는 변수

        # 코스포 종목 얻어오기
        kospi = kiwoom.dynamicCall("GetCodeListByMarket(QString)", "0")
        print('kospi: ', kospi)
        codes = kospi.split(';')

        list_code = []
        for code in codes:
            data = []
            code_name = kiwoom.dynamicCall("GetMasterCodeName(QString)", code)
            data=[code, code_name]
            list_code.append(data)

        print('jongmok: ', list_code)

        # print('jongmok: ', jongmok)
        print('종목수: ', len(list_code))

        df_code = DataFrame(list_code, columns= ['종목코드', '종목명'])
        print(df_code)

        if not os.path.exists(file_name):
            with ExcelWriter(file_name, mode= 'w', engine= 'openpyxl') as writer:
                df_code.to_excel(writer, sheet_name='코스피종목', index=False)
        else:
            with ExcelWriter(file_name, mode= 'a', engine= 'openpyxl') as writer:
                df_code.to_excel(writer, sheet_name='코스피종목', index=False)


        #코스닥 종목 얻어오기
        kosdaq = kiwoom.dynamicCall("GetCodeListByMarket(QString)", "10")
        print('kosdaq: ', kosdaq)
        codes = kosdaq.split(';')

        list_code = []
        for code in codes:
            data = []
            code_name = kiwoom.dynamicCall("GetMasterCodeName(QString)", code)
            data=[code, code_name]
            list_code.append(data)

        print('jongmok: ', list_code)

        # print('jongmok: ', jongmok)
        print('종목수: ', len(list_code))

        df_code = DataFrame(list_code, columns= ['종목코드', '종목명'])
        print(df_code)

        if not os.path.exists(file_name):
            with ExcelWriter(file_name, mode= 'w', engine= 'openpyxl') as writer:
                df_code.to_excel(writer, sheet_name='코스닥종목', index=False)
        else:
            with ExcelWriter(file_name, mode= 'a', engine= 'openpyxl') as writer:
                df_code.to_excel(writer, sheet_name='코스닥종목', index=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main()
    # sys.exit(app.exec_())
