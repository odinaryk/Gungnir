#encoding=utf-8
import Queue
import urlparse
import os
import requests
from urllib import quote
from bs4 import BeautifulSoup
import sys
import json
import re
queue = Queue.Queue()
processed_url = set()
processed_img = set()
PIC_ROOT = "cache"
basket=[]
pronum=3
def output(basket,filename):
    f=open(filename,'w')
    json.dump(basket[:3],f, encoding = "gb2312")
def prepare(name):
    first = "http://search.yhd.com/c0-0/k"
    url = first + name
    return url
def get_picture(soup):
    first=soup.find('div',{'class':'mBox clearfix'})
    second=first.find('b')
    third=second.find('img')
    return third['src']

def get_price(soup,num):
    i=0
    results=[]
    for item in soup.find_all('div',{'class':'itemBox'}):
        price=item.find('p',{'class':'proPrice'})
        first=price.find('em',{'class':'num'})
        result=str(first.get_text().encode('utf-8'))[0:10]
        price=re.findall(r"\d+\.?\d*",result)[0]
        results.append(price)
        i = i + 1
        if i == num: break
    return results
def get(name):
    num=3
    del basket[:]
    url = prepare(name)
    processor(url,num)
    output(basket,name+'_one.json')
def get_name(soup):
    first=soup.find('div',{'class':'mod_detailInfo_proName'})
    return first.h1.text

def get_rate(soup,num):
    i=0
    results=[]
    for item in soup.find_all('p',{'class':'proPrice'}):
        first=item.find('span',{'class':'positiveRatio'})
        if str(first) != 'None':
            result=first.text
            final=result[1:5]
            results.append(final)
           
        else:
            results.append('-1')
        i = i + 1
        if i == num: break
    return results

def save_img_url_to_file(img_url,name):
    data = requests.get(img_url).content
    while img_url and img_url[-1] == '/':
        img_url = img_url[:-1]
    filename = name
    file(os.path.join(PIC_ROOT, filename), "wb").write(data)
#using url to get information，call functions such as get_rate
#price and rate are gotten in the original webpage
#name、picture、source are gottem in the detail page     
def processor(url,num):
    pageSource = requests.get(url).text
    soup = BeautifulSoup(pageSource,"html.parser")
    i = 0
    pri=get_price(soup,num)
    rat=get_rate(soup,num)
    
    for item in soup.find_all('p',{'class':'proName clearfix'}):
        
        if i == num:
            break
        thing={}
        temp = item.find('a')
        thing['source']=temp['href']#get the source of the goods
        
        pageSource = requests.get(thing['source']).text
        soup2 = BeautifulSoup(pageSource,"html.parser")
        thing['name']=get_name(soup2)#using source to enter the detailed page
        
        thing['rate']=rat[i]#all the rates of those goods have been obtained in the get_rate function,we append them to thing.rate in order
        
        
      
        picurl =get_picture(soup2)
       
        thing['picture']='one_'+str(i)+'.jpg'
        save_img_url_to_file(picurl,thing['picture'])
        
        thing['price']=pri[i]#all the prices of those goods have been obtained in the get_price function,we append them to thing.price in order
       
        thing['sale']='-1'
        basket.append(thing)#a thing is completed ,we add it to the basket list
        i = i + 1

    
    
    
       
   




def main():
    name = "ipad"
    get(name,pronum)
    
if __name__ == "__main__":
    main()

        
    
       
