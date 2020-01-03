#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from os.path import exists
from os import makedirs, chdir
from selenium import webdriver
import time
import numpy as np
from getpass import getuser
from win10toast import ToastNotifier as toast


# In[ ]:

'''A path to store the previous data'''
track={}
if not exists("C://Users/"+str(getuser())+"/Documents/price_tracker/"):
    chdir("C://Users/"+str(getuser())+"/Documents/")
    makedirs("price_tracker")
    track = {}
    np.save('data.npy',track)
else:
    chdir("C://Users/"+str(getuser())+"/Documents/price_tracker/")
    

def execute(website,interval):
    chrome_options = webdriver.ChromeOptions()
    n = toast()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome('F://chromedriver_win32/chromedriver.exe',chrome_options=chrome_options)
    browser.get(website)
    


        
    print('Please wait while the website loads')
    time.sleep(1) #time to allow the website to load
    #price = browser.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[3]/div/div[4]/div[1]/div/div[1]')
    price =browser.find_element_by_class_name('_1vC4OE._3qQ9m1')
    price = price.text[1:]
    price = price_in_int(price)
    track = np.load('data.npy',allow_pickle='TRUE').item()
    previous_price=999999999
    if website in track.keys():
        previous_price = track[website]
    else:
        track[website]= price
    if(previous_price>price):
        print('Whow! There is a price drop!! from '+str(previous_price)+' to '+str(price))
        n.show_toast("There is a price drop!",icon='icon.ico',duration=12)  # You need to place an icon.ico in the same folder
    elif(previous_price==price):
              print('The price is still the same')
    else:
              print('Price increase')
    np.save('data.npy',track)
    browser.quit()
    time.sleep(interval)
    execute(website)
    
        
    
    
def price_in_int(price):
    n=''
    for i in price:
        if i.isdigit():
            n+=i
    return (int(n))


# In[ ]:


def checker():
    try:
        inp = input('Please copy paste the web address here: ')
        print('The default checking interval is 60min if you want to change input time in minutes below or just hit ENTER')
        interval = (input())
        time = 3600
        if(interval!=''):
            time=int(interval)*60
        execute(inp,time)
    except:
        print('OOOPS! looks like you entered something wrong... try again or contact the developer.')


# In[ ]:


if __name__ == "__main__":
    checker()


