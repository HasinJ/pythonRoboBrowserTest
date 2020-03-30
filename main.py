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


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

import config
driver = webdriver.Ie(r"H:\IEDriver\IEDriverServer.exe")
wait = WebDriverWait(driver,5)

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

wait = WebDriverWait(driver,30)
productMixReport = wait.until(EC.element_to_be_clickable((By.ID, "Node_1018703_0")))
ActionChains(driver).move_to_element(productMixReport).click(productMixReport).perform()

driver.switch_to.default_content()

wait = WebDriverWait(driver,30)
frame = wait.until(EC.presence_of_element_located((By.ID, "fraContent")))
driver.switch_to.frame(frame)

wait = WebDriverWait(driver,30)
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
busUnit.send_keys('text to prompt modal box') #temporary, needs to grab list
busUnit.send_keys(Keys.ENTER)
time.sleep(1)

#HTML parse and PC#-count-grab
#pcBtn = driver.find_element_by_id('__lufOrgUnit_image')
#pcBtn.send_keys(Keys.ENTER)
#time.sleep(3)
#main_page = switchHandle(driver)
#print(driver.page_source)

dateUnit = driver.find_element_by_id('lkupDates')
dateUnit.clear()
dateUnit.send_keys('text to prompt modal box')
time.sleep(1)
dateUnit.send_keys(Keys.ENTER)
time.sleep(3)



main_page = switchHandle(driver)




#frame switch to date frame
wait = WebDriverWait(driver,10)
frame = wait.until(EC.presence_of_element_located((By.ID, "renderFrame")))
driver.switch_to.frame(frame)

#click on save and close
wait = WebDriverWait(driver,10)
saveANDclose = wait.until(EC.presence_of_element_located((By.ID, 'waSaveClose')))
saveANDclose.send_keys(Keys.ENTER)

#go back to previous screen/frame
driver.switch_to.window(main_page)
driver.switch_to.default_content()

wait = WebDriverWait(driver,30)
frame = wait.until(EC.presence_of_element_located((By.ID, "fraContent")))
driver.switch_to.frame(frame)

wait = WebDriverWait(driver,30)
frame = wait.until(EC.presence_of_element_located((By.ID, "Frame2")))
driver.switch_to.frame(frame)

wait = WebDriverWait(driver,10)
submit = wait.until(EC.presence_of_element_located((By.ID, 'wrLHSalesMixCon__AutoRunReport')))
submit.send_keys(Keys.ENTER)

print(driver.page_source)
