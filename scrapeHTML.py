def sliceString(string,beginStr,endStr='nothing'):
    startIndex = string.find(beginStr)+len(beginStr) #doesnt include beginStr
    if endStr=='nothing': #if there is no parameter for endStr
        return string[startIndex:]
    stopIndex = string.find(endStr,startIndex) #so it doesn't take beginStr into consideration, it solves the problem with having beginStr and endStr being the same string (like when finding pcNumber)
    output = string[startIndex:stopIndex]
    return output

import json
import pandas as pd
import os.path
import csv
import MySQLdb
from os import path
from bs4 import BeautifulSoup
from sqlQueries import connectDB

def scrape(dateDotNotation='04.02.2020',  pcNumber='347884', dir = fr'C:\Users\Hasin Choudhury\Desktop\pythonBeautifulSoupScrape'): #no driver.page_source because just in case we want to be able to run the code without selenium

    mydb = connectDB()
    cursor = mydb.cursor()

    f = open(dir + fr'\Reports\{pcNumber}\{dateDotNotation}Report.html','rb') # 'rb' stands for read-binary, write-binary needs chmoding, this also needs to be changed for Selenium (needs to have date)
    content = f.read()
    soup = BeautifulSoup(content,'html.parser')
    mainHeaderText = soup.find(id='MainReportDiv').text.strip().split('Time')[0]

    data = []
    columnNames = []
    dbTable = 'TempTable' #dont add spaces
    insert = f'INSERT INTO {dbTable} (`PC Number`,`Date`,' #one half
    values = ' VALUES (%s,%s,' #another half
    sql = ''
    date = ''
    pcNumber = ''


    #grabs first table since there are two tables and CSS
    table = soup.find(class_='TableStyle')

    #grabs business unit and then PC#
    businessUnit = sliceString(mainHeaderText,'Business Unit','-')
    pcNumber = sliceString(businessUnit,' ',' ')

    #grabs date
    businessDate = sliceString(mainHeaderText,'Date','Report')
    endDate = sliceString(businessDate,'Date')
    date = sliceString(endDate,' ')

    #strips of whitespaces AGAIN just incase
    date = date.strip()
    pcNumber = pcNumber.strip()

    #grabs count of the table without total rows
    dataRows = table.findAll(True, {'class':['RowStyleData', 'RowStyleDataEven']})

    #find (first) header row
    rowHead = table.find(class_="RowStyleHead")
    HTMLcolumns = rowHead.select('.CellStyle')
    for index in range(len(HTMLcolumns)):
        columnNames.insert(index, HTMLcolumns[index].text.strip())
        #sql also needs column names
        if index != (len(HTMLcolumns)-1): #if the index isn't the last column name, add a comma
            insert = insert + '`' + columnNames[index] + '`' + ','
            values = values + '%s,'
        elif index == (len(HTMLcolumns)-1): #if the index is the last column name, add a parenthesis
            insert = insert + '`' + columnNames[index] + '`' + ')'
            values = values + '%s)'


    #cleaning sql of '%' in the INSERT INTO sequence, otherwise SQL query fails
    insert = insert.replace('%', 'Percent')
    sql = insert + values

    #main data
    for count in range(len(dataRows)):
        dataCell = dict()
        dataCell['PC Number'] = pcNumber
        dataCell['Date'] = date
        for index in range(len(HTMLcolumns)):
            try:
                dataCell[columnNames[index]] = dataRows[count].select('.CellStyle')[index]['dval']
            except: #if there is no value, then the data cell has to represent the item name
                dataCell[columnNames[index]] = dataRows[count].select('.CellStyle')[index].text.strip()
        data.append(dataCell)

    columnNames.insert(0,'Date')
    columnNames.insert(0,'PC Number')
    f.close()


    #checks for .json existence
    if path.exists(dir + fr'\Reports\{pcNumber}\{dateDotNotation}Output.json')==False: #f-string to differentiate files, r-string to change the use of backslashes (for absolute path)
        with open(dir + fr'\Reports\{pcNumber}\{dateDotNotation}Output.json','w') as f:
            json.dump(data,f)

    #checks for dataframe export existence
    if path.exists(dir + fr'\Reports\{pcNumber}\{dateDotNotation}dataframe.csv')==False:
        df = pd.read_json(open(dir + fr'\Reports\{pcNumber}\{dateDotNotation}Output.json','r'))
        #df.set_index('PC Number', inplace=True) takes its own row
        #print(df)
        df.to_csv(dir + fr'\Reports\{pcNumber}\{dateDotNotation}dataframe.csv', index=False, header=True)


    csv_data = csv.reader(open(dir + fr'\Reports\{pcNumber}\{dateDotNotation}dataframe.csv'))
    next(csv_data) #to ignore header
    for row in csv_data:
       cursor.execute(sql, row)


    mydb.commit()
    print(date,pcNumber,f'{len(data)}','sql committed \n ')
    cursor.close()
    return len(data)

#to test the 7 PC numbers for a specific date
#total = 0
#total += scrape(['2020-04-23', 'Thu', '', '04', '23', '2020'],'04.22.2020','347884',fr'C:\Users\Hasin Choudhury\Desktop\pythonSeleniumRadiant')
#total += scrape('04.11.2020','348454',fr'C:\Users\Hasin Choudhury\Desktop\pythonSeleniumRadiant')
#total += scrape('04.11.2020','349941',fr'C:\Users\Hasin Choudhury\Desktop\pythonSeleniumRadiant')
#total += scrape('04.11.2020','354651',fr'C:\Users\Hasin Choudhury\Desktop\pythonSeleniumRadiant')
#total += scrape('04.11.2020','355342',fr'C:\Users\Hasin Choudhury\Desktop\pythonSeleniumRadiant')
#total += scrape('04.11.2020','355673',fr'C:\Users\Hasin Choudhury\Desktop\pythonSeleniumRadiant')
#total += scrape('04.11.2020','356170',fr'C:\Users\Hasin Choudhury\Desktop\pythonSeleniumRadiant')
#print(total)

#These are some checks to have (there are a lot to check, but these are the crucial ones):

#this one should show the last row:
#print(dataCell)

#these should match:
#print(len(dataRows)) #what is in the HTML DOM
#print(len(data)) #what the script makes
#end

#sql for one row and for the for loop, respectively
#cursor.execute("INSERT INTO hasindatabase.testcsv (`PC Number`,`Date`,`Item`,`Price`,`Items Sold`,`Sold Amount`,`Percent Sales`,`Item Reductions`,`Item Refunds`,`Item Net Sales`) VALUES ('347884', '2020-03-18', 'Bagel w/CC, Item Only', '2.49', '16', '39.84', '2.76', '2.94', '0.0', '36.9')")
#cursor.execute("INSERT INTO hasindatabase.testcsv (`PC Number`,`Date`,`Item`,`Price`,`Items Sold`,`Sold Amount`,`Percent Sales`,`Item Reductions`,`Item Refunds`,`Item Net Sales`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

#proper sibling navigation:
#dataRows[index].select('.CellStyle')[0].next_sibling.next_sibling['dval'] #twice because of whitespace

#should grab count of the table, including 'total' ROWS (the rows labeled as 'total')
#lastID = table.tfoot.find('tr')['id']
