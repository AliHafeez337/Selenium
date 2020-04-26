
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
options.add_argument('--proxy-server=socks5://127.0.0.1:9050')

driver = webdriver.Chrome('/home/ali/Desktop/Scrapping/chromedriver', options = options)
# driver = webdriver.Chrome('/home/ali/Desktop/Scrapping/chromedriver')

# driver.get('https://www.whatismyip.com/')
driver.get('https://whatismyipaddress.com/')
txt = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div[1]/div[3]/table/tbody/tr[2]/td').text
txt1 = driver.find_element_by_xpath('//*[@id="ipv6"]').text
if (txt1 == "Not detected"):
    print("Location: " + txt1)
elif (txt != ""):
    print("Your city is: " + txt)
else:
    print("Didn't get anything...")

# driver.close()