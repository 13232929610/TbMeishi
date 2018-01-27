#! C:\Python36\python.exe
# coding:utf-8
import re
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from project.config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# browser = webdriver.Chrome()  # 打开谷歌浏览器
browser = webdriver.PhantomJS('phantomjs.exe',service_args=SERVICE_ARGS)  # 打开无界面浏览器
wait = WebDriverWait(browser, 10)  # 显式等待,等待10秒

browser.set_window_size(1400, 900)  # 设置窗口大小


# 搜索
def search():
    print("正在搜索...")
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))  # 等待直到查询按钮出现为止
        )
        # 复制搜索按钮的selector元素
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys(KEYWORD)  # 向搜索框中输入文本
        submit.click()  # 点击搜索
        # 直到页数出现,返回总页数的文本
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        return total.text
    except TimeoutException:
        return search()  # 失败则重新搜索


# 翻页
def nextPage(pageNum):
    print('正在翻页...', pageNum)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
            # 页码输入框
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))  # 确定按钮
        input.clear()  # 清除页码框中的内容
        input.send_keys(pageNum)  # 输入页码
        submit.click()  # 点击确定按钮
        # 直到页码序号被选中为止
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(pageNum)))
        getProducts()
    except TimeoutException:
        nextPage(pageNum)


# 获取商品信息
def getProducts():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source  # 页面源码
    doc = pq(html)  # 创建pyquery对象
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text(),
        }
        # print(product)
        saveToMongo(product)


# 存储到MongoDB数据库中
def saveToMongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功', result)
    except Exception:
        print('存储到MONDODB失败', result)


def main():
    try:
        total = search()
        # 正则匹配页数
        total = int(re.compile('(\d+)').search(total).group(1))
        # print(total)
        for i in range(2, total + 1):
            nextPage(i)
        browser.close()
    except Exception:
        print('出现错误......')
    finally:
        browser.close()


if __name__ == '__main__':
    main()
