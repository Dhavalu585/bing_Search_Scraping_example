
# coding: utf-8

# In[8]:

import tkinter
from tkinter import Tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
root = Tk()
root.fileName = filedialog.askopenfilename( filetypes = (("Text file","*.txt"),("All Types","*.*")))
path = r"C:\Python35-32\chromedriver.exe"
f = open(str(root.fileName),'r')
root.fileName = filedialog.askopenfilename( filetypes = (("Text file","*.txt"),("All Types","*.*")))
f2 = open(str(root.fileName),'r')


# In[9]:

snippets = []
links = []
params = []
keywrd = []
keywrd2 = []


# In[10]:

for l in f:
    keywrd.append(l.strip())
for l2 in f2:
    keywrd2.append(l2.strip())


# In[11]:

for line in keywrd:
    driver = webdriver.Chrome(path)
    for line2 in keywrd2:
        df = pd.DataFrame()
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        df3 = pd.DataFrame()
        driver.get('https://www.bing.com/search?q='+'"'+line.strip()+'"'+' '+'"'+line2.strip()+'"'+'&go=Search&qs=bs&form=QBRE')
        soup = BeautifulSoup(driver.page_source,"html.parser")
        
        search = soup.findAll('li',attrs={'class':'b_algo'})
        for item in search:
            a = item.findAll('div',attrs={'class':'b_caption'})
            for item2 in a:
                b = item2.findAll('p')
                for item3 in b:
                    snippets.append(item3.text)
                    params.append(line2)
        srch2 = soup.findAll('span',attrs={'class':'b_address'})
        for it2 in srch2:
            snippets.append(it2.text)
            params.append(line2)
        srch3 = soup.findAll('div',attrs={'class':'lfact'})
        for it3 in srch3:
            snippets.append(it3.text)
            params.append(line2)
        lk = soup.findAll('li',attrs={'class':'b_algo'})
        for itm in lk:
            ab = itm.findAll('h2')
            for itm2 in ab:
                ab2 = itm2.findAll('a')
                for ab3 in ab2:
                    links.append(ab3.get('href'))
        csvfl = open(line+".csv","a",encoding='utf-8')
        df['parameters'] = params
        df1['snippet'] = snippets
        df2['link'] = links
        df3 = pd.concat([df,df1,df2], ignore_index=True, axis=1)
        df3.to_csv(csvfl, header = False, index = None)
        csvfl.close()
        del df
        del df1
        del df2
        del df3
        del snippets[:]
        del links[:]
        del params[:]
    driver.quit()
