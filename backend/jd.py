import requests
import re
import json
import os
Pic_Dir = "cache"
def save_pic(url,fname):
  f=open(os.path.join(Pic_Dir, fname), "wb")
  r=requests.get(url)
  f.write(r.content)
  f.close()

def process_item(item):
  url_head="http://item.m.jd.com/product/"
  url_tail=".html"
  conv={}
  conv['source']=url_head+item['wareId']+url_tail
  conv['name']=item['wname']
  conv['price']=item['jdPrice']
  conv['rate']=item['good']
  conv['sale']=item['totalCount']
  conv['picture']=item['imageurl']
  url=conv['picture']
  picname=url[url.rfind('/')+1:]
  save_pic(url,picname)
  conv['picture']=picname
  return conv

def get_data(name):
  base_url="http://m.jd.com/ware/search.action?keyword="
  result=[]
  req=requests.get(base_url+name)
  pat='"wareList":(\[.*?\}\])'
  json_list=json.loads(re.findall(pat,req.text)[0])
  for item in json_list:
    result.append(process_item(item))
  return result

class provider:
  name=""
  goods=[]
  goods_num=3
  def __init__(self,name):
    self.name=name
    self.goods=get_data(name)
  def dump(self,filename):
    f=open(filename,'w')
    json.dump(self.goods[:self.goods_num],f)

def get(name):
  prov=provider(name)
  prov.dump(name+'_jd.json')

def main():
  s=input('Search:')
  get(s)

if __name__ == "__main__":
    main()