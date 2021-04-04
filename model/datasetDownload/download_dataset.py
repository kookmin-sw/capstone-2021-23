from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import subprocess
import time
import os

i=25
j=0

x_len=0
y_len=0

isDone = False
while not isDone:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": r"/home/taehyeon/Desktop/dataset/download",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome('/home/taehyeon/Downloads/chromedriver', options=options)

    driver.get('https://aihub.or.kr/user/login?destination=/node/1')
    driver.implicitly_wait(3)
    driver.find_element_by_name('name').send_keys('YOUR ID')
    driver.find_element_by_name('pass').send_keys('YOUR PASSWORD')
    driver.implicitly_wait(3)
    driver.find_element_by_css_selector('input#edit-submit').click()
    driver.implicitly_wait(3)
    driver.find_element_by_css_selector('#gnb > nav > ul > li:nth-child(1) > a').click()
    driver.implicitly_wait(3)
    driver.find_element_by_css_selector('#block-stig-sub-system-main > div > section.AIHub-container.sub > div > div.content-left > nav > ul > li:nth-child(3) > a').click()
    driver.implicitly_wait(3)
    driver.find_element_by_css_selector('#block-stig-sub-system-main > div > section.AIHub-container.sub > div > div.content-left > nav > ul > li.more.on > ul > li:nth-child(2) > a').click()
    driver.implicitly_wait(3)
    driver.find_element_by_css_selector('#block-gavias-edupia-local-tasks > div > ul > li:nth-child(2) > a').send_keys(Keys.ENTER)#.click()
    driver.implicitly_wait(3)
    data_category = driver.find_elements_by_class_name('item-columns')

    data_list = [[dataset for dataset in category.find_elements_by_tag_name('a')] for category in data_category]

    driver.implicitly_wait(3)

    if i == 33:
        i = 41
        driver.close()
        continue
    if i == 57:
        i = 60
        driver.close()
        continue

    print("download start", i, j)
    print(data_list)
    data_list[i][j].click()

    #### 전처리 코드 시작 ####
    time.sleep(3)

    download_check = True
    file_info = subprocess.check_output('ls -l /home/taehyeon/Desktop/dataset/download/', shell=True).decode().split()
    prev_file_size = file_info[6]

    # 다운로드 체크
    while download_check:
        time.sleep(1)

        file_info = subprocess.check_output('ls -l /home/taehyeon/Desktop/dataset/download/', shell=True).decode().split()

        if file_info[6] == prev_file_size:
            download_check = False
        else:
            prev_file_size = file_info[6]


    print("download done", i, j)

    # original에 아무것도 없는지 체크
    downsize_check = True
    while downsize_check:
        time.sleep(1)
        dic_info = subprocess.check_output('ls -l /home/taehyeon/Desktop/dataset/original/', shell=True).decode().split()
        if dic_info[1] == '0':
            downsize_check = False

    # 1. download -> original
    # 2. download 지우기
    # 3. original에서 다운사이즈 작업
    os.system("mv /home/taehyeon/Desktop/dataset/download/* /home/taehyeon/Desktop/dataset/original")
    os.system("rm -rf /home/taehyeon/Desktop/dataset/download/*")
    os.system("bash downsize.sh&")

    #### 전처리 코드 끝 ####

    if i == len(data_list[0])-1:
        isDone = True

    i+=1

    driver.close()
