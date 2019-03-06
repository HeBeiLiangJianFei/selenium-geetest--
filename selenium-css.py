#执行js语句
from selenium import webdriver
import time,os
driver=webdriver.Chrome()
driver.get('https://www.baidu.com/')
time.sleep(3)

root_dir='baidu'
if not os.path.exists(root_dir):
    os.mkdir(root_dir)
driver.save_screenshot('baidu/index1.png')

#1.通过js改变页面控件的属性（边框粗细，颜色，线的类型）

js='q=document.getElementById("kw");q.style.border="1px solid red";'
driver.execute_script(js)
driver.save_screenshot('baidu/index2.png')

#2.通过js隐藏元素
# 法一：img=driver.find_element_by_class_name("index-logo-src")`
#法二：xpath
# img=driver.find_element_by_xpath('//div[@id="lg"]/img')
# driver.execute_script("$(arguments[0]).fadeOut()",img)
# time.sleep(4)
# driver.save_screenshot('baidu/index3.png')