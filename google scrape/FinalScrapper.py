
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
from random import randint
root = Tk()
root.fileName = filedialog.askopenfilename( filetypes = (("Text file","*.txt"),("All Types","*.*")))
path = r"C:\Python35-32\chromedriver.exe"
f = open(str(root.fileName),'r')
root.fileName = filedialog.askopenfilename( filetypes = (("Text file","*.txt"),("All Types","*.*")))
f2 = open(str(root.fileName),'r')
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
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

for line in keywrd:  
    driver = webdriver.Chrome(chrome_options=chrome_options)
    c = 0
    for line2 in keywrd2:
        c = c + 1
        if c > 7:
            driver.quit()
            driver = webdriver.Chrome(chrome_options=chrome_options)
            c = 0
        df = pd.DataFrame()
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        df3 = pd.DataFrame()
        driver.get('https://www.google.co.in/search?sclient=psy-ab&site=&source=hp&q='+'"'+line.strip()+'"'+' '+'"'+line2.strip()+'"'+'&oq='+'"'+line.strip()+'"'+' '+'"'+line2.strip()+'"')
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source,"html.parser")
        search = soup.findAll('span', attrs={'class':'st'})
        for item in search:
            snippets.append(item.text)
            params.append(line2)
        results = driver.find_elements_by_css_selector('div.g')
        for it in range(len(results)):
            if it < 10:
                l = results[int(it)].find_element_by_tag_name("a")
                href = l.get_attribute("href")
                links.append(href)
        csvfl = open(line+".csv","a",encoding='utf-8')
    
        df['parameters'] = params
        df1['snippet'] = snippets
        df2['link'] = links
        df3 = pd.concat([df,df1,df2], ignore_index=True, axis=1)
        df3.to_csv(csvfl, header = False)
        csvfl.close()
        del df
        del df1
        del df2
        del df3
        del snippets[:]
        del links[:]
        del params[:]
        time.sleep(randint(1,3))
    driver.quit()


# In[5]:




# In[ ]:



