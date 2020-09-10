from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.firefox.options import Options
import re

options = Options()
options.headless = True

browser = webdriver.Firefox(
    options=options
)  # replace with .Chrome() .Firefox(), or with the browser of your choice
login_url = "http://lamp1.ad.nswcsystems.co.uk/DVWA/login.php"
browser.get(login_url)  # navigate to the page
username = browser.find_element_by_name("username")  # username form field

password = browser.find_element_by_name("password")  # password form field
username.send_keys("admin")
password.send_keys("password")
submitButton = browser.find_element_by_name("Login")
submitButton.click()
xss_dom_url = (
    "http://lamp1.ad.nswcsystems.co.uk/DVWA/vulnerabilities/xss_d/?default=English#1234"
)

time.sleep(1)
browser.get("http://lamp1.ad.nswcsystems.co.uk/DVWA/security.php")
# securityLevel = browser.get_cookie('security')
# print(securityLevel)

cookie = {
    "name": "security",
    "value": "low",
    "path": "/DVWA/",
    "domain": "lamp1.ad.nswcsystems.co.uk",
    "secure": False,
    "httpOnly": True,
}

browser.add_cookie(cookie)
# securityLevel = browser.get_cookie('security')
# print(securityLevel)
browser.get(xss_dom_url)  # navigate to the page
innerHTML = browser.execute_script(
    "return document.body.innerHTML"
)  # returns the inner HTML as a string
soup_from_selenium = BeautifulSoup(innerHTML, "html.parser")
xss_string = re.compile(r"^.*#1234.*$", re.M)
for i in soup_from_selenium:  # .findAll(text=re.compile('#1234')):
    m = xss_string.search(str(i))
    if m:
        print(m.group(0).strip())
        print("DOM based XSS is found")
