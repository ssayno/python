#!/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import random
import time
import requests
import cv2 as cv
import re
import os
import getpass


class Zhihu():

    def __init__(self):
        self.chrome_options = Options()
        # 转到测试端口
        self.chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # 确定 chromedrive 位置
        self.chromedriver = Service("/home/sayno/chromedriver")
        self.br = webdriver.Chrome(service=self.chromedriver, options=self.chrome_options)
        # 设置等待时间
        self.wait = WebDriverWait(self.br, 10)
        # 用来计数
        self.count = 1
        if not os.path.exists('passage'):
            os.mkdir('passage')

    def initProcess(self):
        self.br.get("https://www.zhihu.com/signin?next=%2F")
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/main/div/div/div/div[1]/div/div[1]/form/div[1]/div[2]')))
        button.click()
        input_name = input("输入帐号：")
        name = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/div/div/div[1]/div/div[1]/form/div[2]/div/label/input')))
        name.click()
        name.clear()
        for item in input_name:
            time.sleep(random.uniform(0.05, 0.1))
            name.send_keys(item)
        # 输入自己的密码
        input_passwd = getpass.getpass("输入密码：")
        passwd = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/div/div/div[1]/div/div[1]/form/div[3]/div/label/input')))
        passwd.click()
        passwd.clear()
        for item in input_passwd:
            time.sleep(random.uniform(0.05, 0.1))
            passwd.send_keys(item)
        login = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/main/div/div/div/div[1]/div/div[1]/form/button')))
        login.click()
        time.sleep(2)
        images = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img')))
        inames = []
        for image in images:
            url = image.get_attribute('src')
            iname = re.split('/', url)[-1]
            inames.append(iname)
            with open(iname, 'wb') as f:
                f.write(requests.get(url).content)
        distance = self.get_distance(inames[0], inames[1])
        tracks = self.get_tracks(distance)
        self.moveButton(tracks)
        # 这里而是判断是否成功，写不下去了
        # element = self.br.find_element(By.ID, 'Popover15-toggle')
        # need = self.wait.until(EC.staleness_of(element))
        # print(need)
        # while not need:
        #     need = self.wait.until(EC.staleness_of(element))
        #     print(need)
        #     self.moveButton(tracks)
        time.sleep(3)
        # 寻找搜索框
        search = self.wait.until(EC.element_to_be_clickable((By.ID, 'Popover1-toggle')))
        search.click()
        search.clear()
        search.send_keys('汉江大学')
        # 搜索按钮
        enter = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div[2]/header/div[2]/div[1]/div/form/div/div/label/button')))
        enter.click()
        # 寻找当前文章链接
        # 注意的事： 每次 back 都会重新刷新 url, 所以需要 self.count 来计数，可以添加 js 语句来进行滚动查找，可惜，我有点忘了
        hrefs = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//*[@id="SearchMain"]/div/div/div/div/div/div/div/h2/div/a')))
        for i in range(len(hrefs)):
            try:
                self.getMessage(hrefs[self.count].get_attribute("href"))
                self.count += 1
                hrefs = self.wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[@id="SearchMain"]/div/div/div/div/div/div/div/h2/div/a')))
            except IndexError as e:
                print("没有添加模拟滚动，所以超出索引")

    def moveButton(self, tracks):
        btn = self.br.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div/div[2]/div[2]')
        move = ActionChains(self.br)
        move.click_and_hold(btn)
        for track in tracks:
            move.move_by_offset(track, 0)
        move.release()
        move.perform()

    def get_distance(self, bg_img_path, slider_img_path):
        """获取滑块移动距离"""
        # 背景图片处理
        print("")
        bg_img = cv.imread(bg_img_path, 0)  # 读入灰度图片
        bg_img = cv.GaussianBlur(bg_img, (3, 3), 0)  # 高斯模糊去噪
        bg_img = cv.Canny(bg_img, 50, 150)  # Canny算法进行边缘检测
        # 滑块做同样处理
        slider_img = cv.imread(slider_img_path, 0)
        slider_img = cv.GaussianBlur(slider_img, (3, 3), 0)
        slider_img = cv.Canny(slider_img, 50, 150)
        # 寻找最佳匹配
        res = cv.matchTemplate(bg_img, slider_img, cv.TM_CCOEFF_NORMED)
        # 最小值，最大值，并得到最小值, 最大值的索引
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        # 例如：(-0.05772797390818596, 0.30968162417411804, (0, 0), (196, 1))
        top_left = max_loc[0]  # 横坐标
        return top_left

    def get_tracks(self, distance):
        '''滑动轨迹 '''
        tracks = []
        v = 30
        t = 0.5 # 单位时间
        current = 0  # 滑块当前位移
        distance += 10  # 多移动10px,然后回退
        while current < distance:
            if current < distance * 5 / 8:
                a = random.randint(1, 2)
            else:
                a = -random.randint(1, 2)
            v0 = v  # 初速度
            track = v0 * t + 0.5 * a * (t ** 2)  # 单位时间（0.2s）的滑动距离
            tracks.append(round(track))  # 加入轨迹
            current += round(track)
            v = v0 + a * t
                #回退到大致位置
        for i in range(5):
            tracks.append(-random.randint(1, 3))
            return tracks

    def getMessage(self, url):
        try:
            self.br.get(url)
            title = self.br.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div[1]/div[2]/div/div[1]/div[1]/h1').text
            content = self.br.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/span').text
            with open(f'./passage/{title}.txt', 'w') as f:
                print(f'./passage/{title}.txt'+"正在创建")
                f.write(content)
        except Exception as e:
            print("This is erros")
        finally:
            self.br.back()


if __name__ == '__main__':
    zhihu = Zhihu()
    zhihu.initProcess()