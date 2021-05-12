from selenium import webdriver
import time

exit_value = False

driver = webdriver.Chrome('chromedriver.exe')
driver.get("http://dart.fss.or.kr/dsab007/main.do")
time.sleep(3)

# 종목코드 입력
company = driver.find_element_by_xpath('//*[@id="textCrpNm"]')
company.send_keys("000660")
driver.find_element_by_xpath('//*[@id="detailSearch"]/p[1]/input').click()
time.sleep(3)
# 검색창에서 선택키
driver.find_element_by_xpath('//*[@id="allCheck"]').click()
# 확인 클릭
driver.find_element_by_xpath('//*[@id="corpListContents"]/div/fieldset/div[3]/a[1]/img').click()

# 통합검색창에서 첫번째 항목인 key word("미상환 전환사채") 입력
element = driver.find_element_by_xpath('//*[@id="keyword"]')
element.send_keys("전환사채 등 발행현황")
driver.find_element_by_xpath('//*[@id="keywordBtn"]').click()
time.sleep(2)



#


# # 검색창 초기화
# length = len(element.get_attribute('value'))
# element.send_keys(length * Keys.BACKSPACE)
#
# # 검색 기업 입력
# element.send_keys("삼성전자")






# 로그인타임 기다리자
# input("준비가 되면 아무키나 누르세요")
