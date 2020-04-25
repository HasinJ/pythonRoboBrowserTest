import MySQLdb
import RDSconfig
import os
import os.path as path

def connectDB():
    mydb = MySQLdb.connect(host = RDSconfig.RDS_HOSTNAME,
        user = RDSconfig.RDS_USER,
        passwd = RDSconfig.RDS_PASSWORD,
        db = RDSconfig.RDS_DBNAME)
    return mydb

def insertDatePK(values):
    mydb = connectDB()
    cursor = mydb.cursor()

    sql = 'INSERT INTO DateTBL (`Date`,`DOW`,`TOD`,`Month`,`Day`,`Year`) VALUES (%s,%s,%s,%s,%s,%s)'
    val = values
    cursor.execute(sql,val)

    mydb.commit()
    cursor.close()

def moveOneTempSQL(target):
    mydb = connectDB()
    cursor = mydb.cursor()
    sql=''

    #this is pretty specific
    destination = fr'C:\Users\Hasin Choudhury\Desktop\pythonSeleniumRadiant\Consumption Table Queries\{target} Insert.txt'
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

    dirList = os.listdir(fr'C:\Users\Hasin Choudhury\Desktop\pythonSeleniumRadiant\Consumption Table Queries')


    #this is pretty specific
    for file in dirList:
        sql=''
        destination = fr'C:\Users\Hasin Choudhury\Desktop\pythonSeleniumRadiant\Consumption Table Queries\{file}'
        if path.exists(destination)==True:
            with open(destination) as f:
                while True:
                    line = f.readline()
                    if not line:
                        sql+=line.strip()
                        break
                    sql+=line.strip() + ' '
                print(sql)
                cursor.execute(sql)

    mydb.commit()
    cursor.close()

moveAllTempSQL()
