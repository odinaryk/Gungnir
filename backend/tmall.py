#encoding=utf-8
#name:楼思琦
#ID:5140379052
import requests
import os
import json
from urllib import quote
from urllib import unquote
from bs4 import BeautifulSoup

productNum=3
PIC_ROOT="cache"
# url of the search page
def encodeName(name):
    head="https://list.tmall.com/search_product.htm?"
    second="q="
    third="&click_id="
    url=head+second+name+third+name
    return url

# get pic(url) from the search page 
# return a list of the first num-th pic(url)
def get_pic(soup,num):
    result=[]
    i=0
    for second in soup.find_all('div',{'class':'productImg-wrap'}):
        if i==num:
            break
        result.append('https:'+str(second.img.get('src')))
        i=i+1
    return result

# get name from the search page 
# return a list of the first num-th name
def get_name(soup,num):
    result=[]
    i=0
    for second in soup.find_all('p',{'class':'productTitle'}):
        if i==num:
            break
        result.append(second.a.get('title'))
        print second.a.get('title')
        i=i+1
    return result

# get rate from the search page 
# sadly,TMall page store the rate by Dynamic interaction 
# so i can't get it and set it default value:'-1'
def get_rate(soup,num):
    result=[]
    i=0
    for i in range(num):
        result.append('-1')
    return result

# get sale from the search page 
# return a list of the first num-th sale
def get_sale(soup,num):
    result=[]
    i=0
    for second in soup.find_all('p',{'class':'productStatus'}):
        if i==num:
            break
        sale=second.em.text
        strr=sale.encode('gbk')
        l=len(strr)
        s=0
        ss=u'万笔'
        sss=ss.encode('gbk')
        print l
        if l>4 and strr[l-4:l]==sss:
            s=float(strr[0:l-4])*10000
        else:
            s=int(strr[0:l-2])
        result.append(str(s))
        i=i+1
    return result

# get price from the search page 
# return a list of the first num-th price
def get_price(soup,num):
    result=[]
    i=0
    for second in soup.find_all('p',{'class':'productPrice'}):
        if i==num:
            break
        result.append(second.em.get('title'))
        i=i+1
    return result
	
# get item-url from the search page 
# return a list of the first num-th url
def get_source(soup,num):
    result=[]
    i=0
    for second in soup.find_all('p',{'class':'productTitle'}):
        if i==num:
            break
        url=second.a.get('href')
        result.append('https:'+str(url))
        i=i+1
    return result

# save img to file
def save_img_url_to_file(img_url,name):
    print u"saving %s" % img_url
    data = requests.get(img_url).content
    while img_url and img_url[-1] == '/':
        img_url = img_url[:-1]
    filename = name
    file(os.path.join(PIC_ROOT, filename), "wb").write(data)

# get all information by search page
def processor(url,num):
    pageSource = requests.get(url).text
    soup = BeautifulSoup(pageSource,"html.parser")#from_encoding="gbk"
    i = 0
    basket=[]
    name=get_name(soup,num)
    price=get_price(soup,num)
    sale=get_sale(soup,num)
    pic=get_pic(soup,num)
    rate=get_rate(soup,num)
    source=get_source(soup,num)
    
    PicName=[]

    for i in range(min(num,len(source))):
        picurl=pic[i]
        PicName.append(picurl[picurl.rfind('/')+1:])
        save_img_url_to_file(pic[i],PicName[i])
        conv={}
        conv['source']=source[i]
        conv['name']=name[i]
        conv['price']=price[i]
        conv['rate']=rate[i]
        conv['sale']=sale[i]
        conv['picture']=PicName[i]
        basket.append(conv)
    return basket
    
class provider:
  url=""
  goods=[]

  def __init__(self,url):
    self.url=url
    self.goods=processor(url,productNum)

  def dump(self,filename):
    f=open(filename,'w')
    json.dump(self.goods[:productNum],f)

def get(name):
    url = encodeName(name)
    prov=provider(url)
    prov.dump(name+'_tmall.json')
    
def main():
    productName=input('Search:')
    get(productName)

if __name__ == "__main__":
    main()

