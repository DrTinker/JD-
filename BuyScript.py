from selenium import webdriver
import tkinter as tk
import threading
import os
import config
import datetime
import time

username = config.username
password = config.password


# 日志信息
log = ''
is_change = False


def login_by_name(driver, delay):
    global log
    global is_change
    driver.get("https://passport.jd.com/new/login.aspx")
    time.sleep(1)
    while True:
        try:
            driver.find_element_by_link_text("账户登录").click()
            driver.find_element_by_name("loginname").send_keys(username)
            driver.find_element_by_name("nloginpwd").send_keys(password)
            driver.find_element_by_id("loginsubmit").click()
            log = '你有60s的时间登录\n'
            is_change = True
            time.sleep(delay)
        except Exception: # 两种可能：1.网页还没加载出来 2.网页成功跳转
            title = driver.title
            # print(title)
            if title == 'JD.com, Inc.' or title == '京东(JD.COM)-正品低价、品质保障、配送及时、轻松购物！':
                break
            else:
                continue


def login_by_qr(driver, delay):
    global log
    global is_change
    driver.get("https://passport.jd.com/new/login.aspx")
    time.sleep(1)
    while True:
        try:
            driver.find_element_by_link_text("扫码登录").click()
            log = '你有60s的时间扫码登录\n'
            is_change = True
            time.sleep(delay)
        except Exception: # 两种可能：1.网页还没加载出来 2.网页成功跳转
            title = driver.title
            # print(title)
            if title == 'JD.com, Inc.' or title == '京东(JD.COM)-正品低价、品质保障、配送及时、轻松购物！':
                break
            else:
                continue


def add_good(driver, eid, buytime):
    global log
    global is_change
    url = 'https://item.jd.com/' + eid + '.html'
    driver.get(url)
    # time.sleep(0.5)
    while True:
        now = datetime.datetime.now()
        if now.strftime('%Y-%m-%d %H:%M:%S') >= buytime:
            try:
                driver.find_element_by_id('InitCartUrl').click()
                log = (now.strftime('%Y-%m-%d %H:%M:%S')+'\n')
                log += '点击加入购物车一次\n'
                is_change = True
                time.sleep(0.1)
            except Exception:
                title = driver.title
                # print('1: ' + title)
                if title == '商品已成功加入购物车':
                    break
                else:
                    continue


def buy_reservation(driver, eid, buytime):
    global log
    global is_change
    while True:
        now = datetime.datetime.now()
        if now.strftime('%Y-%m-%d %H:%M:%S') >= buytime:
            try:
                print('开始')
                url = 'https://item.jd.com/' + eid + '.html'
                driver.get(url)
                time.sleep(0.5)
                driver.find_element_by_link_text('立即抢购').click()
                log = (now.strftime('%Y-%m-%d %H:%M:%S')+'\n')
                log += '点击立即抢购一次\n'
                is_change = True
                time.sleep(0.1)
            except Exception:
                title = driver.title
                if title == '商品已成功加入购物车':
                    log += '抢购成功\n'
                    is_change = True
                    break
                else:
                    print('网页没完成加载')
                    continue


def open_cart(driver):
    global log
    global is_change
    driver.get("https://cart.jd.com/cart.action")
    while True:
        try:
            driver.find_element_by_link_text("去结算").click()
            nowtime = datetime.datetime.now()
            log = (nowtime.strftime('%Y-%m-%d %H:%M:%S')+'\n')
            log += '点击去结算一次\n'
            is_change = True
            time.sleep(0.1)
        except Exception:
            title = driver.title
            # print('2: ' + title)
            if title == '订单结算页 -京东商城':
                break
            else:
                continue


def buy_on_time(driver):
    global log
    global is_change
    # print('正在提交订单')
    while True:
        now = datetime.datetime.now()
        try:
            driver.find_element_by_id('order-submit').click()
            log = (now.strftime('%Y-%m-%d %H:%M:%S')+'\n')
            log += '点击提交订单一次，如成功跳转支付界面，请在规定时间内支付，不然没了\n'
            is_change = True
            time.sleep(0.1)
        except Exception:
            title = driver.title
            # print('3: ' +  title)
            if title == '收银台':
                break
            else:
                continue


def work(eid, buytime, delay, is_qr, is_qg):
    # 启动浏览器
    driver = webdriver.Firefox(executable_path='./geckodriver/geckodriver.exe')
    if is_qr.get() == 1:
        login_by_qr(driver, delay)
    elif is_qr.get() == 0:
        login_by_name(driver, delay)
    else:
        print('CheckBox Error!')

    if is_qg.get() == 1:
        buy_reservation(driver, eid, buytime)
    elif is_qg.get() == 0:
        add_good(driver, eid, buytime)
    else:
        print('CheckBox Error!')

    # print('首页:' + driver.title)
    # print('去查看购物车:' + driver.title)
    open_cart(driver)
    # print('提交订单:' + driver.title)
    buy_on_time(driver)


def check(txt):
    global log
    global is_change
    while True:
        if is_change:
            txt.insert('end', log)
            is_change = False


def shut_down():
    os._exit(0)


def main_for_gui(eid, buytime, delay, is_qr, is_qg):
    t1 = threading.Thread(target=work, args=(eid, buytime, delay, is_qr, is_qg,))
    t1.start()
    # 初始化窗口
    root = tk.Tk()
    # 设置标题
    root.title('抢购脚本')
    # 窗口大小
    root.geometry('500x300')
    tk.Label(root, text='实时监测', font=('Arial', 16)).pack()
    t = tk.Text(width=400, height=250)
    t.pack()
    t2 = threading.Thread(target=check, args=(t,))
    t2.start()
    tk.Button(root, text='终止脚本', command=shut_down).place(x=250, y=260)
    root.mainloop()
