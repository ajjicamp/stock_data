from user.kiwoom import *




app = QApplication(sys.argv)
kiwoom = Kiwoom()
# 테마그룹명 리스트를 가져옴. '100|태양광_폴리실리콘'; '101|태양광_잉속/웨이펴/셀/모듈; '102|태양광_부품/소재/장비 ... 이런식
theme_group = kiwoom.dynamicCall("GetThemeGroupList(Int)", 0)

# 위 테마그룹명 리스트를 파이썬리스트로 변환하기 위하여 ';'를 기준으로 분할.
theme_group = theme_group.split(';')

# 1차 변환된 리스트의 개별 항목을 '|'를 기준으로 그룹코드와 그룹명으로 분할하여 딕셔너리{}로 저장

theme_group_list = []
for theme in theme_group:
    # data = []
    # print(group_list)
    data = theme.split("|")      # 그룹명 리스트를 종목코드와 종목명을 분할.
    theme_group_list.append(data)
# print(theme_group_list)  # {'100': '태양광_폴리실리콘', '101': '태양광_잉곳/웨이퍼/셀/모듈', '102': '태양광_부품/소재/장비',

cnt = len(theme_group_list)
for i in range(cnt):
    group_code = theme_group_list[i][0]
    group_name = theme_group_list[i][1]
    print(group_code, group_name)
    if group_code == '100':
        print(group_code, "찾기성공", group_name)
        input()

# 테마그룹별 종목코드를 검색하여 딕셔너리에 저장
theme_jongmok_dict = {}
for i in range(cnt):
    code = theme_group_list[i][0]
    data = kiwoom.dynamicCall("GetThemeGroupCode(QString)", code)
    # print(code,' ', data)
    theme_jongmok_list = data.split(';')
    theme_jongmok_dict[code] = theme_jongmok_list
print(theme_jongmok_dict)


# find_theme("000660")
#
#
# # 특정 종목이 어떤 테마에 속해 있는지와 같은 테마그룹종목들을 출력하는 함수
# def find_theme(code):
#     for i in range(cnt):
#         if code == theme_group_list[i][0]:
#             kiwoom.dynamicCall(())
#             print(theme_group_list[i][0])
#





# print(theme_dic)

app.exec_()

