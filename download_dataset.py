from selenium import webdriver

driver = webdriver.Chrome('/home/user/바탕화면/capstone/crawler/chromedriver')
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
  #"download.default_directory": r"/foscar ~~",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
isdone = False
while not isdone:
    driver.get('https://aihub.or.kr/user/login?destination=/node/1')

    driver.find_element_by_name('name').send_keys('plmoknijb3123@gmail.com')
    driver.find_element_by_name('pass').send_keys('!qazwsx123')

    driver.find_element_by_css_selector('input#edit-submit').click()

    driver.find_element_by_css_selector('#gnb > nav > ul > li:nth-child(1) > a').click()
    driver.find_element_by_css_selector('#block-stig-sub-system-main > div > section.AIHub-container.sub > div > div.content-left > nav > ul > li:nth-child(3) > a').click()
    driver.find_element_by_css_selector('#block-stig-sub-system-main > div > section.AIHub-container.sub > div > div.content-left > nav > ul > li.more.on > ul > li:nth-child(2) > a').click()

    driver.find_element_by_css_selector('#block-gavias-edupia-local-tasks > div > ul > li:nth-child(2) > a').click()


    driver.find_element_by_css_selector('#container > article > div.js-view-dom-id-342be2055f276d8474ca310724c65b510826e3ce231631c0274258e91cfb4ba5 > div > div:nth-child(1) > div > span > div > div.js-view-dom-id-a3102fb516bd9970099a679a2230c37c36fbd8c6eed29974fd0b2146570c7d16 > div > div > div:nth-child(1) > div > div.views-field.views-field-views-conditional-field-1 > span > a').click()

    #driver.find_element_by_css_selector('').click()

    #driver.find_element_by_css_selector('#block-stig-sub-system-main > div > div > div > section.AIHub-container.sub > div > div.content-left > nav > ul > li.on.more > ul > li:nth-child(2) > a')

    #driver.find_element_by_css_selector('#block-gavias-edupia-local-tasks > div > ul > li:nth-child(2) > a')
