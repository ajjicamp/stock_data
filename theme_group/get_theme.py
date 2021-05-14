from trkiwoom.kiwoom import *

app = QApplication(sys.argv)
kiwoom = Kiwoom()
theme_group = kiwoom.dynamicCall("GetThemeGroupList(Int)", 0)
theme_group_lists = theme_group.split(';')
print("테마그룹: ", theme_group)

for group_list in theme_group_lists:
    # print(group_list)
    group_code, group_name = group_list.split("|")
    # print(code, code_name)
    jongmok_code = kiwoom.dynamicCall("GetThemeGroupCode(QString)", group_code)
    print(group_name, jongmok_code)
    # code_list = codes.split(';')
    # print("code: ", code_list)

