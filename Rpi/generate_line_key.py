from getpass import getpass

import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

# account = input("Account: ")
# password = getpass()
account = "ponywang10@gmail.com"
password = "Pony910506"

driver = webdriver.Chrome()
driver.get('https://notify-bot.line.me/en/')

loginPageLink = driver.find_element(By.LINK_TEXT,"Log in")
loginUrl = loginPageLink.get_attribute('href')
driver.get(loginUrl)
driver.implicitly_wait(10)

account_blank = driver.find_element(By.NAME,"tid")
password_blank = driver.find_element(By.NAME,"tpasswd")

account_blank.send_keys(account)
password_blank.send_keys(password)

login_btn = driver.find_element(By.CLASS_NAME,"MdBtn01")
login_btn.click()

driver.implicitly_wait(10)

checkNumber = driver.find_element(By.CLASS_NAME,"mdMN06Number")
print("Please open your Line app and input {} to verify your account".format(checkNumber.text))

toContinue = input("press enter if you've checked your login")

driver.get('https://notify-bot.line.me/my/')

getKeyLink = driver.find_element(By.LINK_TEXT,"發行權杖")
getKeyLink.click()

driver.implicitly_wait(10)


keyName = "line_notify"

keyName_blank = driver.find_element(By.XPATH,"//div[@class='MdInputTxt01']/input[1]")
keyName_blank.send_keys(keyName)

chatroom = driver.find_element(By.XPATH,"//li[@class='mdMN04Li']")
chatroom.click()

WebDriverWait(driver,10)

input("Press enter to continue")


try:
    generateToken_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME,"MdBtn01P01"))
    )
finally:
    driver.quit()

generateToken_btn.click()

WebDriverWait(driver,10)

lineKey_blank = driver.find_element(By.XPATH,"//div[@class='MdInputTxt01 mdInputTxt01Read']/input[1]")
print(lineKey_blank.get_attribute("value"))


# toContinue = input("Press enter to continue")

# driver.close()




