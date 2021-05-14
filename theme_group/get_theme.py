from user.kiwoom import *

app = QApplication(sys.argv)
kiwoom = Kiwoom()
theme_group = kiwoom.dynamicCall("GetThemeGroupList(Int)", 0)
theme_group_lists = theme_group.split(';')
print("테마그룹: ", theme_group_lists)

theme_dic = {}
for group_list in theme_group_lists:
    # print(group_list)
    group_code, group_name = group_list.split("|")
    print(group_code, group_name)
    jongmok_code = kiwoom.dynamicCall("GetThemeGroupCode(QString)", group_code) # 1개 테마그룹의 종목코드리스트
    theme_dic[group_code] = jongmok_code
    print(theme_dic)
app.exec_()

