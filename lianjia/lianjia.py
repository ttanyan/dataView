#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#name   = lianjia
#author = rache
#time   = 2017/2/15 21:39
#Description=添加描述信息
#eMail   =tangtao@lhtangtao.com
#git     =lhtangtao
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
import datetime
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

from lianjia.my_sqldb import insert_info, update_info, get_row, create_table

#importlib.reload(sys)
#sys.setdefaultencoding('utf-8')
current_data = time.strftime('%Y-%m-%d', time.localtime(time.time()))
time.clock()


def get_house_href(total_page=2):
    """
    获取文本后面的链接网址
    :return:无
    """
    i = 1
    while i < total_page:
        url = 'http://cq.lianjia.com/ershoufang/yubei/pg' + str(i) + '/'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        for title in soup.find_all('div', 'title'):
            print(type(title.a))
        i += 1


def get_house(location="yubei", current_id=1):
    global location_chinese
    current_page = 1  # 当前在第几页
    total_page = 0  # 在这个区里一共有多少页房产信息
    url = 'http://cq.lianjia.com/ershoufang/' + location
    req = urllib.request.Request(url)
    time.sleep(1)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    if location == 'yubei':
        location_chinese = '渝北'
    elif location == 'jiangbei':
        location_chinese = '江北'
    elif location == 'yuzhong':
        location_chinese = '渝中'
    elif location == 'shapingpa':
        location_chinese = '沙坪坝'
    elif location == 'jiulongpo':
        location_chinese = '九龙坡'
    elif location == 'nanan':
        location_chinese = '南岸'
    elif location == 'dadukou':
        location_chinese = '大渡口'
    elif location == 'beibei':
        location_chinese = '北碚'
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
        #获取价格
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
            # print('info:'+context)
            village = context.split('|')[6]  # 楼房类型
            house_type = context.split('|')[0]  # 布局
            square = context.split('|')[1][:-3]  # 面积
            orientation = context.split('|')[2]  # 朝向
            year = context.split('|')[5]   # 年份
            decr = context.split('|')[3]   # 描述

            # if '别墅' in house_type:
            #     house_type = context.split('|')[2]
            #     square = context.split('|')[3][:-3]  # 把平米两个字去掉
            #     orientation = context.split('|')[4]
            update_info("village", village, ID_num)
            update_info("house_type", house_type, ID_num)
            update_info("square", square, ID_num)
            update_info("orientation", orientation, ID_num)
            update_info("location", location_chinese, ID_num)
            update_info("year", year, ID_num)
            update_info("decr", decr, ID_num)

            if len(context.split("|")) >= 5:
                decorate = context.split('|')[4]
                update_info("decorate", decorate, ID_num)
            else:
                pass
            ID_num += 1
        ID_num = current_id
        # 单价信息
        for price in soup.find_all('div', 'unitPrice'):  # 单价的信息
            strprice = price.get_text()
            unit_price = strprice[2:-1]
            print(unit_price)

            # unit_price = re.findall(r"\d+\.?\d*", unit_price)[0]
            update_info("per_square", unit_price, ID_num)
            update_info("page", current_page, ID_num)
            ID_num += 1
        ID_num = current_id
        # 获取链接地址
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
    row = get_house('yubei', row + 1)
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