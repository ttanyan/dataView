#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#name   = lianjia
# code is far away from bugs with the god animal protecting
I love animals. They taste delicious.
┏┓      ┏┓
┏┛┻━━━┛┻┓
┃      ☃      ┃
┃  ┳┛  ┗┳  ┃
┃      ┻      ┃
┗━┓      ┏━┛
┃      ┗━━━┓
┃  神兽保佑    ┣┓
┃　永无BUG！   ┏┛
┗┓┓┏━┳┓┏┛
┃┫┫  ┃┫┫
┗┻┛  ┗┻┛
"""
import re
import urllib.request, urllib.error, urllib.parse
import time

import datetime
from bs4 import BeautifulSoup
from Demo.my_sqldb import insert_info, update_info, get_row, create_table

current_data = time.strftime('%Y-%m-%d', time.localtime(time.time()))
time.clock()


def get_house_href(total_page=2):
    """
    获取文本后面的链接网址
    :return:无
    """
    i = 1
    while i < total_page:
        url = 'http://cq.lianjia.com/ershoufang/binjiang/pg' + str(i) + '/'
        # 对url进行访问 page的数据格式为bytes类
        page = urllib.request.urlopen(url)
        # 将page解析成"html.parser"
        soup = BeautifulSoup(page, "html.parser")
        # 找到div和title元素的信息
        for title in soup.find_all('div', 'title'):
            print(type(title.a))
        i += 1


def get_house(location="binjiang", current_id=1):
    global location_chinese
    current_page = 1  # 当前在第几页
    total_page = 0  # 在这个区里一共有多少页房产信息
    url = 'http://cq.lianjia.com/ershoufang/' + location
    req = urllib.request.Request(url)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    if location == 'binjiang':
        location_chinese = '滨江'
    elif location == 'xihu':
        location_chinese = '西湖'
    elif location == 'xiacheng':
        location_chinese = '下城'
    elif location == 'jianggan':
        location_chinese = '江干'
    elif location == 'gongshu':
        location_chinese = '拱墅'
    elif location == 'shangcheng':
        location_chinese = '上城'
    elif location == 'yuhang':
        location_chinese = '余杭'
    elif location == 'xiaoshan':
        location_chinese = '萧山'
    else:
        print('wrong location')
    try:
        error = soup.title.text
        if error == "验证异常流量-链家网":
            print('ip被封 请尝试更换代理')
            return get_row()
        else:
            pass
    except:
        pass

    for link in soup.find_all('div', 'resultDes clear'):
        context = link.get_text()
        total_house = re.findall(r"\d+\.?\d*", context)[0]  # 总共有多少套房子
        print(location + '一共有' + total_house + '套房子')
        total_page = int(total_house) / 30 + 1  # 求出一共有多少页
        # total_page=2
    while current_page <= total_page:  # 遍历这个区域的所有房子的信息
        url = 'http://cq.lianjia.com/ershoufang/' + location + '/pg' + str(current_page) + '/'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        ID_num = current_id
        for price in soup.find_all('div', 'totalPrice'):  # 总价的信息
            insert_info("Id", ID_num)
            unit_price = price.get_text()
            unit_price = unit_price[:-1]  # 把最后的一个万字去掉
            update_info('money', unit_price, ID_num)
            update_info('current_data', current_data, ID_num)
            ID_num += 1
        ID_num = current_id
        for link in soup.find_all('div', 'houseInfo'):  # 房子的相关信息，排除出各种别墅
            # print url
            context = link.get_text()
            # print 'info:'+context
            village = context.split('|')[0]
            house_type = context.split('|')[1]
            square = context.split('|')[2][:-3]  # 把平米两个字去掉
            orientation = context.split('|')[3]
            if '别墅' in house_type:
                house_type = context.split('|')[2]
                square = context.split('|')[3][:-3]  # 把平米两个字去掉
                orientation = context.split('|')[4]
            update_info("village", village, ID_num)
            update_info("house_type", house_type, ID_num)
            update_info("square", square, ID_num)
            update_info("orientation", orientation, ID_num)
            update_info("location", location_chinese, ID_num)
            if len(context.split("|")) >= 5:
                decorate = context.split('|')[4]
                update_info("decorate", decorate, ID_num)
            else:
                pass
            ID_num += 1
        ID_num = current_id
        for price in soup.find_all('div', 'unitPrice'):  # 单价的信息
            unit_price = price.get_text()
            # print unit_price
            unit_price = re.findall(r"\d+\.?\d*", unit_price)[0]
            update_info("per_square", unit_price, ID_num)
            update_info("page", current_page, ID_num)
            ID_num += 1
        ID_num = current_id
        for price in soup.find_all("a", attrs={"target": "_blank", 'class': "title"}):  # 获取链接
            url_text = price.get('href')
            # print url_text
            update_info("url", url_text, ID_num)
            ID_num += 1
        current_id = ID_num
        # print current_page
        # print ID_num
        current_page += 1
    return get_row()


if __name__ == '__main__':
    now_time_start = datetime.datetime.now()  # 现在
    create_table()
    row = get_row()  # 获取数据库中有多少行数据
    row = get_house('binjiang', row + 1)
    print('当前时间为：*************************************************')
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print('总计已采集数据量为' + str(row) + '    ' + str(time.clock()))
    row = get_house("jianggan", row + 1)
    print('总计已采集数据量为' + str(row) + '    ' + str(time.clock()))
    row = get_house('gongshu', row + 1)
    print('总计已采集数据量为' + str(row) + '    ' + str(time.clock()))
    row = get_house('shangcheng', row + 1)
    print('总计已采集数据量为' + str(row) + '    ' + str(time.clock()))
    row = get_house('yuhang', row + 1)
    print('总计已采集数据量为' + str(row) + '    ' + str(time.clock()))
    row = get_house('xiaoshan', row + 1)
    print('总计已采集数据量为' + str(row) + '    ' + str(time.clock()))
    row = get_house('xihu', row + 1)
    print('总计已采集数据量为' + str(row) + '    ' + str(time.clock()))
    row = get_house('xiacheng', row + 1)
    print('总计已采集数据量为' + str(row) + '    ' + str(time.clock()))
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    now_time_end = datetime.datetime.now()  # 现在
    print((now_time_end - now_time_start))  # 计算时间差