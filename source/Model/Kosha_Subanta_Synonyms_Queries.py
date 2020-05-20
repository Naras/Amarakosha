import logging

import pyodbc
from iscii2utf8 import *
import pandas as pd

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=I:\VMBox-Shared-WinXP-VB\ChaamiMaama\Narasimhan\all_in_one_DAO\wordsdata.mdb;')
# conn = pyodbc.connect('DSN=Amarakosha')
cursor = conn.cursor()
rowcursor = conn.cursor()
maxrows = 5

mypar = Parser()
mypar.set_script(1)
def flatMap(f, li):
    mapped = map(f, li)
    flattened = flatten_single_dim(mapped)
    yield from flattened
def flatten_single_dim(mapped):
    for item in mapped:
        for subitem in item:
            yield subitem

# isascii = lambda s: len(s) == len(s.encode())
def isascii(s):
    # import re
    # return re.search('[^\x00-\x7F]', s) is None
    try:
        s.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False
def iscii_unicode(iscii_string):
    flush = 0
    x_as_List = [ord(char) for char in iscii_string+' ']
    n = mypar.iscii2utf8(x_as_List, flush)
    # y = x[n:]
    return ''.join([ch for ch in mypar.write_output()])
def schemaParse():
    conn = pyodbc.connect(
        r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=I:\VMBox-Shared-WinXP-VB\ChaamiMaama\Narasimhan\all_in_one_DAO\wordsdata.mdb;')
    # conn = pyodbc.connect('DSN=Amarakosha')
    cursor = conn.cursor()
    mypar = Parser()
    mypar.set_script(1)
    tbls = []
    for row in cursor.tables():
        if not (str(row.table_name).startswith("MSys") or str(row.table_name).startswith("Con")):
            tbls.append(row.table_name)
    return tbls
def sqlQuery(sql,param,maxrows=5,duplicate=True):
    current = 0
    rowcursor.execute(sql, param)
    try:
        result = []
        for r in rowcursor.fetchall():
            # print(r)
            resultRow = []
            for field in r:
                # resultRow.append(field)
                if isascii(str(field)):
                    resultRow.append(field)
                    if duplicate: resultRow.append(field)
                else:
                    resultRow.append(iscii_unicode(str(field)))
                    if duplicate: resultRow.append(field)
            result += [resultRow]
            current += 1
            if maxrows > 0 and current > maxrows:
                break
    except IllegalInput as e:
        logging.warning('%s' % e)

    columns = [column[0] for column in rowcursor.description]
    if duplicate: columns = list(flatMap(lambda x: (x, x), columns))
    return columns, result
def tblSelect(table_name,maxrows=5,duplicate=True):
    current = 0
    rowcursor.execute('select * from ' + table_name)
    try:
        tbl = []
        for r in rowcursor.fetchall():
            # print(r)
            tblRow = []
            for field in r:
                if isascii(str(field)):
                    tblRow.append(field)
                    if duplicate: tblRow.append(field)
                else:
                    tblRow.append(iscii_unicode(str(field)))
                    if duplicate: tblRow.append(field)
            tbl += [tblRow]
            current += 1
            if maxrows > 0 and current > maxrows:
                break
    except IllegalInput as e:
        logging.warning('%s' % e)
    columns = [column[0] for column in rowcursor.description]
    if duplicate: columns = list(flatMap(lambda x: (x, x), columns))

    return columns, tbl
    '''
    # print(columns)
    qry = 'select ' + ','.join(columns) + ' from ' + row.table_name
    # print(qry)
    tblDF = pd.DataFrame(pd.read_sql_query(qry, conn), columns=columns)  # 'select * from ' + row.table_name,conn)
    # rowcursor.execute('select * from ' + row.table_name)
    # tblDF = pd.DataFrame(rowcursor.fetchall())
    # df = pd.DataFrame()
    # for fld in tblDF: print(type(fld),fld)
    # tblDF.columns = columns
    df = []
    for i in tblDF.head().index:
        r = []
        for col in columns:
            if not isascii(str(tblDF[col][i])):
                r.append(iscii_unicode(tblDF[col][i]))
            else:
                r.append(tblDF[col][i])
        df.append(r)
    print(df)
    tblDF = pd.DataFrame(df)
    tblDF.columns = columns
    # tblDF.at[i, k] = iscii_unicode(str(v))
    # print(tblDF.head())
    '''

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename='../../Amarakosha.log', format='%(asctime)s %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p')
    # table_names = schemaParse()
    # for tbl in ['Amara_Words']: # table_names:
    #     cols, tbl = tblSelect(tbl)
    #     print('%s\n%s'%(cols, tbl))
    # cols,lines = sqlQuery('Select * from Janani1 where EngWord like ?',"%A calf%")
    # print('%s\n%s'%(cols, lines))
    cols,lines = sqlQuery('Select * from Subanta where Base = ?', "¤¢ÕÝÌÂÜ") #×èÔÏè
    print('%s\n%s'%(cols, lines))
