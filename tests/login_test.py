# -*- coding: utf-8 -*-
import time
from PIL import Image
import io  # 新增：用于处理字节流
import requests
from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup
import webview
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


class Crack_newsmth:
    def __init__(self):
        self.login_page_url = "https://m.newsmth.net/user/login"

        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser,20)
        button = self.get_shuimu_button()
        button.click()
        slider = self.get_slider()
        slider.click()
    def verify_login(self):
        # 1. 创建会话
        session = requests.Session()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "Referer": "https://m.newsmth.net/index",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
        }

        # 5. 准备登录数据
        data = {
            "id": "HLHCCC",  # 用户名
            "passwd": "Hlk6397Hlk@",  # 密码
        }

        print("正在执行登录...")
        response = session.post(self.login_page_url, headers=headers, data=data)
        print(f"登录响应状态码: {response.status_code}")
        print(f"登录响应URL: {response.url}")
    def get_shuimu_button(self):
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'shuimu_radar_tip')))
        return button
    def get_position(self):
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'shuimu_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom , left, right = location['y'],location['y']+size['height'],location['x'],location['x']+size['width']
        return (top,bottom,left,right)
    #获取验证码图片
    def get_shuimu_image(self,name='captcha.png'):
        top,bottom,left,right = self.get_position()
        print("验证码位置:",top,bottom,left,right)
        screenshot = self.get_screenshot()  #网页截图
        captcha = screenshot.crop((left,top,right,bottom))
        return captcha

    def get_screenshot(self):
        try:
            # 修正：使用self.browser（实例化的浏览器对象）而非self.driver
            screenshot_bytes = self.browser.get_screenshot_as_png()
            # 修正：使用PIL的Image处理图片
            screenshot = Image.open(io.BytesIO(screenshot_bytes))
            return screenshot
        except Exception as e:
            print(f"截取页面截图失败: {e}")
            raise  # 抛出异常便于调试

    def get_slider(self):
        # 修正：确保滑块元素定位正确
        return self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'shuimu_slider_button'))
        )

    def get_slider(self):
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'shuimu_slider_button')))
        return slider


if __name__ == "__main__":
    app = Crack_newsmth
