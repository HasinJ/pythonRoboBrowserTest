from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
browser = RoboBrowser(parser='html.parser')
browser.open('https://adqsr.radiantenterprise.com/bin/orf.dll/PE.platformForms.login.select.1.ghtm')

login_form = browser.get_form(id='theForm')

#tells us what HTML we're dealing with
print(login_form.parsed)
