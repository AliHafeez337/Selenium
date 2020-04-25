#!/usr/bin/env python
# coding: utf-8

# In[50]:

import os 
os.environ["LANG"] = "en_US.UTF-8"

import pymongo
client = pymongo.MongoClient("mongodb://mootje:mootje2000@82.217.36.166/properties") # defaults to port 27017
db=client.properties
col=db.ids
col_remaining=db.remaining_ids


# In[62]:


import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")


# In[78]:

print("Please wait while we divide the ids...")


remaining_ids=col_remaining.find()
arr = []
url = ''
temp = ''
loop = 0
crawled = 0
for i in remaining_ids:
#     print('if runs')
    loop += 1
    if i['name']!= None:
        col_remaining.delete_one({"_id":i['_id']})
        
        crawled = i['crawled']
        temp = i["name"]
        url=i['search_url']
        start = i['start']
        end = i["end"]
        range1 = i["query"]
        
    break
        
if (loop == 0):
#     print('else runs')
    docs=col.find()
    list_=[]
    for i in docs:
        list_.append(i)
    s=list_[-1]
    start=s["starting_ids"]
    end=s["ending_ids"]
    url=s["search_url"]
    range1=s["query"]
    temp = s["name"]

arr = []
idInput = ''
no = 0
inserted = 0
if (end > start):
    rang = len(range(end-start))+1
    for i in (range(rang)):
        no = i
        if (inserted >= range1):
            idInput = idInput[:-1]

            arr.append(idInput)
            idInput = ''
            inserted = 0

            if (no+start < end+1):
                idInput = idInput + str(no+start) + ','

                inserted += 1
                if(no+start == end):
                    idInput = idInput[:-1]

                    arr.append(idInput)
                    idInput = ''
                    inserted = 0

        else:

            idInput = idInput + str(no+start) + ','

            inserted += 1
            if(no+start == end):
                idInput = idInput[:-1]
                arr.append(idInput)
                idInput = ''
                inserted = 0

colSave=db[temp]

# print(crawled)
if (loop > 0):
    arr = arr[crawled:]


# In[79]:


# print(arr[-100::])
# print(arr)


# In[80]:


# save starting, ending, query, url and name in remaining

print("Starting crawling...")

driver = webdriver.Chrome('/home/ali/Desktop/Scrapping/chromedriver', options = options)

indexDone = 0
for index, i in enumerate(arr):
#     print(index)

    print("Crawling for ids: "+i)
    try: 
        
#         if (index == 2):
#             print(1/0)
            
        driver.get(url)
        input_field='//*[@id="objectIds"]'
        driver.find_element_by_xpath(input_field).send_keys(i)
        select_box='//*[@id="f"]/option[2]'
        driver.find_element_by_xpath(select_box).click()
        get_json='/html/body/div/form/table/tbody/tr[36]/td/input[1]'
        driver.find_element_by_xpath(get_json).click()
        txt=driver.find_element_by_xpath("/html/body/pre").text
        data=json.loads(txt)
        
#         print(type(data))
        colSave.insert_one(data)
        indexDone += 1
        
#         print(i)
#         print(index)

        if (index > 0):
            #delete remaining
            try:
                col_remaining.delete_one({"_id":1000})
            except:
                pass
        if (index < len(arr)):
            #save remaining
            remainig_save={ "_id": 1000, "crawled": indexDone+crawled, "start": start, "end": end, "query": range1,"search_url":url,"name":temp}
            print("Progress Saved...")
            col_remaining.insert_one(remainig_save)
        
#         print(arr,copy)
    except:
        
        try:
            col_remaining.delete_one({"_id":1000})
        except:
            pass
        remainig_save={"start": start, "crawled": indexDone+crawled, "end": end, "query": range1, "name":temp, "search_url":url}
        col_remaining.insert_one(remainig_save)
        print("We encountered an error, but we saved the remaining record to be crawled, please rerun the program...")
        break

try:
    col_remaining.delete_one({"_id":1000})
except:
    pass

driver.close()
print("Crawling done...")


# In[28]:





# In[ ]:




