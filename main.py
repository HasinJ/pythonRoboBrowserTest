
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
#keyReports = driver.find_element_by_id('Node_1004552_')Node_1004555_ Node_1018704_0 347884
#keyReports.send_keys(Keys.ENTER)


productMixReport = wait.until(EC.presence_of_element_located((By.ID, "Node_1018703_0")))

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

busUnit = driver.find_element_by_id('__lufBusUnit')
busUnit.clear()
time.sleep(1)
busUnit.send_keys('347884')
busUnit.send_keys(Keys.ENTER)

dateUnit = driver.find_element_by_id('lkupDates')
dateUnit.clear()
dateUnit.send_keys('text to prompt dialog box')
time.sleep(1)
dateUnit.send_keys(Keys.ENTER)
time.sleep(3)



main_page = driver.current_window_handle

handles = driver.window_handles

# print the window_handle length
print(len(handles))

popup_window_handle = None
# loop through the window handles and find the popup window.
for handle in driver.window_handles:
    if handle != main_page:
        print(handle)
        popup_window_handle = handle
        break
# switch to the popup window.
driver.switch_to.window(popup_window_handle)

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
#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='btn btn-primary' and @id='YesBtn']")))


#submit = driver.find_element_by_id('wrLHSalesMixCon__AutoRunReport')
#ActionChains(driver).move_to_element(submit).click(submit).perform()
#time.sleep(1)

#print(driver.window_handles)
#actions = ActionChains(driver)
#actions.send_keys(Keys.TAB).perform()
#time.sleep(1)

#wait = WebDriverWait(driver,30)
#time.sleep(5)
#print(driver.page_source)
#frame = wait.until(EC.presence_of_element_located((By.ID, "renderFrame")))
#driver.switch_to.frame(frame)
#actions.send_keys(Keys.ENTER).perform()
#time.sleep(1)
#actions.move_to_element(submit).click(submit).perform()


time.sleep(5)
print(driver.page_source)






#window.top.ShowMenu(!window.top.bMenuVisible);
