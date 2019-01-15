# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 15:46:11 2019

@author: lab123
"""

import requests
from bs4 import BeautifulSoup
import os
from threading import Thread

class Jbhdq:
#root_url='https://www.jbhdq.com/'
    def __init__(self):
        self.root_url='https://www.jbhdq.com'
        self.root_dir=r'E:\Dataset\jbh'
    def request_func(self,url):
        headers={'referer':'https://www.jbhdq.com/','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        r=requests.get(url,headers=headers)
        r.encoding='utf-8'
        if not r.status_code==200:
            print(url,' code error')
            return
        r_text=r.text
        r.close()
        return r_text
    
    def every_page(self,r_text):
        #this func is for every page
        title_url_d={}
        if not r_text:
            print('no r text')
            return
        soup=BeautifulSoup(r_text,'html.parser')
        wrapper=soup.find('div',class_='wrapper')
        a_list=wrapper.find_all('a')        
        for a in a_list:
#            print(self.root_url+a.get('href'),':',a.get('title'))
            title_url_d.setdefault(a.get('title'),self.root_url+a.get('href'))
        return title_url_d
#        return [self.root_url+a.get('href') for a in a_list]
    
    def one_html(self,url):
        alt_src_d={}
        r_text=self.request_func(url)
        soup=BeautifulSoup(r_text,'html.parser')
        content_div=soup.find('div',class_='content')
        if not soup.find('p',class_='step_img'):
            img_soup=content_div.find('img')
            src=img_soup.get('src')
            alt=img_soup.get('alt')
            alt_src_d.setdefault(alt,src)
        else:    
            for p in soup.find_all('p',class_='step_img'):
                src=p.find('img').get('src')
                alt=p.find('img').get('alt')
                alt_src_d.setdefault(alt,src)
        return alt_src_d
        
    def download(self,url,file_path):
        if os.path.exists(file_path):
            print(file_path,'exists')
            return
        headers={'referer':'https://www.jbhdq.com/','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        r=requests.get(url,headers=headers)
        with open(file_path,'wb') as f:
            f.write(r.content)
        print(file_path,'download successfully')
        r.close()
    
    def run(self,i):
        
            #this i is the page num
        if i==1:
            page_url='https://www.jbhdq.com/dongwu/'
        else:
            page_url='https://www.jbhdq.com/dongwu/list_{}.html'.format(str(i))
            
        r_text=self.request_func(page_url)
        title_url_d=self.every_page(r_text)
        for title,url in title_url_d.items():
            folder=os.path.join(self.root_dir,title)
            if not os.path.exists(folder):
                os.makedirs(folder)
            alt_src_d=self.one_html(url)
            
            for alt,url in alt_src_d.items():
                file_path=os.path.join(folder,alt+'.jpg')
                self.download(url,file_path)

if __name__=='__main__':
    jbh=Jbhdq()
    for i in range(1,116):
        t=Thread(target=jbh.run,args=(i,))
        t.start()
    
    