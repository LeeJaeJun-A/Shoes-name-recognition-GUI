from urllib.parse import quote_plus
from selenium import webdriver
import time
import os
import urllib.request

#name
Air_jordan = 'Air jordan 1 high og dior'
German = 'German Army Trainers'
Chuck = 'Chuck 70 Classic Black 162058C'

baseUrl = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query='
searchTerm  = input ('검색어 입력: ')
url = baseUrl + quote_plus(searchTerm)
folder_path = 'C:/Users/msi/Desktop/openCV project/' + 'khyunglee'

# 폴더 만들기
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

driver = webdriver.Chrome('C:/Users/msi/Desktop/openCV project/chromedriver_win32/chromedriver.exe')
driver.get(url)

# 스크롤 끝까지 내리기
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    time.sleep(0.5)

    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        break
    last_height = new_height

#이미지 url 찾기 밎 저장
imgs = driver.find_elements_by_css_selector("img._img")
img_list = []
for img in imgs:
    if 'http' in img.get_attribute('src'):
        img_list.append(img.get_attribute('src'))

for num , link in enumerate(img_list):
    start = link.rfind('.')
    end = link.rfind('&')
    filetype = link[start:end]
    urllib.request.urlretrieve(link, folder_path + '/'+ 'kyunglee' + ' ' + str(num+1)+ ".jpg")

print('완료')

driver.close
