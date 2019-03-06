from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
driver = webdriver.Chrome()
driver.implicitly_wait(20)
driver.maximize_window()
driver.get('https://www.cnblogs.com/')
#给元素加上红色边框,0.3秒后还原
def highlightElement(element):
    driver.execute_script("arguments[0].setAttribute('style',arguments[1]);",element,
                          "border:2px solid red;")
    time.sleep(0.3)
    driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", element,
                          "")

program_lan = driver.find_element_by_xpath('//li[@id="cate_item_2"]/a')
program_py = driver.find_element_by_xpath('//li/a[@href="/cate/python/"]')

highlightElement(program_lan)
#鼠标先移动到“编程语言”上，然后点击Python
ActionChains(driver).move_to_element(program_lan).click(program_py).perform()

driver.quit()