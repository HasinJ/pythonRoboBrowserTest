from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from scrapeHTML import scrape
import time
import config
import os
import os.path as path
import math
import sqlQueries
import datetime
from dateutil.relativedelta import relativedelta


#functions
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

def get_past_date(str_days_ago):
    TODAY = datetime.date.today()
    splitted = str_days_ago.split()
    if len(splitted) == 1 and splitted[0].lower() == 'today':
        return TODAY
    elif len(splitted) == 1 and splitted[0].lower() == 'yesterday':
        date = TODAY - relativedelta(days=1)
        return date
    else:
        return "Wrong Argument format"

def dateConversions(self,fromDate='empty'):
    global dateToday, dateDotNotation

    hour = int(self.datetime.now().strftime('%H'))

    if fromDate!='empty':
        selectedDate=self.date(fromDate['year'], fromDate['month'], fromDate['day'])

    elif hour >= 23: #the half of the day
        selectedDate = get_past_date('today')
        print("use today's date")

    elif hour < 23: #the other half of the day
        selectedDate = get_past_date('yesterday')
        print("use yesterday's date")

    dateToday = selectedDate.strftime('%x') #local version of date 12/31/2020
    monthLong = selectedDate.strftime('%B') #December
    DOW = selectedDate.strftime('%a') #Wed
    day = selectedDate.strftime('%d') #31
    year = selectedDate.strftime('%Y') #2020
    dayofyear = selectedDate.strftime('%j') #356

    dateToday = dateToday[:6] + year #adds the year in full, "2021" instead of "21"
    dateDotNotation = dateToday.replace('/', '.')
    print(dateToday) #12/31/2020

    #Datesql, DOW, TOD, Month, Day, Year
    selectedDate = str(selectedDate.isoformat()) #2020-12-31
    sqlDates = [selectedDate,DOW,'',monthLong,day,year,dayofyear]

    delete = 0

    try:
        sqlQueries.insertDatePK(sqlDates)
    except sqlQueries.MySQLdb._exceptions.IntegrityError:
        print('Date already exists in DateTBL.. deleting date and truncating TempTable')
        sqlQueries.oneFile('Temp','TempTable Truncate.txt')
        delete=1

    if delete==1:
        sqlQueries.deleteDay(selectedDate)
        sqlQueries.insertDatePK(sqlDates)
        print('Done. \n ')
#end

sqlQueries.oneFile('Temp','TempTable Truncate.txt')


time.sleep(1)
dateConversions(datetime) #can also be used for one day format: dateConversions(datetime, {'year':number, 'month':number, 'day':number}) day shouldnt have zero
sqlQueries.oneFile('Temp','TempTable Truncate.txt')


#important variables
waitTime = 10 #seconds
totalIDs = 0
driver = webdriver.Ie(r"C:\Program Files (x86)\IEDriver\IEDriverServer.exe")
wait = WebDriverWait(driver,waitTime)
oddCount = 0
evenCount = 0


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
busUnit.send_keys('text')
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
dateUnit.send_keys('text')
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
ActionChains(driver).send_keys(dateToday).perform() #from (dateToday)
time.sleep(0.5)
ActionChains(driver).send_keys(Keys.TAB).perform()
ActionChains(driver).send_keys(Keys.DELETE).perform()
ActionChains(driver).send_keys(dateToday).perform() #to (dateToday)

backToReportOptions(driver, main_page, 'waSaveClose')

#remember we want to try to put them all in at once!
wait = WebDriverWait(driver,waitTime)
submit = wait.until(EC.presence_of_element_located((By.ID, 'wrLHSalesMixCon__AutoRunReport')))
ActionChains(driver).move_to_element(submit).click(submit).perform()


#parse table HTML into a file
if path.isdir(config.dir + fr'\Reports')==False:
    os.mkdir(config.dir + fr'\Reports')

if path.isdir(config.dir + fr'\Reports\{somePCNumber}')==False:
    os.mkdir(config.dir + fr'\Reports\{somePCNumber}')

with open(config.dir + fr'\Reports\{somePCNumber}\{dateDotNotation}Report.html','w') as f:
    f.write(driver.page_source)

totalIDs += scrape(dateDotNotation,somePCNumber,config.dir)
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

    if path.isdir(config.dir + fr'\Reports\{pcNumbers[index]}')==False:
        os.mkdir(config.dir + fr'\Reports\{pcNumbers[index]}')
    with open(config.dir + fr'\Reports\{pcNumbers[index]}\{dateDotNotation}Report.html','w') as f:
        f.write(driver.page_source)
    print(f'{pcNumbers[index]}' + ' HTML recorded.')
    totalIDs += scrape(dateDotNotation,pcNumbers[index],config.dir)

print('last ID should be: ' + f'{totalIDs}')
time.sleep(1)
driver.quit()


print('moving from temp table in..')
time.sleep(1)
print('3')
time.sleep(1)
print('2')
time.sleep(1)
print('1')
time.sleep(1)
sqlQueries.moveAllTempSQL()
print('success! \n \n Emptying TempTable...')
sqlQueries.oneFile('Temp','TempTable Truncate.txt')
print("done!")
time.sleep(1)


#sqlQueries.moveOneTempSQL('BagelTBL')
#sqlQueries.moveOneTempSQL('BakeryTBL')
#sqlQueries.moveOneTempSQL('ColdBeverageTBL')
#sqlQueries.moveOneTempSQL('FrozenTBL')
#sqlQueries.moveOneTempSQL('HotBeverageTBL')
#sqlQueries.moveOneTempSQL('SandwichTBL')
#time.sleep(5)
