from bs4 import BeautifulSoup
import time

f = open('pcNumberModalprettify.html','rb')
soup = BeautifulSoup(f,'html.parser')
table = soup.find(id="grdHierarchy")

rows = table.findAll(True, {'class':['gridRowOdd', 'gridRowEven']})

pcNumbers = []

for index in range(len(rows)):
    dataCell = rows[index].find(class_='gridCell')
    pcNumbers.insert(index, dataCell.text.strip())
    print(pcNumbers[index])

if len(rows) == len(pcNumbers):
    time.sleep(1)
