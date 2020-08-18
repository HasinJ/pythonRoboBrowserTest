import MySQLdb
import config
import os
import os.path as path
import time

def connectDB():
    mydb = MySQLdb.connect(host = config.RDS_HOSTNAME,
        user = config.RDS_USER,
        passwd = config.RDS_PASSWORD,
        db = config.RDS_DBNAME)
    return mydb

def insertDatePK(values):
    mydb = connectDB()
    cursor = mydb.cursor()

    sql = 'INSERT INTO DateTBL (`Date`,`DOW`,`TOD`,`Month`,`Day`,`Year`,`Day of Year`) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    val = values
    cursor.execute(sql,val)

    mydb.commit()
    cursor.close()

def deleteDay(dateSTR):

    mydb = connectDB()
    cursor = mydb.cursor()
    dirList = os.listdir(config.dir + fr'\Consumption Table Queries\Insert Queries')

    #for every file in directory
    for file in dirList:
        tableName = file.split(' ')[0]
        sql=fr'DELETE FROM {tableName} '
        destination = config.dir + fr'\Consumption Table Queries\Insert Queries\{file}'
        if path.exists(destination)==True:
            with open(destination) as f:
                while True:
                    line = f.readline()
                    if not line:
                        sql+=line.strip()
                        break
                    sql+=line.strip() + ' '

                sql=f"{sql} AND `Date` = '{dateSTR}'"
                sql=sql.replace('Item','ItemName')
                #print(sql) #checks sql
                cursor.execute(sql)
                mydb.commit()
    sql=f"DELETE FROM LeftoversTBL WHERE `Date` = '{dateSTR}'"
    cursor.execute(sql)
    mydb.commit()
    cursor.close()

def moveOneTempSQL(target):
    mydb = connectDB()
    cursor = mydb.cursor()
    sql=''

    #this is pretty specific
    destination = config.dir + fr'\Consumption Table Queries\Insert Queries\{target} Insert.txt'
    if path.exists(destination)==True:
        with open(destination) as f:
            for line in f:
                if line.strip()=='Order by Item':
                    sql += line.strip()
                    break
                sql+=line.strip() + ' '

    cursor.execute(sql)
    mydb.commit()
    print(sql)
    cursor.close()

def moveAllTempSQL():
    mydb = connectDB()
    cursor = mydb.cursor()

    dirList = os.listdir(config.dir + fr'\Consumption Table Queries\Insert Queries')


    #for every file in directory
    for file in dirList:
        tableName = file.split(' ')[0]
        sqlInsert=fr'INSERT INTO {tableName} (`PCNumber`, `Date`, `ItemName`, `Price`, `UnitSold`, `SoldAmount`) SELECT `PC Number`, `Date`, `Item`, `Price`, `Items Sold`, `Sold Amount` FROM TempTable '
        sqlDelete=fr'DELETE FROM TempTable '
        destination = config.dir + fr'\Consumption Table Queries\Insert Queries\{file}'
        if path.exists(destination)==True:
            with open(destination) as f:
                while True:
                    line = f.readline()
                    if not line:
                        sqlInsert+=line.strip()
                        sqlDelete+=line.strip()
                        break
                    sqlInsert+=line.strip() + ' '
                    sqlDelete+=line.strip() + ' '

                sql = fr"{sqlInsert};"
                #print(sql) #checks sql
                cursor.execute(sql)
                mydb.commit()
                time.sleep(1)

                sql = fr"{sqlDelete};"
                #print(sql) #checks sql
                cursor.execute(sql)
                mydb.commit()

    sql = "INSERT INTO LeftoversTBL (`id`, `PC Number`, `Date`, `Item`, `Price`, `Items Sold`, `Sold Amount`, `Percent Sales`, `Item Reductions`, `Item Refunds`, `Item Net Sales`) SELECT * FROM TempTable;"
    print(f"\n \n{sql}")
    cursor.execute(sql)
    mydb.commit()
    cursor.close()

def oneFile(folder, file):
    mydb = connectDB()
    cursor = mydb.cursor()

    destination = config.dir + fr'\Consumption Table Queries\{folder}\{file}'

    with open(destination) as f:
        sql=''
        while True:
            line = f.readline()
            if not line:
                sql+=line.strip()
                break
            sql+=line.strip() + ' '
        #print(sql) #checks sql
        cursor.execute(sql)

    mydb.commit()
    cursor.close()

def insertpcNumber(pcNumber):
    mydb = connectDB()
    cursor = mydb.cursor()

    sql=f'INSERT INTO storeTBL (`PCNumber`) VALUES ({pcNumber})'
    #print(sql)

    cursor.execute(sql)
    mydb.commit()
    cursor.close()

#commitSQL("DELETE FROM `DateTBL` WHERE (`Date` = '2020-07-13');") #example
#deleteDay('2020-07-14')

#deleteDay('2020-07-18')
#run this to empty temp table
#moveAllTempSQL()
#oneFile('Temp','TempTable Truncate.txt')
#deleteDay('2020-08-04') #should delete day from item tables and leftovers table
#print('\n \n THIS SHOULDNT SHOW \n \n') #put this on when uncommenting something down here

##sql query def template:
#mydb = connectDB()
#cursor = mydb.cursor()
#cursor.execute(sql) #the rest from here (including) are for commiting
#mydb.commit()
#cursor.close()
