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
root = Tk()
root.fileName = filedialog.askopenfilename( filetypes = (("Text file","*.txt"),("All Types","*.*")))
path = r"C:\Python35-32\chromedriver.exe"
f = open(str(root.fileName),'r')
keywrd = []
stat = []
cmpny = []

for l in f:
    keywrd.append(l.strip())

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
head = 0
c = 0
driver = webdriver.Chrome(chrome_options=chrome_options)
for line in keywrd:
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    if c < 7:
        driver.get('https://www.google.co.in/search?sclient=psy-ab&site=&source=hp&q='+'"'+line.strip()+'"'+'&oq='+'"'+line.strip()+'"')
    else:
        driver.quit()
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get('https://www.google.co.in/search?sclient=psy-ab&site=&source=hp&q='+'"'+line.strip()+'"'+'&oq='+'"'+line.strip()+'"')
        c = 0
    soup = BeautifulSoup(driver.page_source,"html.parser")
    a = driver.find_element_by_css_selector('div#resultStats')
    stat.append(a.text)
    cmpny.append(line.strip())
    newp = r"C:\\outputsCategory\\Search Res\\" 
    if not os.path.exists(newp):
        os.makedirs(newp)
    csvfl = open(r"C:\\outputsCategory\\Search Res\\results.csv","a",encoding='utf-8')
    df['Company'] = cmpny
    df1['Stats'] = stat
    df2 = pd.concat([df,df1], ignore_index=True, axis=1)
    df2.columns = ['Company Name','Number of Search Results']
    if head == 0:
        df2.to_csv(csvfl,index = None)
    else:
        df2.to_csv(csvfl, header = False,index = None)
    head = head + 1
    c = c + 1
    del df
    del df1
    del df2
    del stat[:]
    del cmpny[:]
    time.sleep(randint(1,3))
driver.quit()
