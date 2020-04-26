#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

import os 
os.environ["LANG"] = "en_US.UTF-8"


# In[2]:



import pymongo
# client = pymongo.MongoClient("mongodb://mootje:mootje2000@82.217.36.166/properties") # defaults to port 27017
client = pymongo.MongoClient("mongodb://192.168.10.5:27017/temp")
db=client.temp
col=db.ids
col_remaining=db.remaining_ids


# In[26]:



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


# In[27]:



remaining_ids=col_remaining.find()
arr = []
url = ''
temp = ''
loop = 0
crawled = 0
deleteId = ''

for i in remaining_ids:
#     print('if runs')
    try:
        if i['name']!= None:
            loop += 1
            deleteId = i['_id']
            
            crawled = i['crawled']
            temp = i["name"]
            url=i['search_url']
            start = i['start']
            end = i["end"]
            range1 = i["query"]

            print("Running in pause mode... (i.e. Data is picked from the 'remaining_ids' collection.)\n")

    except:
        pass

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

    print("Running in fresh mode... (i.e. Data is picked from the 'ids' collection.)\n")

# In[28]:



print("Please wait while we divide the range into ids... This will take little longer for the large range.\n")

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


# In[29]:



if (loop > 0):
    arr = arr[crawled:]
# print(arr[-5:])


# In[30]:



print("Starting crawling...\n")

driver = webdriver.Chrome('/home/ali/Scrapping/chromedriver', options = options)

err = False
indexDone = 0
for index, i in enumerate(arr):
#     print(index)

    print("Crawling for ids: "+i)
    try: 
        
#         if (index == 1):
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
            if (index == 0):
                col_remaining.delete_one({"_id": deleteId})

            idsSaved = int(i.split(',')[:1:-1][0])
            idsRemain = end - idsSaved

            #save remaining
            remainig_save={ "_id": 1000, "idsSaved": idsSaved, "idsRemain": idsRemain, "crawled": indexDone+crawled, "start": start, "end": end, "query": range1,"search_url":url,"name":temp}
            print("Progress Saved...")
            col_remaining.insert_one(remainig_save)
        
#         print(arr,copy)
    except:
        err = True
        try:
            col_remaining.delete_one({"_id":1000})
        except:
            pass
        
        idsSaved = int(i.split(',')[:1:1][0])-1
        idsRemain = end - idsSaved

        remainig_save={"idsSaved": idsSaved, "idsRemain": idsRemain, "start": start, "crawled": indexDone+crawled, "end": end, "query": range1, "name":temp, "search_url":url}
        col_remaining.insert_one(remainig_save)
        print("We encountered an error, but we saved the remaining record to be crawled, please rerun the program...")
        break

try:
    col_remaining.delete_one({"_id":1000})
except:
    pass

driver.close()

if (not err):
    print("\nCrawling done...\n")


# In[15]:




