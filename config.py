import datetime
dateToday = datetime.datetime.now().strftime('%x') #local version of date
year = datetime.datetime.now().strftime('%Y')
dateToday = dateToday[:6] + year #adds the year in full, "2021" instead of "21"
dateToday = '04/02/2020' #temp
dateDotNotation = dateToday.replace('/', '.')
print(dateToday)

radUser = ''
radPass = ''
