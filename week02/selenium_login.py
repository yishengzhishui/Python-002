from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    # 打开石墨
    browser.get("https://shimo.im/login?from=home")
    time.sleep(1)

    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input') \
        .send_keys('xxxxx')
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input') \
        .send_keys('xxxxx')

    btn_login = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button')
    btn_login.click()

    time.sleep(2)

except Exception as e:
    print(e)
finally:
    browser.close()
