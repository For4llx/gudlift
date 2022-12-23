from selenium import webdriver
import time
URL = 'http://127.0.0.1:5000'
email = 'john@simplylift.co'
competition = 'Spring Festival'
browser = webdriver.Firefox()
browser.get(URL)
found_email = browser.find_element(by='id', value='email')
found_email.clear()
found_email.send_keys(email)
found_email.submit()
browser.close()