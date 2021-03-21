from selenium import webdriver
from selenium.webdriver.common.keys import Keys

i=0
j=0

x_len=0
y_len=0

isdone = False
while not isdone:
    driver = webdriver.Chrome('/home/user/바탕화면/capstone/crawler/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        # "download.default_directory": r"/foscar ~~",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver.get('https://aihub.or.kr/user/login?destination=/node/1')
    driver.implicitly_wait(3)
    driver.find_element_by_name('name').send_keys('plmoknijb3123@gmail.com')
    driver.find_element_by_name('pass').send_keys('!qazwsx123')
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
    data_list[i][j].click()
    if j == len(data_list[i])-1:
        if i== len(data_list):
            break
        i+=1
        j=0
        continue

    j+=1

    driver.close()

