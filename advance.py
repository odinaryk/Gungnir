#encoding=utf-8
#save function
#list name basket
#name is in the search box
import json
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator  
import time
#the order of goods are tmall,amazon,jingdong,one
num=3
#save the price of each search
#if there is already some records of the search_name,
#add a new name
#else
#add a pair of new key-value to the dictionnary

def saveprice(basket,tname):
    cur_time=time.strftime("%m-%d %H:%M",time.localtime(time.time()))
    summary=0
    if os.path.exists(r'saves.json'):
         file_object = open("saves.json",'r+')
         dic=json.load(file_object)
    else:
        dic={}
    prices=[]
    prices.append(cur_time)
    oldprices=[]
    pricelist=[]
    names=['tmall','amazon','jd','one']
    identify=['tmall','amazon','jd','yhd']
    tmp=[[],[],[],[]]
    print tname
    for item in basket:
    	for i in range(len(identify)):
    		if item['source'].find(identify[i])!=-1:
    			tmp[i].append(float(item['price']))
    for lst in tmp:
    	if len(lst)!=0:
    		prices.append(sum(lst)/len(lst))
    	else:
    		prices.append(-1) 
    
    if(dic.has_key(tname)):
        oldprices=dic[tname]
        oldprices.append(prices)
        dic[tname]=oldprices
    else:
        print 1
        pricelist.append(prices)
        dic[tname]=pricelist
    #write back
    if os.path.exists(r'saves.json'):
        file_object .close()
    f=open("saves.json",'w')
    json.dump(dic,f, encoding = "gb2312")
        
        
    
def drawpic(name):
    file_object = open('saves.json','r')
    dic=json.load(file_object)
    file_object.close()
    x_time=[]
    y_tmall=[]
    y_amazon=[]
    y_jingdong=[]
    y_one=[]
    x=[]
    if dic.has_key(name):
        for i in range(0,len(dic[name])):
            x_time.append(dic[name][i][0])
            y_tmall.append(dic[name][i][1])
            y_amazon.append(dic[name][i][2])
            y_jingdong.append(dic[name][i][3])
            y_one.append(dic[name][i][4])
            x.append(0.3*(i+1))
   
    for i in range(0,len(y_tmall)):
        print y_tmall[i]
    fig = plt.figure()
    ax=plt.gca() 
    plt.xlabel('time')
    plt.ylabel('average price')
    plt.plot(x, y_tmall,"-or",label="tmall")
    plt.plot(x, y_amazon,"-og",label='amazon' )
    plt.plot(x, y_jingdong,"-ob" ,label='jd')
    plt.plot(x, y_one,"-oc" ,label='one')
    ax.legend(loc='best')
    #ax.xaxis.set_major_locator(x_time)
    ax.set_title('history price')
    ticks = ax.set_xticks(x)
    ax.set_xticklabels(x_time,rotation=30, fontsize='small')
    plt.show()


def creatdic():
    f=open('oneq.json','a+')
    dic=json.load(f)
    return dic
    
def main():
    name="饼干"
    basket=creatdic()
    saveprice(basket,name,num)
    drawpic(name)
    
    
if __name__ == "__main__":
    main()
       
