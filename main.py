def switchHandle(currentDriver):
    main_page = currentDriver.current_window_handle

    handles = currentDriver.window_handles

    # print the window_handle length
    print(len(handles))

    popup_window_handle = None
    # loop through the window handles and find the popup window.
    for handle in currentDriver.window_handles:
        if handle != main_page:
            print(handle)
            popup_window_handle = handle
            break
    # switch to the popup window.
    currentDriver.switch_to.window(popup_window_handle)
    return main_page

def backToReportOptions(currentDriver, switchFrameID, closeID, main, waitingTime=10,):
        wait = WebDriverWait(currentDriver, waitingTime)
        frame = wait.until(EC.presence_of_element_located((By.ID, switchFrameID))) #frame inside the modal box
        currentDriver.switch_to.frame(frame)

        #click on save and close
        wait = WebDriverWait(currentDriver,waitingTime)
        saveANDclose = wait.until(EC.presence_of_element_located((By.ID, closeID)))
        saveANDclose.send_keys(Keys.ENTER)

        #go back to previous screen/frame
        currentDriver.switch_to.window(main_page)
        currentDriver.switch_to.default_content()

        wait = WebDriverWait(currentDriver,waitingTime)
        frame = wait.until(EC.presence_of_element_located((By.ID, "fraContent"))) #stays the same in report options screen
        currentDriver.switch_to.frame(frame)

        wait = WebDriverWait(currentDriver,waitingTime)
        frame = wait.until(EC.presence_of_element_located((By.ID, "Frame2"))) #stays the same in report options screen
        currentDriver.switch_to.frame(frame)


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import config

waitTime = 10 #seconds


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
frame = wait.until(EC.presence_of_element_located((By.ID, "MenuFrame")))
driver.switch_to.frame(frame)

wait = WebDriverWait(driver,waitTime)
productMixReport = wait.until(EC.element_to_be_clickable((By.ID, "Node_1018703_0")))
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

busUnit = wait.until(EC.presence_of_element_located((By.ID, "__lufBusUnit")))
busUnit.clear()
time.sleep(1)
busUnit.send_keys('text to prompt modal business unit box')
busUnit.send_keys(Keys.ENTER)

#HTML parse and PC#-count-grab
#pcBtn = driver.find_element_by_id('__lufOrgUnit_image')
#pcBtn.send_keys(Keys.ENTER)
#time.sleep(3)
#main_page = switchHandle(driver)
#print(driver.page_source)

dateUnit = wait.until(EC.presence_of_element_located((By.ID, "lkupDates")))
dateUnit.clear()
dateUnit.send_keys('text to prompt modal date box')
time.sleep(1)
dateUnit.send_keys(Keys.ENTER)
time.sleep(3)



main_page = switchHandle(driver)


backToReportOptions(driver, 'renderFrame', 'waSaveClose', main_page)


wait = WebDriverWait(driver,waitTime)
submit = wait.until(EC.presence_of_element_located((By.ID, 'wrLHSalesMixCon__AutoRunReport')))
submit.send_keys(Keys.ENTER)

print(driver.page_source)