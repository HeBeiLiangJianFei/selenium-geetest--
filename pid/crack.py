import random
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = '1436678918@qq.com'
PASSWORD = '1596357ljf'
BORDER = 6
INIT_LEFT = 60


#  PID控制一阶惯性系统测试程序

# *****************************************************************#
#                      增量式PID系统                              #
# *****************************************************************#
class IncrementalPID:
    def __init__(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.PIDOutput = 0.0  # PID控制器输出
        self.SystemOutput = 0.0  # 系统输出值
        self.LastSystemOutput = 0.0  # 上次系统输出值

        self.Error = 0.0  # 输出值与输入值的偏差
        self.LastError = 0.0
        self.LastLastError = 0.0

    # 设置PID控制器参数
    def SetStepSignal(self, StepSignal):
        self.Error = StepSignal - self.SystemOutput
        IncrementValue = self.Kp * (self.Error - self.LastError) + self.Ki * self.Error + self.Kd * (
                    self.Error - 2 * self.LastError + self.LastLastError)
        self.PIDOutput += IncrementValue
        self.LastLastError = self.LastError
        self.LastError = self.Error

    # 设置一阶惯性环节系统  其中InertiaTime为惯性时间常数
    def SetInertiaTime(self, InertiaTime, SampleTime):
        self.SystemOutput = (InertiaTime * self.LastSystemOutput + SampleTime * self.PIDOutput) / (
                    SampleTime + InertiaTime)
        self.LastSystemOutput = self.SystemOutput


# *****************************************************************#
#                      位置式PID系统                              #
# *****************************************************************#
class PositionalPID:
    def __init__(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.SystemOutput = 0.0
        self.ResultValueBack = 0.0
        self.PidOutput = 0.0
        self.PIDErrADD = 0.0
        self.ErrBack = 0.0

    def SetInertiaTime(self, InertiaTime, SampleTime):
        self.SystemOutput = (InertiaTime * self.ResultValueBack + SampleTime * self.PidOutput) / (
                    SampleTime + InertiaTime)
        self.ResultValueBack = self.SystemOutput

    def SetStepSignal(self, StepSignal):
        Err = StepSignal - self.SystemOutput
        KpWork = self.Kp * Err
        KiWork = self.Ki * self.PIDErrADD
        KdWork = self.Kd * (Err - self.ErrBack)
        self.PidOutput = KpWork + KiWork + KdWork
        # print(Err)
        self.PIDErrADD += Err
        self.ErrBack = Err





import matplotlib.pyplot as plt

plt.figure(1)  # 创建图表1
plt.figure(2)  # 创建图表2


# 测试PID程序
def TestPID(P, I, D, li):
    PositionalPid = PositionalPID(P, I, D)
    PositionalXaxis = [0]
    PositionalYaxis = [0]

    for i in range(1, 100):
        # 位置式
        PositionalPid.SetStepSignal(li)
        PositionalPid.SetInertiaTime(3, 0.1)
        PositionalYaxis.append(PositionalPid.SystemOutput)
        PositionalXaxis.append(i)
    l = []
    for i in range(len(PositionalYaxis) - 1):
        l.append(round(PositionalYaxis[i + 1] - PositionalYaxis[i]))
    return l


    # plt.figure(1)  # 选择图表1
    # plt.plot(IncrementalXaxis, IncrementalYaxis, 'r')
    # plt.xlim(0, 120)
    # plt.ylim(0, 140)
    # plt.title("IncrementalPID")
    #
    # plt.show()


# if __name__ == "__main__":
#     TestPID(2.5, 0.5, 0.1)






class CrackGeetest():
    def __init__(self):
        self.url = 'https://account.geetest.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 6)
        self.email = EMAIL
        self.password = PASSWORD
    
    # def __del__(self):
    #     self.browser.quit()
    
    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return:
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button
    
    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)
    
    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot
    
    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider
    
    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        # captcha = screenshot.crop((left*100/80, top*100/80, right*100/80, bottom*100/80))
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha
    
    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        email.send_keys(self.email)
        password.send_keys(self.password)
    
    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left
    
    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        此处是最基础的模拟移动  不能够更好的模拟人类
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def get_pid_track(self, distance):
        '''
        此处是 利用工业中常用的PID 比例积分微分调节，返回每次移动的步长；模拟人类的往返运行
        '''
        lis = TestPID(4.5, 0.5, 0.1, distance)
        return lis

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()
    
    def login(self):
        """
        登录
        :return: None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
        submit.click()
        print('登录成功')
        time.sleep(10)
        self.browser.quit()

    def crack(self):
        # 输入用户名密码
        self.open()
        # 点击验证按钮
        button = self.get_geetest_button()
        button.click()
        time.sleep(2)
        """
        执行js代码 将原图显示
        """
        js = "document.getElementsByTagName('canvas')[2].style.cssText='display:block;opacity:10'"
        self.browser.execute_script(js)
        time.sleep(0.5)
        # 获取验证码图片
        image1 = self.get_geetest_image('captcha1.png')

        # 点按呼出缺口
        slider = self.get_slider()
        slider.click()
        # 获取带缺口的验证码图片
        image2 = self.get_geetest_image('captcha2.png')
        # 获取缺口位置
        gap = self.get_gap(image1, image2)
        print('缺口位置', gap)
        # 减去缺口位移
        gap -= BORDER
        # 获取移动轨迹
        # self.start_move(gap)
        # track = self.get_track(gap)
        track = self.get_pid_track(gap)
        print('滑动轨迹', track)
        # # 拖动滑块
        self.move_to_gap(slider, track)
        try:
            success = self.wait.until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
            print(success)

            # 失败后重试
            if not success:
                self.crack()
            else:
                self.login()
        except Exception as e:
            print(e)
            self.crack()


if __name__ == '__main__':
    crack = CrackGeetest()
    crack.crack()
