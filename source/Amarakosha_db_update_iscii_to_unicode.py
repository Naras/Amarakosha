__author__ = 'NarasMG'

import peewee, os, pandas as pd  #, logging
from iscii2utf8 import *
conn_unicode = peewee.SqliteDatabase(os.getcwd() + '\WordsDataUnicode.db', pragmas={'journal_mode': 'wal', 'cache_size': -1024 * 64})
conn_iscii = peewee.SqliteDatabase(os.getcwd() + '\WordsData.db', pragmas={'journal_mode': 'wal','cache_size': -1024 * 64})
cursor = conn_unicode.cursor()
rowcursor = conn_unicode.cursor()
maxrows = 5

mypar = Parser()
mypar.set_script(1)

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
    cursor = conn_iscii.get_tables()
    mypar = Parser()
    mypar.set_script(1)
    tbls = []
    for row in cursor:
        tbls.append(row)
    return tbls
def sqlQueryIscii(sql, param=None, maxrows=0, script=1):
    current = 0
    if param==None: rowcursor = conn_iscii.execute_sql(sql)
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
                else:
                    resultRow.append(iscii_unicode(str(field), script))
            result += [resultRow]
            current += 1
            if maxrows > 0 and current > maxrows:
                break
    except IllegalInput as e:
        logging.warning('%s' % e)

    columns = [column[0] for column in rowcursor.description]
    return columns, result
def sqlQueryUnicode(sql, param=None, maxrows=0, script=1):
    current = 0
    if param==None: rowcursor = conn_unicode.execute_sql(sql)
    else:
        if not isinstance(param,tuple): param = (param,)
        rowcursor = conn_unicode.execute_sql(sql, param)
    result = []
    for r in rowcursor.fetchall():
            # print(r)
            resultRow = []
            for field in r:
                # resultRow.append(field)
                if isascii(str(field)):
                    resultRow.append(field)
                else:
                    resultRow.append(unicode_iscii(str(field), script))
            result += [resultRow]
            current += 1
            if maxrows > 0 and current > maxrows:
                break
    columns = [column[0] for column in rowcursor.description]
    return columns, result
def createCsvFiles(tbls):
    for tbl in tbls:
        cols_unicode, lines = sqlQueryIscii('Select * from %s' % tbl)
        # print('tbl:%s cols_unicode:%s\n%s' % (tbl, cols_unicode, lines))
        # print(os.path.join('WordsData', '%s.csv'%tbl))
        f = codecs.open(os.path.join('WordsData', '%s.csv' % tbl), mode='w', encoding='utf-8')
        f.writelines("%s\n" % ','.join([str(fld) for fld in cols_unicode]))
        # f.writelines(["%s\n" % ','.join([str(fld) for fld in item]) for item in lines])
        for item in lines:
            line = ''
            for fld in item:
                if ',' in str(fld): fld = '"' + str(fld) + '"'
                line += str(fld).replace('\r\n', '<nl>') + ','
            f.write('%s\n' % line[:-1])
        f.close
    print('csv files created')
def createUnicodeDatabase(tbls):
    for tbl in tbls:
        try:
            tbldata = pd.read_csv(os.path.join('WordsData', '%s.csv' % tbl))
            print('creating %s' % tbl)
            tbldata.to_sql(tbl, conn_unicode, if_exists='replace', index=False)
        except Exception as e:
            print('%s Exception->%s' % (tbl, e))
def compare(tbls):
    for tbl in tbls:
        cols_unicode, lines_unicode = sqlQueryIscii('Select * from %s' % tbl)
        cols_iscii, lines_iscii = sqlQueryUnicode('Select * from %s' % tbl)
        assert (cols_unicode == cols_iscii)
        # print('comparing table %s'%tbl)
        for unicodeItem, isciiItem in zip(lines_unicode, lines_iscii):
            try:
                # print(unicodeItem, isciiItem)
                for uni, isc in zip(unicodeItem, isciiItem):
                    if not isascii(str(isc)):
                        assert (unicode_iscii(uni) == isc)
                        assert (iscii_unicode(isc) == uni)
                        # uniwords, iscwords = uni.split(), isc.split()
                        # for uniword, iscword in zip(uniwords, iscwords):
                        #     assert(unicode_iscii(uniword) == iscword)
                        #     assert(iscii_unicode(iscword) == uniword)
            except AssertionError:
                id = isciiItem[cols_iscii.index('ID')] if 'ID' in cols_iscii else ''
                # print('%s id %s unicode-string %s(%s)\n\t\t\t\t iscii-string %s(%s)' % (tbl, id, uni, uni.encode('utf-8').hex(),  iscii_unicode(isc), iscii_unicode(isc).encode('utf-8').hex()))
                print('%s id %s unicode-string %s(%s)\n\t\t\t\t iscii-string %s(%s)' % (tbl, id, uni, [hex(ord(ch)) for ch in uni], iscii_unicode(isc), [hex(ord(ch)) for ch in iscii_unicode(isc)]))
            except Exception as e:
                print('%s exception %s' % (tbl, e))
            '''mypar.set_script(1)
            scripts_map_unicode = mypar.make_script_maps_unicode_to_iscii()
            # print(scripts_map_unicode)
            iscii_to_unicode, iscii_to_unicode_x, scripts_map_unicode_x = {}, {}, {}
            for k, v in scripts_map_unicode.items():
                iscii_to_unicode[v] = k
                iscii_to_unicode_x[hex(v)] = hex(k)
                scripts_map_unicode_x[hex(k)] = hex(v)
            print('%s\n%s\n%s\n%s'%(scripts_map_unicode, scripts_map_unicode_x, iscii_to_unicode, iscii_to_unicode_x))'''
            # exit(1)
def iscii_unicode_iscii(tbls):
    for tbl in tbls:
        cols, rows = tblSelect(tbl, maxrows=0)
        # print(tbl)
        for row in rows:
            try:
                for col, fld in enumerate(row):
                    if not isascii(str(fld)): assert(fld == unicode_iscii(iscii_unicode(fld)))
            except AssertionError:
                id = row[cols.index('ID')] if 'ID' in cols else ''
                print('%s id %s - col %s - %s(%s %s)'%(tbl, id, cols[col], iscii_unicode(fld), [hex(ord(ch)) for ch in fld], fld))
            except Exception as e:
                print('%s exception %s' % (fld, e))
def tblSelect(table_name, maxrows=5):
    current = 0
    rowcursor = conn_iscii.execute_sql('select * from ' + table_name)
    try:
        tbl = []
        for r in rowcursor.fetchall():
            # print(r)
            tblRow = []
            for field in r: tblRow.append(field)
            tbl += [tblRow]
            current += 1
            if maxrows > 0 and current > maxrows:
                break
    except IllegalInput as e:
        logging.warning('%s' % e)
    columns = [column[0] for column in rowcursor.description]
    return columns, tbl

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG, filename='iscii_unicode.log', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    tbls = schemaParse()
    # print('tables %s' % tbls)
    # createCsvFiles(['Janani1'])
    # createUnicodeDatabase(['Janani1'])
    compare(tbls)
    '''
    for test in ['³ßé',  'Âßé', '¤·è³åÑèè', '¤ÍåêéµèÏè', 'ÕÛÏåêé×èÃè',   # subanta
                 'ËÚÍÍÛÖèÍÂèé', '×èÈÏèÕÛÖèÍÂèé', 'ËÚÍÍÛÖèÍÂèé', '×èÈÏèÕÛÖèÍÂèé', '§ÏèÖèÍÍÛÖÛÂÔÂèé', 'ÑÛÑ·è¶ÛÖÛÂÔÂèé', '×èÌÚÏÍÛÖèÍÂèé',  # krud
                 '§ÏèÖèÍÍÛÖÛÂÔÂèé', 'ÑÛÑ·è¶ÛÖÛÂÔÂèé', '×èÌÚÏÍÛÖèÍÂèé',
                 '¨·è³èÂ ¨¼èºÚÂÚÌè ¨¼èºÂ ¨é¼è³èÃÚ£ ¨¼èºÚÃÚÌè ¨¼èºÅèÔÌè/¨ÀèÔÌè ¨³èÖÛ ¨³èÖèèÔØÛ ¨³èÖèèÌØÛ',
                 'ÊèÅ Âè×ÚÂÚÌè Âè×Â ÊèÅÚ£ Âè×ÚÃÚÌè ÊèÅèÔÌè/ÊèÄèÅèÔÌè Âè×Û Âè×èÔØÛ Âè×èÌØÛé',

                'ÌÂè×èÍ ÔÛÕáÖ ³á ÈßÃ³è ÈßÃ³è Øâ¢, ÈÏèÍÚÍ ÆØÜ¢ ê ¥ÄÛ ÈÄ ×á ÂÛÌÛ·èµÑ, ÆÆèÄÜÔÏèÂ ³Ú ×¢µèÏØ',
                 '¹å½á ºÑ ÊÛÆèÄÝ°¢ ³Ú Øâ¢ ê)', '³á ÈÚ× Ìá¢ ÏØÆá ÔÚÑá ³á ¬³ Øâ¢ ê)', 'ÌÂè×èÍ ÔÛÕáÖ ³á ÈßÃ³è ÈßÃ³è Øâ¢',
                 'ÈÏèÍÚÍ ÆØÜ¢ ê ¥ÄÛ ÈÄ ×á ÂÛÌÛ·èµÑ, ÆÆèÄÜÔÏèÂ ³Ú ×¢µèÏØ )',  # Janani
                 'ï¤Æè']:
        test_uni = iscii_unicode(test)
        test_isc = unicode_iscii(test_uni)
        if test != test_isc:
            print('ori %s\n%s\n%s\nuni %s\n%s\n%s\nisc %s\n%s\n%s'%(
                test, [hex(ord(ch)) for ch in test], [ord(ch) for ch in test],
                test_uni, [hex(ord(ch)) for ch in test_uni],  [ord(ch) for ch in test_uni],
                test_isc, [hex(ord(ch)) for ch in test_isc],  [ord(ch) for ch in test_isc]))
    iscii_unicode_iscii(tbls)  # ['Janani1', 'Subanta','KRUD', 'Sdhatu', 'Stinfin', 'Stinsuf']
    '''