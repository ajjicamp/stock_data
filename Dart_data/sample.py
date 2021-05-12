from selenium import webdriver
import re
import time
import random
from pandas import *
import os

exit_value = False

def get_content(driver, i, last_picture):
    '''
    :param driver: slenium의 webdriver browser
    :param i: 일련번호 1 ~ 사용자가 지정하는 마지막사진까지
    :param last_picture: 사용자가 지정하는 마지막 사진의 날짜시간요소. 이게 개체의 정체성을 나타내는 유일한지표.
    :return:
    '''
    # 인텍스 번호  => 엑셀파일에 저장하여 인데스로 사용하고, 사진파일이름을 만들때도 붙여쓴다.
    index_num = str(i)
    index_num = index_num.rjust(4, '0')

    # 게시자 id
    owner = driver.find_elements_by_css_selector(".sqdOP.yWX7d._8A5w5.ZIAjV")[0].text
    print('owner', owner)

    # 날짜시간
    s_date = driver.find_elements_by_css_selector('time._1o9PC.Nzb55')[0]
    date = s_date.get_attribute('datetime')

    # date == '2021-04-24T01:49:02.000Z':           이러한 형식
    if date == last_picture:
        global exit_value
        exit_value= True
    print('시간: ', date)

    # 첫 게시글 => 태그를 확인하기 위하여 얻어옴. db에 저장하지는 않음.
    content =  driver.find_elements_by_css_selector('div.C4VMK > span')[0].text
    print('content:', content)

    # 해시태그
    tags = re.findall(r'#[^\#,\\]+', content)  # content 안에서 해시태그 찾는 로직. 즉, #로 시작해서
    print('tags:', tags)

    # 사진 : position사진을 screenshot하여 png파일로 생성보관한다.
    # 포스트용 표지사진을 가져온다.
    picture =  driver.find_elements_by_css_selector('.ZyFrc')
    # .ZyFrc요소는 클릭한 focusable 포스트로써 인데스[0]이 사진 인데스[1]부터 게시글이 순서대로 저장되어 있다.
    picture_path = 'C:\\Users\\SAMSUNG\\PycharmProjects\\instagram\\img(30회사생)/'  # 현재작업중인 폴드내에 디렉토리 미리생성
    picture_file = owner + "!" + index_num + '.png'  # 파일명은 게시자id + 인덱스번호(4자리) + 이미지확장자

    picture.screenshot(picture_path + picture_file)
    print("사진파일명: ", picture_file)


    # 아래와 같이 코딩하면 data값을 0으로 주었을때 list.append는 괜찮으나 DataFrame만들때는 에러가 난다.
    # if ('#경남은행' in tags) or ('#bnk경남은행' in tags):
    #     data = None
    # else:
    #     data = [index_num, owner, date, tags, picture_file]

    return  data

def move_next(driver):
    right = driver.find_element_by_css_selector('a.coreSpriteRightPaginationArrow')
    right.click()
    time.sleep(random.uniform(5,7))          

def save_data():
    df_results = DataFrame(results)
    df_results.columns = ['일련번호', '게시자ID', '날짜시간', '해시태그', '사진파일명']

    file_name = "사생실기대회(30회사생).xlsx"
    if not os.path.exists(file_name):
        with ExcelWriter(file_name, mode='w', engine='openpyxl') as writer:
            df_results.to_excel(writer, sheet_name="sheet1", index=False)
    else:
        with ExcelWriter(file_name, mode='a', engine='openpyxl') as writer:
            df_results.to_excel(writer, sheet_name="sheet1", index=False)


driver = webdriver.Chrome('chromedriver.exe')
driver.get("http://dart.fss.or.kr")
time.sleep(3)

# 로그인타임 기다리자
# input("준비가 되면 아무키나 누르세요")

results = []
i = 0
while not exit_value:
# for i in range(start_num, last_num):
    try:
        data = get_content(driver, i, last_picture)
        # index_num = i
        # data.insert(0,index_num)
        results.append(data)
        print(f"{i}번 data 저장완료")
        move_next(driver)
        i += 1
    except:
        print(f"{i+1}번 data저장 실패")
        # move_next가 실패하면 끝났다는 얘기이므로 저장함.
        save_data()
        # 저장실패인덱스 번호를 텍스트파일에 저장
        # f = open('log.txt', mode='wt', encoding='utf-8')
        # f.write(f"{i}번 데이터 저장 오류")
        # 우측자료로 이동
        time.sleep(2)
        # move_next(driver)
    if i % 100 == 0 :
        save_data()
        results = []

save_data()
# driver.close()

## 사진url 얻어오기 관련(현재가창의 클리한 사진 얻어오는 방법)
# picture_source = driver.find_elements_by_css_selector('.ZyFrc')[0]  #여기서 css_selector('.KL4Bh')하면 클릭한 창이 나오지 앟는다.
# picture_class = picture_source.find_element_by_class_name('FFVAD') # 여기서는 by_class_name은 '.'으로 시작하지 않는다.
# imgurl = picture_class.get_attribute('src')

'''
# url을 이용하여 사진을 파일로 저장하는 방법
with urlopen(imgurl) as f:
    # with open('C:\\Users\\SAMSUNG\\PycharmProjects\\instagram\\img/' + plusurl + str(n) + '.jpg', 'wb') as h:
    with open('C:\\Users\\SAMSUNG\\PycharmProjects\\instagram\\img/' + owner + '.jpg', 'wb') as h:
        img = f.read()
        h.write(img)
        print("이미지파일 이름; ", h.name)
'''
