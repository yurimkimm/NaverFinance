import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome() # 크롬창열기
browser.maximize_window() # 창 최대화

# 1. 페이지 이동
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

# 2. 조회 항목 초기화
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected(): # 체크된 상태라면
        checkbox.click() # 클릭 (체크 해제)

# 3. 조회 항목 설정 (영업이익, per, poe, 매출액)
items_to_select = ['영업이익', 'PER', 'ROE', '매출액']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..')
    label = parent.find_element(By.TAG_NAME, 'label')
    # print(label.text) # 이름 확인
    if label.text in items_to_select:
        checkbox.click() # 체크

# 4. 적용하기 클릭
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()


for idx in range(1, 48): # 1 이상 47 미만
    # 사전 작업 : 페이지 이동
    browser.get(url + str(idx)) # http://naver.com...&page=2

    # 5. 데이터 추출
    df = pd.read_html(browser.page_source)[1]
    df.dropna(axis='index', how='all', inplace=True) # 모든 row가 결측치이면 지우기
    df.dropna(axis='columns', how='all', inplace=True) # 모든 colum이 결측치이면 지우기
    if len(df) == 0: # 더 이상 가져올 데이터가 없으면
        break

    # 6. 파일 저장
    f_name = 'sise.csv'
    if os.path.exists(f_name): # 파일 있다면? 헤더 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else: # 파일 없다면? 헤더 포함
        df.to_csv(f_name, encoding='utf-8-sig', index=False)

    print(f'{idx} 페이지 완료')

browser.quit() # 브라우저 종료