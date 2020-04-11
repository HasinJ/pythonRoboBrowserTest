
def switchHandle(currentDriver):
    main_page = currentDriver.current_window_handle

    handles = currentDriver.window_handles

    # print the window_handle length
    print(f'{len(handles)}' + ' handles located... switching windows...')

    popup_window_handle = None
    # loop through the window handles and find the popup window.
    for handle in currentDriver.window_handles:
        if handle != main_page:
            popup_window_handle = handle
            break
    # switch to the popup window.
    currentDriver.switch_to.window(popup_window_handle)
    return main_page

def backToReportOptions(currentDriver, main, closeID='nothing', waitingTime=10):
    print('Switching driver focus back to report options...')
    #click on save and close
    if closeID != 'nothing':
        wait = WebDriverWait(currentDriver,waitingTime)
        saveANDclose = wait.until(EC.presence_of_element_located((By.ID, closeID)))
        saveANDclose.send_keys(Keys.ENTER)

    #go back to previous screen/frame
    currentDriver.switch_to.window(main)
    currentDriver.switch_to.default_content()

    wait = WebDriverWait(currentDriver,waitingTime)
    frame = wait.until(EC.presence_of_element_located((By.ID, "fraContent"))) #stays the same in report options screen
    currentDriver.switch_to.frame(frame)

    wait = WebDriverWait(currentDriver,waitingTime)
    frame = wait.until(EC.presence_of_element_located((By.ID, "Frame2"))) #stays the same in report options screen
    currentDriver.switch_to.frame(frame)


from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import config
import os
import os.path as path
import math
from scrapeHTML import scrape
import datetime

dateToday = datetime.datetime.now().strftime('%x') #local version of date
year = datetime.datetime.now().strftime('%Y')
dateToday = dateToday[:6] + year #adds the year in full, "2021" instead of "21"
dateDotNotation = dateToday.replace('/', '.')
print(dateToday)


waitTime = 10 #seconds
totalIDs = 0
dir = fr'C:\Users\Hasin Choudhury\Desktop\pythonSeleniumRadiant'

driver = webdriver.Ie(r"H:\IEDriver\IEDriverServer.exe")
wait = WebDriverWait(driver,waitTime)

driver.get('https://adqsr.radiantenterprise.com/bin/orf.dll/PE.platformForms.login.select.1.ghtm')

username = driver.find_element_by_id("weMemberId")
password = driver.find_element_by_id("pwd")

username.send_keys(config.radUser)
password.send_keys(config.radPass)

continueBtn = driver.find_element_by_id("waLogin")
continueBtn.send_keys(Keys.ENTER)

continueBtn = driver.find_element_by_id('waContinue')
continueBtn.send_keys(Keys.ENTER)

#frame = driver.find_element_by_id('MenuFrame')
time.sleep(3)
frame = wait.until(EC.presence_of_element_located((By.ID, "MenuFrame")))
driver.switch_to.frame(frame)

wait = WebDriverWait(driver,waitTime)
productMixReport = wait.until(EC.element_to_be_clickable((By.ID, "Node_1018704_0")))
ActionChains(driver).move_to_element(productMixReport).click(productMixReport).perform()

driver.switch_to.default_content()

wait = WebDriverWait(driver,waitTime)
frame = wait.until(EC.presence_of_element_located((By.ID, "fraContent")))
driver.switch_to.frame(frame)

wait = WebDriverWait(driver,waitTime)
frame = wait.until(EC.presence_of_element_located((By.ID, "Frame2")))
driver.switch_to.frame(frame)

orgUnit = wait.until(EC.presence_of_element_located((By.ID, "__selOrgUnit")))
orgUnit.clear()
time.sleep(1)
orgUnit.send_keys('Business Unit')
time.sleep(1)
orgUnit.send_keys(Keys.ENTER)
time.sleep(1)
orgUnit.send_keys(Keys.DOWN)
time.sleep(1)
orgUnit.send_keys(Keys.ENTER)
time.sleep(1)
orgUnit.send_keys(Keys.ENTER)

#pcNumber selection
busUnit = wait.until(EC.presence_of_element_located((By.ID, "__lufBusUnit")))
busUnit.clear()
time.sleep(1)
busUnit.send_keys('text to prompt modal business unit box')
busUnit.send_keys(Keys.ENTER)
time.sleep(3)
main_page = switchHandle(driver)

wait = WebDriverWait(driver, waitTime)
frame = wait.until(EC.presence_of_element_located((By.ID, 'renderFrame'))) #frame inside the modal box
driver.switch_to.frame(frame)
time.sleep(2)

#BeautifulSoup parse
soup = BeautifulSoup(driver.page_source,'html.parser')
table = soup.find(id="grdHierarchy")

rows = table.findAll(True, {'class':['gridRowOdd', 'gridRowEven']})

pcNumbers = []

for index in range(len(rows)):
    dataCell = rows[index].find(class_='gridCell')
    pcNumbers.insert(index, dataCell.text.strip())

if len(rows) == len(pcNumbers):
    time.sleep(1)

odd = driver.find_elements_by_class_name('gridRowOdd')
even = driver.find_elements_by_class_name('gridRowEven')
oddCount = 0
evenCount = 0
webElements = even + odd

#test = wait.until(EC.element_to_be_clickable((By.ID, f"{even[0]}")))
#print(even[0])

time.sleep(1)

for webElementsIndex in range(len(webElements)):
    somePCNumber = webElements[webElementsIndex].find_element_by_class_name('gridCell').find_element_by_tag_name('span').get_attribute("innerHTML")
    if somePCNumber != pcNumbers[0]:
        continue
    elif somePCNumber == pcNumbers[0]:
        firstPCNumber = webElements[webElementsIndex]
        print(somePCNumber + ' is the first PC number AKA Business Unit')
        pcNumbers.remove(somePCNumber)
        oddCount = 1
        break

ActionChains(driver).move_to_element(firstPCNumber).click(firstPCNumber).perform()
backToReportOptions(driver, main_page)


#date selection
dateUnit = wait.until(EC.presence_of_element_located((By.ID, "lkupDates")))
dateUnit.clear()
dateUnit.send_keys('text to prompt modal date box')
time.sleep(1)
dateUnit.send_keys(Keys.ENTER)
time.sleep(3)

main_page = switchHandle(driver)

wait = WebDriverWait(driver, waitTime)
frame = wait.until(EC.presence_of_element_located((By.ID, 'renderFrame'))) #frame inside the modal box
driver.switch_to.frame(frame)
time.sleep(1)

#5 tabs, 3 from close
for i in range(5):
    ActionChains(driver).send_keys(Keys.TAB).perform()
    time.sleep(0.5)

ActionChains(driver).send_keys(Keys.DELETE).perform()
ActionChains(driver).send_keys(dateToday).perform()
time.sleep(0.5)
ActionChains(driver).send_keys(Keys.TAB).perform()
ActionChains(driver).send_keys(Keys.DELETE).perform()
ActionChains(driver).send_keys(dateToday).perform()

backToReportOptions(driver, main_page, 'waSaveClose')

#remember we want to try to put them all in at once!
wait = WebDriverWait(driver,waitTime)
submit = wait.until(EC.presence_of_element_located((By.ID, 'wrLHSalesMixCon__AutoRunReport')))
ActionChains(driver).move_to_element(submit).click(submit).perform()

#parse table HTML into a file
if path.isdir(dir + fr'\Reports\{somePCNumber}')==False:
    os.mkdir(dir + fr'\Reports\{somePCNumber}')

with open(dir + fr'\Reports\{somePCNumber}\{dateDotNotation}Report.html','w') as f:
    f.write(driver.page_source)

totalIDs += scrape(dateDotNotation,somePCNumber,dir)
print(f'{somePCNumber}' + ' HTML recorded.')

#the loop after the first one is parsed
for index in range(len(pcNumbers)):
    wait = WebDriverWait(driver,waitTime)
    options = wait.until(EC.presence_of_element_located((By.ID, 'wrLHSalesMixCon__Options')))
    ActionChains(driver).move_to_element(options).click(options).perform()
    time.sleep(1)
    busUnit = wait.until(EC.presence_of_element_located((By.ID, "__lufBusUnit")))
    busUnit.click()
    busUnit.send_keys(Keys.DELETE)
    busUnit.send_keys(pcNumbers[index])
    busUnit.send_keys(Keys.ENTER)

    #goes to frame
    time.sleep(2)
    main_page = switchHandle(driver)
    wait = WebDriverWait(driver, waitTime)
    frame = wait.until(EC.presence_of_element_located((By.ID, 'renderFrame'))) #frame inside the modal box
    driver.switch_to.frame(frame)


    #stuff done while in frame
    time.sleep(1)
    even = driver.find_elements_by_class_name('gridRowEven')
    odd = driver.find_elements_by_class_name('gridRowOdd')
    if len(even)+len(odd) == len(pcNumbers)-1:
        print('row count matches!')

    if index/2 == math.floor(index/2):
        print('even...')
        ActionChains(driver).move_to_element(even[evenCount]).click(even[evenCount]).perform()
        evenCount += 1

    elif index/2 != math.floor(index/2):
        print('odd...')
        ActionChains(driver).move_to_element(odd[oddCount]).click(odd[oddCount]).perform()
        oddCount += 1


    #goes back after clicking on correct pcNumber
    backToReportOptions(driver, main_page)
    wait = WebDriverWait(driver,waitTime)
    submit = wait.until(EC.presence_of_element_located((By.ID, 'wrLHSalesMixCon__AutoRunReport')))
    ActionChains(driver).move_to_element(submit).click(submit).perform()

    time.sleep(5)

    if path.isdir(dir + fr'\Reports\{pcNumbers[index]}')==False:
        os.mkdir(dir + fr'\Reports\{pcNumbers[index]}')
    with open(dir + fr'\Reports\{pcNumbers[index]}\{dateDotNotation}Report.html','w') as f:
        f.write(driver.page_source)
    print(f'{pcNumbers[index]}' + ' HTML recorded.')
    totalIDs += scrape(dateDotNotation,pcNumbers[index],dir)

print('last ID should be: ' + f'{totalIDs}')
time.sleep(1)
driver.quit()
#time.sleep(5)
