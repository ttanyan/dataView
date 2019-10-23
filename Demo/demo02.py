import requests,os,random,time
from bs4 import BeautifulSoup
class xiacf():
    htm=""
    wangye=""
    tmingzi=""
    lis=[]   #转抓到的网页
    lisat=[]
    def req(self,hht):           #抓页面元素
        self.htm=requests.get(hht)
        return self.htm
        # print(self.htm.content)
    def jiexi(self,tag,divmingzi,num):  #tag=要窃取的标签名字 divmingzi=tag的属性，num=下标
        soup = BeautifulSoup(self.htm.content, 'html.parser')
        div=soup.find_all(name=tag,attrs={divmingzi})[num]   #取出DIV
        # print(div.find_all(name='li')[0])
        # lis=div.find_all(name='li')[0]
        # h=lis.find_all(name='a')[0]['href']
        # print(h)
        for i in range(len(div.find_all(name='li'))):     #取出所有大图的进入地址
            lis=div.find_all(name='li')[i].find_all(name='a')[0]['href']
            # h=lis.find_all(name='a')[0]['href']
            hq='http://www.xiachufang.com/'+lis  #大图片地址
            # print(hq)
            # self.lisat.append(hq)              #地址存入self.lisat
            # self.req(self.lisat[i])
            soup = BeautifulSoup(self.req(hq).content, 'html.parser')  #返回大图地址页面
            # print(soup.find_all(name='img')[i]['src'])
            ran=soup.find_all(name='img')[0]['src']    #抓取大图页面大图SRC
            print(ran)
            self.req(ran)   #请求大图SRC  并将大图content存入，self.htm
            try:
                self.tmingzi=soup.find_all(name='img')[i]['alt']+str(random.randint(11,22)).split('的')[0]  #抓取大图页面大图名字
                self.baocun(self.tmingzi+'.png')     #保存 self.htm.content
                time.sleep(3)
            except:
                pass
        # lis=div.find_all(name='li')[2].find_all(name='a')[0]['href']
        # hq='http://www.xiachufang.com/'+lis
        # print(hq)
        #
        # soup = BeautifulSoup(self.req(hq).content, 'html.parser')
        # ran=soup.find_all(name='img')[0]['src']
        # self.tmingzi=soup.find_all(name='img')[0]['alt']+str(random.randint(1,22))
        # print(ran)
        # print(self.tmingzi)

        # s='罗宋汤的做法14'
        # print(s.split('的')[0])
        # img=self.req(soup.find_all(name='img')[0]['src'])
        #     print(li.find_all(name='a',attrs={"target":"_blank"})[1])
            # print(li)
        # lena=len(div.find_all(name='a'))
        # for i in range(lena):
        # print(div.find_all(name='a',attrs={"target":"_blank"})[1])
        # print(div.find_all(name='a',attrs={"target":"_blank"})[0]['href'])
        # self.wangye=div.find_all(name='img')[1]['data-src']
        # self.tmingzi=div.find_all(name='img')[1]['alt']
        # self.req(self.wangye)
        # print(self.htm.content)

        # lenth=len(div.find_all(name='img'))
        # for i in range(lenth):
        #     # print(i)
        #     #每个网站需要改---
        #     self.req(div.find_all(name='img')[i]['data-src'])
        #     # print(div.find_all(name='img')[i]['data-src'])  #图片请求地址
        #     self.tmingzi=div.find_all(name='img')[i]['alt']+str(random.randint(11,22)) #名字请求爬取
        #     self.baocun(self.tmingzi+'.png')

    def baocun(self,mingzi):
        # path='D:\\pac'
        try:
            # os.mkdir(path + './baogao')
            os.mkdir('D:\\'+ './pac')
        except:
            pass
        with open("D:\\pac\\%s"%mingzi,"wb") as f:
            f.write(self.htm.content)
            pass

    def palei(self):    #抓出所有炒饭类网页
        htm1=requests.get('http://www.xiachufang.com/category/731/')
        soup = BeautifulSoup(htm1.content, 'html.parser')
        div1=soup.find_all(name='ul',attrs={'level2 plain list hidden'})
        # print(div1)
        # name=div1[0].find_all('a')[0].text
        # print(name)
        # print(div1[0].find_all('a'))
        for i in range(len(div1[1].find_all('a'))):
            # print(div1[0].find_all('a')[i]['href'])
            a='http://www.xiachufang.com'+div1[1].find_all('a')[i]['href']
            self.lis.append(a)
            # print(self.lis[i])
    def wangz(self):
        self.palei()
        lennum=len(self.lis)
        # print(self.lis)
        for j in range(lennum):
            wy=self.lis[j]
            for i in range(1,5):
                wy=self.lis[j]+"/?page=%d"%i
                print(wy)
                self.req(wy)
                self.jiexi('div','normal-recipe-list',0)
x=xiacf()
x.wangz()
# x.req('http://www.xiachufang.com/category/20130/')
# x.jiexi('div','normal-recipe-list',0)
# x.palei()

