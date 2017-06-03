import tkinter
from tkinter import Tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from time import strftime
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import os
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
stat = []
dt = []
for l in f:
    keywrd.append(l.strip())
ipdf = pd.read_csv(f2,encoding = 'utf-8')
cat = list(ipdf.columns.values)

c = 0 
path = r"C:\Python35-32\chromedriver.exe"
driver = webdriver.Chrome(path)
for line in keywrd:
    head = 0
    for category in cat:
        for line2 in list(ipdf[category]):
            df = pd.DataFrame()
            df1 = pd.DataFrame()
            df2 = pd.DataFrame()
            df3 = pd.DataFrame()
            df4 = pd.DataFrame()
            df5 = pd.DataFrame()
            df6 = pd.DataFrame()
            if str(line2) != "nan":
                driver.get('https://www.bing.com/search?q='+'"'+str(line).strip()+'" '+' '+str(line2).strip()+'&go=Search&qs=bs&form=QBRE')
            else:
                break
            soup = BeautifulSoup(driver.page_source,"html.parser")
            search = soup.findAll('li',attrs={'class':'b_algo'})
            for item in search:
                a = item.findAll('div',attrs={'class':'b_caption'})
                for item2 in a:
                    b = item2.findAll('p')
                    for item3 in b:
                        snippets.append(item3.text)
                        params.append(line2)
                        catlst.append(str(category))
                        dt.append(str(strftime("%Y-%m-%d %H:%M:%S")))
            srch2 = soup.findAll('span',attrs={'class':'b_address'})
            for it2 in srch2:
                snippets.append(it2.text)
                params.append(line2)
                catlst.append(str(category))
                dt.append(str(strftime("%Y-%m-%d %H:%M:%S")))
            srch3 = soup.findAll('div',attrs={'class':'lfact'})
            for it3 in srch3:
                snippets.append(it3.text)
                params.append(line2)
                catlst.append(str(category))
                dt.append(str(strftime("%Y-%m-%d %H:%M:%S")))
            lk = soup.findAll('li',attrs={'class':'b_algo'})
            for itm in lk:
                ab = itm.findAll('h2')
                for itm2 in ab:
                    ab2 = itm2.findAll('a')
                    for ab3 in ab2:
                        links.append(ab3.get('href'))
                        try:
                            a = driver.find_element_by_css_selector('span.sb_count')
                            stat.append(a.text)
                        except Exception:
                            stat.append("No Data")
                            params.append(line2)
                            catlst.append(str(category))
            #newp = r"C:\\outputsCategory\\"+str(re.sub('[-]','',category))
            newp = r"C:\\outputsCategory\\Bing\\" 
            if not os.path.exists(newp):
                os.makedirs(newp)
            csvfl = open(r"C:\\outputsCategory\\bing\\"+line+".csv","a",encoding='utf-8')
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
        c = c + 1
driver.quit()
