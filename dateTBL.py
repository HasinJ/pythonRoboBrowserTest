import MySQLdb
import RDSconfig


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

def moveTempSQL(target):
    mydb = connectDB()
    cursor = mydb.cursor()

    sql = f'INSERT INTO {target} (`PCNumber`, `Date`, `ItemName`, `Price`, `UnitSold`, `SoldAmount`) '
    sql += 'SELECT `PC Number`, `Date`, `Item`, `Price`, `Items Sold`, `Sold Amount` '
    sql += 'FROM TempTable '
    sql += 'Where Item like "%Bagels, Item Only%" OR '
    sql += 'Item like "%Bagel w/%" OR '
    sql += 'Item like "%Bagels & Cream Cheese" OR '
    sql += 'Item like "Cinnamon Raisin Bagel" OR '
    sql += 'Item like "Cinnamon Sugar Bagel" OR '
    sql += 'Item like "Everything Bagel" OR '
    sql += 'Item like "Muligrain Bagel" OR '
    sql += 'Item like "Plain Bagel" OR '
    sql += 'Item like "Sesame Bagel" OR '
    sql += 'Item like "6 Croissants" OR '
    sql += 'Item like "Croissant, Plain Croissant" OR '
    sql += 'Item like "English Muffin, Item Only" '

    cursor.execute(sql)
    mydb.commit()
    cursor.close()

moveTempSQL('BagelTBL')
