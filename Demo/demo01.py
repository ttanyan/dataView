print("hello,world!")
str321="string"
str1="str123"
print(str321+str1)
import keyword
print(keyword.kwlist)
keyword.kwlist

from sys import argv,path
print('导入模块');
print('path:',path)
i=1
if i>1 :
   print('i是大于1的')
elif i==1 :
   print('i=1')

else :
   print('i<1')

print(r'Ru\noob')
print('Ru\noob')

print(type(1))

import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup

def get_house_href(total_page=2):
   """
   获取文本后面的链接网址
   :return:无
   """
   i = 1
   while i < total_page:
      url = 'http://cq.lianjia.com/ershoufang/binjiang/pg' + str(i) + '/'
      page = urllib.request.urlopen(url)
      soup = BeautifulSoup(page, "html.parser")
      print("=====================================page==============================")
      print(page)
      print("=====================================soup==============================")
      print(soup)
      for title in soup.find_all('div', 'title'):
         print("=====================================title==============================")
         print(title)
         print(type(title.a))
      i += 1
print(get_house_href(2))
