import Queue
import urlparse
import os
import requests
from urllib import quote
from bs4 import BeautifulSoup
import sys
import re
import json
from backend import tmall,jd,amazon,one

def get_tmall(name):
	try:
		tmall.get(name)
	except:
		return list()
	f=open(name+'_tmall.json','r')
	tmall_list=json.load(f)
	f.close()
	os.remove(name+'_tmall.json')
	return tmall_list

def get_jd(name):
	try:
		jd.get(name)
	except:
		return list()
	f=open(name+'_jd.json','r')
	jd_list=json.load(f)
	f.close()
	os.remove(name+'_jd.json')
	return jd_list

def get_amazon(name):
	try:
		amazon.get(name)
	except:
		return list()
	f=open(name+'_amazon.json','r')
	amazon_list=json.load(f)
	f.close()
	os.remove(name+'_amazon.json')
	return amazon_list

def get_one(name):
	try:
		one.get(name)
	except:
		return list()
	f=open(name+'_one.json','r')
	one_list=json.load(f)
	f.close()
	os.remove(name+'_one.json')
	return one_list

def get_items(name):
	result=[]
	result.extend(get_jd(name))
	result.extend(get_tmall(name))
	result.extend(get_amazon(name))
	result.extend(get_one(name))
	return result

if __name__ == "__main__":
    get_items('iphone')