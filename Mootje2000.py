#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymongo
client = pymongo.MongoClient("mongodb://mootje:mootje2000@82.217.36.166/properties") # defaults to port 27017
db=client.properties
col=db.ids
col_remaining=db.remaining_ids


# In[4]:


import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

chromedriver_location = "E:\Projects\project - company\Mootje2000\chromedriver"

remaining_ids=col_remaining.find()
arr = []
url = ''
temp = ''
loop = 0
for i in remaining_ids:
#     print('if runs')
    loop += 1
    if i['ids']!= None:
        col_remaining.delete_one({"_id":i['_id']})
        arr=i['ids'].copy()
        temp = i["name"]
        url=i['search_url']
        
    break
        
if (loop == 0):
#     print('else runs')
    docs=col.find()
    list_=[]
    for i in docs:
        list_.append(i)
#     print(list_[-1])
    s=list_[-1]
    start=s["starting_ids"]
#     print(start)
    end=s["ending_ids"]
    url=s["search_url"]
    range1=s["query"]

    arr = []
    idInput = ''
    # range1 = 50
    no = 0
    inserted = 0
    if (end > start):
        rang = len(range(end-start))+1
        for i in (range(rang)):
            no = i
            if (inserted >= range1):
    #             print('naye',arr)
                idInput = idInput[:-1]

#                 print(idInput)
    #             str1 = ','.join(str(e) for e in arr)
    #             print(str1)
                arr.append(idInput)
    #             print(arr)
                idInput = ''
                inserted = 0
    #             print(arr, no+start, end)
                if (no+start < end+1):
                    idInput = idInput + str(no+start) + ','
    #                 print(idInput)
                    inserted += 1
                    if(no+start == end):
                        idInput = idInput[:-1]

                        arr.append(idInput)
                        idInput = ''
                        inserted = 0
    #                     print(arr, no+start, end)
            else:
    #             print('eys',arr)
                idInput = idInput + str(no+start) + ','
    #             print(idInput)
                inserted += 1
                if(no+start == end):
                    idInput = idInput[:-1]
                    arr.append(idInput)
                    idInput = ''
                    inserted = 0
#     print(arr)
    temp = s["name"]




remaining=arr.copy()

colSave=db[temp]

# print(arr)
print("Starting crawling...")
for i in arr:

    print("Crawling for ids: "+i)
    try: 
        
#         if (arr.index(i) == 1):
#             print(1/0)
            
        driver = webdriver.Chrome(chromedriver_location, options=options)
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
        
#         print(i)
#         print(arr.index(i))
        remaining.pop(0)
        if (arr.index(i) > 0):
            #delete remaining
            try:
                col_remaining.delete_one({"_id":1000})
            except:
                pass
        if (arr.index(i) < len(arr)):
            #save remaining
            remainig_save={ "_id": 1000, "ids":remaining,"search_url":url,"name":temp}
            print("Progress Saved...")
            col_remaining.insert_one(remainig_save)
        
#         print(arr,copy)
    except:
        
        try:
            col_remaining.delete_one({"_id":1000})
        except:
            pass
        remainig_save={"ids":remaining,"search_url":url,"name":temp}
        print("We encountered an error, but we saved the remaining record to be crawled, please rerun the program...")
        col_remaining.insert_one(remainig_save)
        break

try:
    col_remaining.delete_one({"_id":1000})
except:
    pass
print("Crawling done...")


# In[ ]:





# In[ ]:




