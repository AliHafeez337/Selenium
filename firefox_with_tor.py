
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument('--headless')

profile = webdriver.FirefoxProfile()
# Set proxy settings to manual
profile.set_preference('network.proxy.type', 1)
# Set proxy to Tor client on localhost
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9050)
# Disable all images from loading, speeds page loading
# http://kb.mozillazine.org/Permissions.default.image
profile.set_preference('permissions.default.image', 2)
# Set all new windows to open in the current window instead
profile.set_preference('browser.link.open_newwindow', 1)
# profile.update_preferences()

driver = webdriver.Firefox(profile, options = options)
# driver = webdriver.Firefox(profile)


driver.get('https://mylocation.org/')
txt = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div[1]/table/tbody/tr[4]/td[2]').text

print('Your location is in: ' + txt)

driver.close()