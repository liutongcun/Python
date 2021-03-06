# -*- coding: utf-8 -*-
"""
爬虫代码示例.
主要模块：
    1. BeautifulSoup，Python的一个库，用于从网页抓取数据。
        安装：pip install beautifulsoup4
    2. requests:是一个Python第三方库，处理URL资源特别方便
        安装：pip install requests
    3. lxml：HTML解析器
        安装：pip install lxml

"""

import requests
from bs4 import BeautifulSoup #最主要的功能是从网页抓取数据
import pandas as pd
import os


#获取网页源代码
def get_html(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'  # 修改编码,apparent_coding是基于文本内容分析出的格式
        return r.text
    except:
        return print("产生异常")

#从网页源代码爬取文章标题、链接、详情以及图片
def get_data_excel(html,id,sheet_name):
    soup = BeautifulSoup(html, features='lxml')
    title_list, href_list, detail_list, img_list = [], [], [], []

    #获取标题以及链接
    text_div = soup.find_all('div', {'id': id})
    #print(text_div)
    for item in text_div:
        titles = item.find_all('text')
        hrefs = item.find_all('a')

        for title, href in zip(titles, hrefs):
            title_list.append(title.get_text())
            href_list.append(href['href'])
    print(title_list)
    print(href_list)

    #获取链接详情以及图片链接
    for href_url in href_list:
        detail_html = requests.get(href_url)
        detail_html.encoding = 'utf-8'
        detail_soup = BeautifulSoup(detail_html.text, features='lxml')
        #在活动表里的文章页面规则不一样，这里用try异常处理一下
        try:
            detail_ = detail_soup.find('div', {'id': 'news_content'})
            detail = detail_.find_all('p')
            detail_img = detail_.find_all('img')
            detail_list.append(detail)
            for img in detail_img:
                # print(img.get('src'))
                img_list.append(img.get('src'))
        except:
            detail_list.append('')
    # print(detail_list)
    # print(img_list)

    #根据爬取的图片链接列表将图片下载到本地保存
    for img_url in img_list:
        res = requests.get(img_url).content
        img_path = 'img/' + sheet_name + '/'
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        with open(img_path + img_url.split('/')[-1] + '.jpg', 'wb') as f:
            f.write(res)

    #将爬取的数据列表生成dataframe格式从而保存成excel格式数据
    # df = pd.DataFrame({'标题': title_list, '链接': href_list, '详情': detail_list})
    # print(sheet_name)
    # print(df)
    # if sheet_name == '全部':
    #     with pd.ExcelWriter('data.xlsx', mode='w') as writer:
    #         df.to_excel(writer, sheet_name=sheet_name)
    # else:
    #     with pd.ExcelWriter('data.xlsx', mode='a') as writer:
    #         df.to_excel(writer, sheet_name=sheet_name)

ids = ['art_list_sp_1', 'art_list_sp_2', 'art_list_sp_3', 'art_list_sp_4', 'art_list_sp_5', 'art_list_sp_6', 'art_list_sp_7', 'art_list_sp_8', 'art_list_sp_9']
sheet_names = ['全部', '财经', '分布式', '市场', '储能', '电站', '技术', '活动', '专题']
html = get_html('http://m.solarzoom.com/')

for id, sheet_name in zip(ids, sheet_names):
    get_data_excel(html, id, sheet_name)