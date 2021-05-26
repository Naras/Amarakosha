__author__ = 'NarasMG'

import peewee, os
from iscii2utf8 import *
conn = peewee.SqliteDatabase(os.getcwd() + '\WordsData.db', pragmas={'journal_mode': 'wal','cache_size': -1024 * 64})
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
def iscii_unicode(iscii_string, script=1):
    mypar.set_script(script)
    flush = 0
    x_as_List = [ord(char) for char in iscii_string+' ']
    n = mypar.iscii2utf8(x_as_List, flush)
    # y = x[n:]
    return ''.join([ch for ch in mypar.write_output()])
def unicode_iscii(unicode_string, script=1):
    mypar.set_script(script)
    scripts_map_unicode = mypar.make_script_maps_unicode_to_iscii()
    return ''.join([chr(scripts_map_unicode[ord(ch)]) for ch in unicode_string])

def schemaParse():
    cursor = conn.get_tables()
    mypar = Parser()
    mypar.set_script(1)
    tbls = []
    for row in cursor:
        tbls.append(row)
    return tbls
def sqlQuery(sql, param=None, maxrows=5, duplicate=True, script=1):
    # lstParam = [x for x in param] if isinstance(param,tuple) else param
    # print('sql=%s param=%s'%(sql, lstParam))
    current = 0
    if param==None: rowcursor = conn.execute_sql(sql)
    else:
        if not isinstance(param,tuple): param = (param,)
        rowcursor = conn.execute_sql(sql, param)
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
                    resultRow.append(iscii_unicode(str(field), script))
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
def tblSelect(table_name,maxrows=5,duplicate=True, script=1):
    current = 0
    rowcursor = conn.execute_sql('select * from ' + table_name)
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
                    tblRow.append(iscii_unicode(str(field), script))
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
    cols, lines = sqlQuery('Select * from Subanta where Base = ?', "¤¢ÕÝÌÂÜ") #×èÔÏè
    print('%s\n%s'%(cols, lines))

    cols, lines = sqlQuery('Select * from SubFin where Finform = ?', 'ÏÚÌ£')
    print('%s\n%s' % (cols, lines))

    cols, lines = sqlQuery('select * from stinfin where field2 = ? and field3 = ?', (383, "1A"))
    print('%s\n%s' % (cols, lines))

    cols, lines = sqlQuery('select * from Sdhatu where field2 = ? ', unicode_iscii('अंश्'))
    print('%s\n%s' % (cols, lines))

    cols2, lines2 = sqlQuery('select * from Sdhatu where field1 = ? ', 383)
    # print('%s\n%s' % (cols, lines))

    print(cols == cols2, lines == lines2)

    tbls = schemaParse()
    print('tables %s' % tbls)


