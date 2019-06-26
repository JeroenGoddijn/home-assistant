# author: Jeroen Goddijn
# code: https://github.com/JeroenGoddijn/home-assistant/tree/dev/homeassistant/components/usps
# blog: http://mrgoddijn.com
# MIT License

# ------------------------------------------
#      Web Scraping USPS Informed Delivery  
# ------------------------------------------

'''
requests
BeautifulSoup
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
Installing Beautiful Soup
pip install beautifulsoup4
Linux: apt-get install python3-bs4
'''

import requests
from bs4 import BeautifulSoup
import re

# Global variables
MAIN_LOGIN_URL = "https://reg.usps.com/entreg/LoginAction_input?app=Phoenix&appURL=https://informeddelivery.usps.com"
SIGNIN_URL = "https://reg.usps.com/entreg/json/AuthenticateAction"
RESTART_URL = "https://informeddelivery.usps.com/box/pages/intro/start.action?restart=1"
LOGGEDIN_URL = "https://informeddelivery.usps.com/box/pages/secure/DashboardAction_input.action?selectedDate=06%2F24%2F2019"
SESSION_REFRESH_URL = "https://reg.usps.com/entreg/secure/SessionRefreshAction"
# ALTERNATIVE SESSION_REFRESH_URL if above one is not working: https://informeddelivery.usps.com/box/pages/secure/ajax/SessionPinger.action
## Mailpieces elements
MAIN_MAILPIECES_DIV = 'find_all(id="CP_nontracked")'
# MAILPIECE_DETAIL_DIV = <div class="mailDashContainer" align="center">
EACH_MAILPIECE_DIV = 'find_all("div", "mailpiece")'
MAILPIECE_IMAGE_URL = "https://informeddelivery.usps.com/box/pages/secure/"

## Packages elements
MAIN_PACKAGES_DIV = 'find_all(id="CP_tracked")'
# PACKAGES_DETAIL_DIV = <div class="packageContainer">
# EACH_PACKAGE_DIV = <div class="pack_row">

# User Credentials
USER_USERNAME = "Mariniertje"
USER_PWD = "Marnalg13"

# Now, let's start a session to be able to re-use and cookie persistence
s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
# Now, let's try to get the login page
r = s.get(MAIN_LOGIN_URL)
r

print(r.url)
print(r.status_code)
print(s.cookies)

soup = BeautifulSoup(r.content)

login_form = soup.find_all(id='loginForm')
# print(login_form)

TOKEN_NAME = soup.find('input', {'name':'struts.token.name'})['value']
print(TOKEN_NAME)

TOKEN = soup.find('input', {'name':'token'})['value']
print(TOKEN)

# Let's build the Login Payload
LOGIN_PAYLOAD = "struts.token.name=" + TOKEN_NAME + "&token=" + TOKEN +"&route=&username=" + USER_USERNAME + "&password=" + USER_PWD + "%40&newPassword=&retypeNewPassword="

# Now, let's sign in to Informed Delivery
r2 = s.post(SIGNIN_URL, params=LOGIN_PAYLOAD, cookies=s.cookies)
print(r2.status_code)
print(r2.url)
# print(r2.content)
# print(s.cookies)

# r3 = s.post("https://informeddelivery.usps.com/box/pages/secure/DashboardAction_input.action?restart=1", cookies=s.cookies)
# print(r3.status_code)
# print(r3.url)
# print(r3.content)


# ------------------------------------------
#      Let's find the number of mailpieces to be delivered on this date  
# ------------------------------------------

## All Mailpieces are shown within this main DIV with id="CP_nontracked"
s.get(SESSION_REFRESH_URL)
r4 = s.get(LOGGEDIN_URL, cookies=s.cookies)
dashboard_soup = BeautifulSoup(r4.content)
# print(dashboard_soup)

mail_pieces = dashboard_soup.find_all("div", "mailpiece")
number_mail_pieces = len(mail_pieces)
print("You'll receive " + str(number_mail_pieces) + " mail pieces today")
## Getting the images for each mailpiece now
mailpiece_images = dashboard_soup.find_all("img", "mailpieceIMG", "src")
print (len(mailpiece_images))
for image in mailpiece_images:
    #get the relative src path
    print (image['src'])
    #get the actual mailpiece image ID number
    image_id_start = image['src'].find('?id=') + 4
    print (image['src'][image_id_start:])
    image_id = image['src'][image_id_start:]
    #build mailpiece image url
    image_url = MAILPIECE_IMAGE_URL + image['src']
    print(image_url)
    #save each image to local disk
    r_image = s.get(image_url)
    print (r_image)
    with open("tmp/" + image_id + ".jpg", "wb") as f:
        f.write(r_image.content)
# print (mailpiece_images)

 

# ------------------------------------------
#      Let's find the number of pacakges to be delivered on this date  
# ------------------------------------------

## All Pacakges are shown within this main DIV with <div class="pack_row">"
# We will re-use the dashboard-soup collected for the mailpieces, since all this data is available on the same HTML page
packages = dashboard_soup.find_all("div", "pack_row")
number_packages = len(packages)
print("You'll receive " + str(number_packages) + " packages today")