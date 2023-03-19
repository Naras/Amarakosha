#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'NarasMG'

import peewee, os
from source.Controller.iscii2utf8 import *
# print(os.path.join(os.getcwd(), 'Amarakosha.db'))
conn_unicode = peewee.SqliteDatabase(os.path.join(os.getcwd(), 'Amarakosha.db'), pragmas={'journal_mode': 'wal','cache_size': -1024 * 64})
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
    try:
        scripts_map_unicode = mypar.make_script_maps_unicode_to_iscii()
        result_as_list = []
        for i, ch in enumerate(unicode_string):
            # print('ch %s hex %s dec %s'%(ch, hex(ord(ch)), ord(ch)))
            result_as_list.append(chr(scripts_map_unicode[ord(ch)]))
            if ord(ch) in nukta_specials.values(): result_as_list.append(chr(ISCII_NUKTA))
        return ''.join(result_as_list)
    except Exception as e:
        raise Exception('unicode_iscii: character %s unicode-string %s character %s' % (e, unicode_string, ch))
def schemaParse():
    cursor = conn_unicode.get_tables()
    mypar = Parser()
    mypar.set_script(1)
    tbls = []
    for row in cursor:
        tbls.append(row)
    return tbls
def sqlQueryUnicode(sql, param=None, maxrows=5, duplicate=False, script=1):
    # lstParam = [x for x in param] if isinstance(param,tuple) else param
    # print('sql=%s param=%s'%(sql, lstParam))
    current = 0
    if param==None: rowcursor = conn_unicode.execute_sql(sql)
    else:
        if not isinstance(param,tuple): param = (param,)
        rowcursor = conn_unicode.execute_sql(sql, param)
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
                    resultRow.append(field)
                    if duplicate: resultRow.append(unicode_iscii(field))
            result += [resultRow]
            current += 1
            if maxrows > 0 and current > maxrows:
                break
    except IllegalInput as e:
        logging.warning('%s' % e)

    columns = [column[0] for column in rowcursor.description]
    if duplicate: columns = list(flatMap(lambda x: (x, x), columns))
    return columns, result
def tblSelectUnicode(table_name,maxrows=5,duplicate=False, script=1):
    current = 0
    rowcursor = conn_unicode.execute_sql('select * from ' + table_name)
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
                    tblRow.append(field)
                    if duplicate: tblRow.append(unicode_iscii(str(field), script))
            tbl += [tblRow]
            current += 1
            if maxrows > 0 and current > maxrows:
                break
    except IllegalInput as e:
        logging.warning('%s' % e)
    columns = [column[0] for column in rowcursor.description]
    if duplicate: columns = list(flatMap(lambda x: (x, x), columns))

    return columns, tbl
if __name__ == '__main__':
    cols, lines = sqlQueryUnicode('Select * from Subanta where Base = ?', "अंशक") #×èÔÏè
    print('Subanta: %s\n%s'%(cols, lines))
    # cols, lines = sqlQueryUnicode('Select * from Subanta where Base = ?', 'अंशुमती') #×èÔÏè
    # print('Subanta: %s\n%s'%(cols, lines))

    # cols, lines = sqlQuery('Select * from SubFin where Finform = ?', 'ÏÚÌ£')
    # print('SubFin: %s\n%s' % (cols, lines))
    # cols, lines = sqlQueryUnicode('Select * from SubFin where Finform = ?', 'राम')
    # print('SubFin: %s\n%s' % (cols, lines))
    #
    # cols, lines = sqlQuery('select * from stinfin where field2 = ? and field3 = ?', (383, "1A"))
    # print('stinfin: %s\n%s' % (cols, lines))
    # cols, lines = sqlQueryUnicode('select * from stinfin where field2 = ? and field3 = ?', (383, "1A"))
    # print('stinfin: %s\n%s' % (cols, lines))
    #
    # cols, lines = sqlQuery('select * from Sdhatu where field2 = ? ', unicode_iscii('अंश्'))
    # print('Sdhatu: %s\n%s' % (cols, lines))
    #
    # cols, lines = sqlQueryUnicode('select * from Sdhatu where field2 = ? ', 'अंश्')
    # print('Sdhatu: %s\n%s' % (cols, lines))
    #
    # cols, data = tblSelect('sdhatu')
    # print('sdhatu: %s\n%s' % (cols, data))
    # cols, data = tblSelectUnicode('sdhatu')
    # print('sdhatu: %s\n%s' % (cols, data))
    #
    # cols, lines = sqlQuery('select * from krud where field4=? and field5=?', ('a1', 383))
    # print('krud: %s\n%s' % (cols,lines))
    # cols, lines = sqlQueryUnicode('select * from krud where field4=? and field5=?', ('a1', 383))
    # print('krud: %s\n%s' % (cols,lines))
    #
    # # cols, lines = sqlQuery('Select * from Amara_Words where Word = ?', "×èÔÏè")
    # # print('Amara_words: %s\n%s'%(cols, lines))
    # # cols, lines = sqlQueryUnicode('Select * from Amara_Words where Word = ?', 'स्वर्') #×èÔÏè
    # # print('Amara_words: %s\n%s'%(cols, lines))
    #
    # for i in range(5):
    #     gana = str(i) if i > 0 else ''
    #     cols, lines = sqlQueryUnicode('select * from Sdhatu where cast(field9 as text) like ?', gana + '__')
    #     print('%d Sdhatu: gana %s' % (i, cols))
    #     for line in lines: print(line)
    # for i in range(4):
    #     cols, lines = sqlQueryUnicode('select * from Sdhatu where cast(field9 as text) like ?', '_' + str(i) + '_')
    #     print('%d Sdhatu: padi %s' % (i, cols))
    #     for line in lines: print(line)
    # for i in range(3):
    #     cols, lines = sqlQueryUnicode('select * from Sdhatu where cast(field9 as text) like ?', '__' + str(i))
    #     print('%d Sdhatu: it %s' % (i, cols))
    #     for line in lines: print(line)
    #
    # tbls = schemaParse()
    # print('tables %s' % tbls)

    cols, lines = sqlQueryUnicode('Select su.base, su.erb, su.code, sf.sufstr from Subanta su, sufcode sf where Base = ? and sf.code = substr(su.code,1, 4)', 'अंशुमती')
    print('Subanta/Sufcode: %s\n%s'%(cols, lines))





