import tkinter
from tkinter import Tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool
from random import randint
from time import sleep
import re
import os
from time import strftime

#This function will be called by two parallel threads to open two different browers window
#Our input to this function will be 0 and 1, So 0 for Bing and 1 for google
def serc(n):
    #if value of the input to the function is 0 then this will open up Bing Search in new browser window clean of any cookies and stuff.
    if n == 0:
        snippets = []
        links = []
        params = []
        keywrd = []
        catlst = []
        dt = []
        root = Tk()
        root.fileName = filedialog.askopenfilename( filetypes = (("Text file","*.txt"),("All Types","*.*")),title = 'FIRST FILE INPUT')
    #using root.fileName to open the file
        f = open(str(root.fileName),'r')
    #writing the whole file into a list
        for l in f:
            keywrd.append(l.strip())
        root.fileName = filedialog.askopenfilename( filetypes = (("Comma Separated Value file","*.csv"),("All Types","*.*")),title = 'TURN FOR SECOND FILE :)')
        f2 = open(str(root.fileName),'r')
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
                    if str(line2) != "nan":
                        driver.get('https://www.bing.com/search?q='+'"'+str(line).strip()+'"'+' '+str(line2).strip()+'&go=Search&qs=bs&form=QBRE')
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
            #newp = r"C:\\outputsCategory\\"+str(re.sub('[-]','',category))
                    newp = r"C:\\outputsCategory\\bing\\" 
                    if not os.path.exists(newp):
                        os.makedirs(newp)
                    csvfl = open(r"C:\\outputsCategory\\bing\\"+line+".csv","a",encoding='utf-8')
                    df['parameters'] = params
                    df1['snippet'] = snippets
                    df2['link'] = links
                    df4['category'] = catlst
                    df5['Date'] = dt
                    df3 = pd.concat([df4,df,df1,df2,df5], ignore_index=True, axis=1)
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
                    del catlst[:]
                    del snippets[:]
                    del links[:]
                    del params[:]
                    del dt[:]
                c = c + 1
        driver.quit()
    #Now input is 1 so time for google search and this inputs are parallel remember so both windows will open together.
    #code is mostly similar to bing search, I will mention only the differences 
    if n == 1:
        snippets = []
        links = []
        params = []
        keywrd = []
        catlst = []
        dt = []
        root = Tk()
        root.fileName = filedialog.askopenfilename( filetypes = (("Text file","*.txt"),("All Types","*.*")),title = 'FIRST FILE INPUT')
    #using root.fileName to open the file
        f = open(str(root.fileName),'r')
    #writing the whole file into a list
        for l in f:
            keywrd.append(l.strip())
        root.fileName = filedialog.askopenfilename( filetypes = (("Comma Separated Value file","*.csv"),("All Types","*.*")),title = 'TURN FOR SECOND FILE :)')
        f2 = open(str(root.fileName),'r')
        ipdf = pd.read_csv(f2,encoding = 'utf-8')
        cat = list(ipdf.columns.values)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")

        for line in keywrd:  
            driver = webdriver.Chrome(chrome_options=chrome_options)
            head = 0
            for category in cat:
                c = 0
                for line2 in list(ipdf[category]):
                    c = c + 1
                    if c > 7:
                        driver.quit()
                        driver = webdriver.Chrome(chrome_options=chrome_options)
                        c = 0
                    df = pd.DataFrame()
                    df1 = pd.DataFrame()
                    df2 = pd.DataFrame()
                    df3 = pd.DataFrame()
                    df4 = pd.DataFrame()
                    df5 = pd.DataFrame()
                    if str(line2) != "nan":
                        driver.get('https://www.google.co.in/search?sclient=psy-ab&site=&source=hp&q='+line.strip()+' '+line2.strip()+'&oq='+line.strip()+' '+line2.strip())
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
                    newp = r"C:\\outputsCategory\\google2\\" 
                    if not os.path.exists(newp):
                        os.makedirs(newp)
                    csvfl = open(r"C:\\outputsCategory\\google2\\"+line+".csv","a",encoding='utf-8')
                    df['parameters'] = params
                    df1['snippet'] = snippets
                    df2['link'] = links
                    df4['category'] = catlst
                    df5['Date'] = dt
                    df3 = pd.concat([df4,df,df1,df2,df5], ignore_index=True, axis=1)
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
                    del catlst[:]
                    del snippets[:]
                    del links[:]
                    del params[:]
                    del dt[:]
                    time.sleep(randint(1,3))
            driver.quit()
#this next line is necessary for using multiple threads 
if __name__ == '__main__':
    #make a worker pool of 2 threads
    p = Pool(2)
    #this list is input to our serc function as discussed Zero and One
    l = [0,1]
    #maps the input to the serc function
    p.map(serc,l)
