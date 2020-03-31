from bs4 import BeautifulSoup

f = open('pcNumberModalprettify.html','rb') 
soup = BeautifulSoup(f,'html.parser')
table = soup.find(id="grdHierarchy")

rows = table.findAll(True, {'class':['gridRowOdd', 'gridRowEven']})

pcNumbers = []

for index in range(len(rows)):
    dataCell = rows[index].find(class_='gridCell')
    pcNumbers.insert(index, dataCell.text.strip())
    print(pcNumbers[index])
