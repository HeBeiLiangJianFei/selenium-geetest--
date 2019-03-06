import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


url = "https://auth.geetest.com/login/"
options =webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# options.add_argument('--proxy-server=127.0.0.1:8080')
cookie = 'Hm_lvt_25b04a5e7a64668b9b88e2711fb5f0c4=1551665740; _ga=GA1.2.1812899874.1551665752; _gid=GA1.2.1189605574.1551665752; intercom-id-kqrnii8q=297147cc-61bb-4622-921f-d04d30134003; auth_email=1436678918@qq.com; session_id=899dea6bcbb4b2bf3cc31f6f9906d259; Hm_lpvt_25b04a5e7a64668b9b88e2711fb5f0c4=1551694399'
options.add_argument('Cookie='+cookie)
options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
options.add_argument('Host="auth.geetest.com"')
brower = webdriver.Chrome(chrome_options=options)
brower.set_window_size(1920, 1080)
brower.get(url)
try:
    email = brower.find_element_by_xpath('//input[@type="email"]')
    print("email===", email)
    time.sleep(3)
    email.send_keys('1436678918@qq.com')
    pwd = brower.find_element_by_xpath('//input[@type="password"]')
    print("pwd===", pwd)
    pwd.send_keys('1596357ljf')
    time.sleep(3)
    submit = brower.find_element_by_xpath('//*[@id="captchaIdLogin"]/div/div[2]/div[1]/div[3]')
    submit.click()





    time.sleep(2)
    brower.save_screenshot('img.png')
    cav1 = brower.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div/canvas[1]')
    location = cav1.location
    print(location)
    # 获取验证码的大小
    size = cav1.size
    print(size)
    # 构建需要截图的坐标
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),int(location['y'] + size['height']))
    i = Image.open('img.png')
    i = i.convert('RGB')
    # 再次从整个界面的途中截取验证码的部分图纸
    frame1 = i.crop(rangle)
    frame1.save('new.png')
    brower.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[2]').click()
    time.sleep(4)
    brower.get_screenshot_as_file("img2.png")



    cav2 = brower.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div/canvas[2]')
    location = cav2.location
    print(location)
    size = cav2.size
    print(size)
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
              int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    i = Image.open("img2.png")  # 打开截图
    i = i.convert('RGB')
    i.save('img_new.png')
    frame2 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame2.save('new2.png')

    # time.sleep(600)
    def is_similar(image1, image2, x, y):
        pass
        # 获取指定位置的RGB值
        pixel1 = image1.getpixel((x, y))
        pixel2 = image2.getpixel((x, y))
        for i in range(0, 3):
            # 如果相差超过50则就认为找到了缺口的位置
            if abs(pixel1[i] - pixel2[i]) >= 50:
                return False
        return True

    # 计算缺口的位置
    def get_diff_location(image1, image2):
        i = 0
        # 两张原始图的大小都是相同的260*116
        # 那就通过两个for循环依次对比每个像素点的RGB值
        # 如果相差超过50则就认为找到了缺口的位置
        for i in range(62, 258):  # 有人可能看不懂这个位置为什么要从62开始看最后一张图（图：3）
            for j in range(0, 159):
                if is_similar(image1, image2, i, j) == False:
                    return i

    def is_similar_color( x_pixel, y_pixel):
        for i, pixel in enumerate(x_pixel):
            if abs(y_pixel[i] - pixel) > 50:
                return False
        return True

    def get_offset_distance(cut_image, full_image):
        for x in range(cut_image.width):
            for y in range(cut_image.height):
                cpx = cut_image.getpixel((x, y))
                fpx = full_image.getpixel((x, y))
                if not is_similar_color(cpx, fpx):
                    img = cut_image.crop((x, y, x + 50, y + 40))
                    # 保存一下计算出来位置图片，看看是不是缺口部分
                    img.save("1.jpg")
                    return x


    # loc = get_diff_location(frame1, frame2)
    loc = get_offset_distance(frame1,frame2)
    print("=====================================")
    print(loc)


    #找到滑动的圆球
    element=brower.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[2]')
    location=element.location
    #获得滑动圆球的高度
    y=location["y"]
    #鼠标点击元素并按住不放
    print ("第一步,点击元素")
    ActionChains(brower).click_and_hold(on_element=element).perform()
    time.sleep(2)

    print ("第二步，拖动元素")
    ActionChains(brower).move_to_element_with_offset(to_element=element, xoffset=loc + 30, yoffset=y - 445).perform()
    # time.sleep(600)
    #释放鼠标
    ActionChains(brower).release(on_element=element).perform()
    time.sleep(5)
    button = brower.find_element_by_xpath('//*[@id="base"]/div[2]/div/div/div[3]/div/form/div[5]/div/button')
    button.click()
    time.sleep(3)
    brower.save_screenshot('end.png')
    brower.quit()
except Exception as e:
    print("出错", e)
finally:
    brower.quit()






