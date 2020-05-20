from source.Controller import Sandhi_Convt
from source.Model import Kosha_Subanta_Synonyms_Queries

def Amarakosha(amaraWord):
    qry = 'select * from Janani1 where Words like ?'
    param = '%' + amaraWord + '%'
    cols, dbdata = Kosha_Subanta_Synonyms_Queries.sqlQuery(qry, param, maxrows=0, duplicate=False)
    # print('%s\n%s' % (cols, dbdata))
    synonyms = (words.split(' ') for words in [r for r in [rec[1] for rec in dbdata] if
                                               Kosha_Subanta_Synonyms_Queries.iscii_unicode(amaraWord) in r.split(' ')])
    synonyms = to_2dList(list(synonyms)[0], 4)
    return synonyms
def to_2dList(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]
def Subanta(base):
    # do sandhi and find vibhakti and vachana forms as per SubGeneration and SubAnalysis in the legacy VB Code
    forms, vacanas, vibhaktis, anta, linga = [],[],[],'',''
    base = str(base)[:-1]
    qry = 'select * from Subanta where Base=?'
    cols, dbdata = Kosha_Subanta_Synonyms_Queries.sqlQuery(qry, base, maxrows=0)
    # print('param %s\n%s\n%s' % (base, cols, dbdata))
    # self.modelJanani._data = pandas.DataFrame(dbdata, columns=cols)
    codeInColumn = cols.index('Code')
    erbInColumn = cols.index('Erb') + 1
    dbSufcodes = []
    for row in dbdata:
        suffixes = []
        erb = row[erbInColumn]
        code = row[codeInColumn]
        # print(erb)
        qry = 'select * from Sufcode where code=?'
        param = row[codeInColumn][:4]
        # print(param)
        cols, dbSufcode = Kosha_Subanta_Synonyms_Queries.sqlQuery(qry, param, maxrows=0)
        # print('%s\n%s' % (cols, dbSufcode))
        dbSufcodes += dbSufcode
        sufstrInColumn = cols.index('SufStr')
        for item in dbSufcode:
            # print(item[sufstrInColumn])
            suffixes += str(item[sufstrInColumn]).split(" ")
        # print(suffixes)
        subforms = []
        for sufcode in suffixes:
            subforms.append(Sandhi_Convt.Convt(sufcode))
        # print([erb+item for item in subforms])
        # print([cli_browse.iscii_unicode(erb+item) for item in subforms])
        subforms_with_sandhi = [Kosha_Subanta_Synonyms_Queries.iscii_unicode(
            Sandhi_Convt.Sandhi(erb + item + ' ')) for item in subforms]
        # print(subforms_with_sandhi)
        # print([Functions_Sandhi_Convt.Sandhi(erb + item) for item in subforms])
        for entry in Sandhi_Convt.antas:
            if code[0] == entry[0]:
                anta = entry[2]  # equivalent of Right$(antas(i), Len(antas(i)) - 2) in VB code
                if code[0] == 'A':
                    anta += "ÚÆèÂ£"
                else:
                    anta += "³ÚÏÚÆèÂ£"
                break
        linga = Sandhi_Convt.lingas[int(code[1:2])]
        # print('anta %s linga %s'%(cli_browse.iscii_unicode(anta), cli_browse.iscii_unicode(linga)))
        vacanas = ['एकवचन', 'द्विवचन', 'बहुवचन']
        vibhaktis = ['प्रथमा', 'द्वितीया', 'तृतीया', 'चतुर्थि', 'पंचमि', 'शष्टि', 'सप्तमि', 'सं प्रथम']
        forms = [subforms_with_sandhi[0:3], subforms_with_sandhi[3:6], subforms_with_sandhi[6:9],
                 subforms_with_sandhi[9:12],
                 subforms_with_sandhi[12:15], subforms_with_sandhi[15:18], subforms_with_sandhi[18:21],
                 # subforms_with_sandhi[21:24]]
                 list(map(lambda word: 'हे ' + word, subforms_with_sandhi[0:3]))]
    return forms, vacanas, vibhaktis, anta, linga


