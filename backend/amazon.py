#encoding=utf-8
import Queue
import urlparse
import os
import requests
from urllib import quote
from bs4 import BeautifulSoup
import sys
import json
queue=Queue.Queue()
processed_url=set()
processed_img=set()
PIC_ROOT="cache"
class goods:
    identity=0
    name=""
    source=""
    rate=0
    picture=""
    price=0
    def __init__(self):
        self.rate=0
    def __repr__(self):
        print self.name
        print self.source
        print self.rate
        print self.picture
        print self.price
        return "good"

def prepare(name):
    first = "http://www.amazon.cn/s/field-keywords="
    url = first + name
    return url

def get_picture(soup): 
    i=0
    results=[]
    for item in soup.find_all('div',{'class':'a-section a-spacing-none a-inline-block s-position-relative'}):
        first=item.find('a')
        second=first.find('img')
        results.append(second.get('src'))
        i=i+1
        if i==3:
            break
    return results

def get_price(soup):
    i=0
    results=[]
    for item in soup.find_all('span',{'class':'a-size-base a-color-price s-price a-text-bold'}):
        first=item.text
        results.append(first)
        i=i+1
        if i==3:
            break
    return results

def get_name(soup):
    i=0
    results=[]
    for item in soup.find_all('a',{'class':'a-link-normal s-access-detail-page  a-text-normal'}):
        first=item.get('title')
        results.append(first)
        i=i+1
        if i==3:
            break
    return results

def get_rate(soup):
    i=0
    results=[]
    for item in soup.find_all('span',{'class':'a-icon-alt'}):
        try:
            first=float(item.text[2:5])
            second=str(first*100/5.0)+'%'
        except:
            second='-1'
        results.append(second)
        i=i+1
        if i==3:
            break
    return results

def get_source(soup):
    i=0
    results=[]
    for item in soup.find_all('li',{'class':"s-result-item  celwidget "}):
        first = item.get('data-asin')
        second="www.amazon.cn/dp/"+first+"/"
        results.append(second)
        i=i+1
        if i==3:
            break
    return results

def save_img_url_to_file(img_url,name):
        print u"saving %s" % img_url
        data = requests.get(img_url).content
        while img_url and img_url[-1] == '/':
            img_url = img_url[:-1]
        filename = name
        file(os.path.join(PIC_ROOT, filename), "wb").write(data)

def dump(basket,filename):
    f=open(filename,"w")
    json.dump(basket,f)

def processor(url):
    pageSource = requests.get(url).text
    soup = BeautifulSoup(pageSource)
    i = 0
    basket=[]
    Price=get_price(soup)
    Name=get_name(soup)
    Rate=get_rate(soup)
    Source=get_source(soup)
    Pic=get_picture(soup)
    for i in range(min(3,len(Source))):
        thing={}
        thing["name"]=Name[i]
        thing["price"]=Price[i][1:].replace(',','')
        thing["rate"]=Rate[i]
        thing["source"]=Source[i]
        thing['sale']='-1'
        thing["picture"]=Pic[i]
        thing["picture"]=thing["picture"][thing["picture"].rfind('/')+1:]
        basket.append(thing)
        save_img_url_to_file(Pic[i],thing["picture"])
    return basket

def get(name):
    url = prepare(name)
    basket=processor(url)
    dump(basket,name+"_amazon.json")

def main():
    name = "kindle"
    get(name)
if __name__ == "__main__":
    main()
