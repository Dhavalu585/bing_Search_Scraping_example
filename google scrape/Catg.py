
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
from time import strftime
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
b = firefox_binary = FirefoxBinary(r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe")
b.add_command_line_options("-private")

root = Tk()
root.fileName = filedialog.askopenfilename( filetypes = (("Text file","*.txt"),("All Types","*.*")))
path = r"C:\Python35-32\chromedriver.exe"
f = open(str(root.fileName),'r')
root.fileName = filedialog.askopenfilename( filetypes = (("Comma Separated Value file","*.csv"),("All Types","*.*")))
f2 = open(str(root.fileName),'r')
snippets = []
links = []
params = []
keywrd = []
catlst = []
dt = []
stat = []

for l in f:
    keywrd.append(l.strip())
ipdf = pd.read_csv(f2,encoding = 'utf-8')
cat = list(ipdf.columns.values)


# In[11]:
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--incognito")
#chrome_options.add_argument('--proxy-server=216.58.209.154:9050')

driver = webdriver.Firefox(firefox_binary=b)
for line in keywrd:
    #driver = webdriver.Firefox(firefox_profile = prof.set_preference("browser.privatebrowsing.autostart", True))
    head = 0
    for category in cat:
        for line2 in list(ipdf[category]):
            #os.remove(r"C:\\Users\\rickyp\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies"
            df = pd.DataFrame()
            df1 = pd.DataFrame()
            df2 = pd.DataFrame()
            df3 = pd.DataFrame()
            df4 = pd.DataFrame()
            df5 = pd.DataFrame()
            df6 = pd.DataFrame()
            if str(line2) != "nan":
                driver.get('http://216.58.209.154/search?sclient=psy-ab&site=&source=hp&q='+'"'+line.strip()+'"'+' '+line2.strip()+'&oq='+'"'+line.strip()+'"'+' '+line2.strip())
            else:
                break
            soup = BeautifulSoup(driver.page_source,"html.parser")
            search = soup.findAll('span', attrs={'class':'st'})
            for item in search:
                snippets.append(item.text)
                params.append(line2)
                catlst.append(str(category))
                dt.append(str(strftime("%Y-%m-%d %H:%M:%S")))
            addsrch = soup.findAll('div',attrs={'class':'mod'})
            ls = []
            for item in addsrch:
                item2 = item.findAll('div',attrs={'class':'_eFb'})
                for item3 in item2:
                    item4 = item3.findAll('div',attrs={'class':'_mr kno-fb-ctx'})
                    for item5 in item4:
                        item6 = item5.findAll('span',attrs={'class':'_Xbe'})
                        for item7 in item6:
                            ls.append(item7.text)
                            snippets.append(' '.join(ls[:]))
                            params.append(line2)
                            catlst.append(str(category))
                            dt.append(str(strftime("%Y-%m-%d %H:%M:%S")))
            del ls[:]       
            linksrch = soup.findAll('div',attrs={'class':'g'})
            for item in linksrch:
                item2 = item.findAll('div',attrs={'class':'rc'})
                for item3 in item2:
                    item4 = item3.findAll('h3',attrs={'class':'r'})
                    for item5 in item4:
                        item6 = item5.findAll('a')
                        for item7 in item6:
                            links.append(item7.get('href'))
                            try:
                                a = driver.find_element_by_css_selector('div#resultStats')
                                stat.append(a.text)
                            except Exception:
                                stat.append("No Data")
                                params.append(line2)
                                catlst.append(str(category))
            try:
                b = driver.find_element_by_css_selector('a.q.qs')
            except Exception:
                print("IP Blocked")
                time.sleep(30)
                #driver.quit()
            newp = r"C:\\outputsCategory\\google\\" 
            if not os.path.exists(newp):
                os.makedirs(newp)
            csvfl = open(r"C:\\outputsCategory\\google\\"+line+".csv","a",encoding='utf-8')
            df['parameters'] = params
            df1['snippet'] = snippets
            df2['link'] = links
            df4['category'] = catlst
            df5['Date'] = dt
            df6['Stats'] = stat
            df3 = pd.concat([df4,df,df1,df2,df5,df6], ignore_index=True, axis=1)
            df3.columns = ['Category','Keyword','Snippet','link','Date & time','Stats']
            if head == 0:
                 df3.to_csv(csvfl,index = None)
            else:
                df3.to_csv(csvfl, header = False,index = None)
            head = head + 1
            csvfl.close()
            del df
            del df1
            del df2
            del df3
            del df4
            del df5
            del df6
            del catlst[:]
            del snippets[:]
            del links[:]
            del params[:]
            del dt[:]
            del stat[:]
            time.sleep(randint(2,5))
driver.quit()


# In[5]:




# In[ ]:



