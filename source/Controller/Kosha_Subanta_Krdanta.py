import inspect

from source.Controller import Sandhi_Convt
from source.Model import AmaraKosha_Subanta_Krdanta_Queries
from source.View import Transliterate

Tganas = ["भ्वादिगणः", "अदादिगणः",  "जुहोत्यादिगणः",  "दिवादिगणः",  "स्वादिगणः",  "तुदादिगणः",  "रुधादिगणः",  "तनादिगणः",  "क्रयादिगणः",  "चुरादिगणः"]
Tkarmas = ["सकर्मकः", "अकर्मकः",  "द्विकर्मकः"]
Tpadis = ["परस्मैपदी",  "आत्मनेपदी",  "उभयपदी"]
Tyits = ["सेट्", "अनिट्", "वेट्"]
purushas = ["प्रथमपुरुषः", "मध्यमपुरुषः", "उत्तमपुरुषः"]

# global krdData
class krdData:
    def __init__(self):
        self.linga = None
        self.verb = None      # SDhatu.field2
        self.nijverb = None   # SDhatu.field3
        self.sanverb = None   # SDhatu.field4
        self.GPICode = None   # SDhatu.field9
        self.gana = None
        self.padi = None
        self.it = None
        self.dhatuVidhah = None  # int(SDhatu.field4[:-1])
        self.krdantaVidhah = None
        self.combinedM = None  # SDhatu.field10
        self.wtype = None
        self.pratyayaVidhah = None
        self.karma = None
        self.meaning = None
        self.vacana = None
        self.vibhakti = None
        self.sabda = None      #KRUD.field3
        self.erb = None        #KRUD.Field1
        self.det = None        #KRUD.field2
        self.ddet = None        #KRUD.field4
        self.Dno = None        #int(KRUD.Field5)
    def get(self):
        return {'linga':self.linga, 'verb':self.verb, 'nijverb':self.nijverb, 'sanverb':self.sanverb, 'GPICode':self.GPICode, 'gana':self.gana,
                'padi':self.padi, 'it':self.it, 'dhatuVidhah':self.dhatuVidhah, 'krdantaVidhah':self.krdantaVidhah, 'combinedM':self.combinedM,
                'wtype':self.wtype, 'pratyayaVidhah':self.pratyayaVidhah, 'karma':self.karma, 'meaning':self.meaning, 'vacana':self.vacana,
                'vibhakti':self.vibhakti, 'sabda':self.sabda, 'erb':self.erb, 'det':self.det, 'ddet':self.ddet, 'Dno':self.Dno}
    def __str__(self):
        return ','.join(self.get())
def Amarakosha(amaraWord):
    qry = 'select * from Janani1 where Words like ?'
    param = '%' + amaraWord + '%'
    cols, dbdata = AmaraKosha_Subanta_Krdanta_Queries.sqlQuery(qry, param, maxrows=0, duplicate=False)
    # print('%s\n%s' % (cols, dbdata))
    KanWord = [item[cols.index('KanWord')] for item in dbdata]
    EngWord = [item[cols.index('EngWord')] for item in dbdata]
    HinWord = [item[cols.index('HinWord')] for item in dbdata]
    synonyms = (words.split(' ') for words in [r for r in [rec[1] for rec in dbdata] if
                                               AmaraKosha_Subanta_Krdanta_Queries.iscii_unicode(amaraWord) in r.split(' ')])
    synonyms = to_2dList(list(synonyms)[0], 4)
    KanWord = [Transliterate.transliterate_lines(item,'kannada') for item in list(map(lambda i : i or '', KanWord))]
    return synonyms, KanWord, EngWord, HinWord
def to_2dList(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]
def Subanta(base):
    # do sandhi and find vibhakti and vachana forms as per SubGeneration and SubAnalysis in the legacy VB Code
    forms, vacanas, vibhaktis, anta, linga = [],[],[],'',''
    base = str(base)[:-1]
    qry = 'select * from Subanta where Base=?'
    cols, dbdata = AmaraKosha_Subanta_Krdanta_Queries.sqlQuery(qry, base, maxrows=0)
    # print('param %s\n%s\n%s' % (base, cols, dbdata))
    # self.modelFinalResults._data = pandas.DataFrame(dbdata, columns=cols)
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
        cols, dbSufcode = AmaraKosha_Subanta_Krdanta_Queries.sqlQuery(qry, param, maxrows=0)
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
        subforms_with_sandhi = [AmaraKosha_Subanta_Krdanta_Queries.iscii_unicode(
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
def krdanta_arthas_karmas(krdantaWord):
    qry = 'select * from Sdhatu where field2 = ?'
    cols, dataDhatu = AmaraKosha_Subanta_Krdanta_Queries.sqlQuery(qry, krdantaWord, maxrows=0)
    # print('Sdhatu field2=%s %s\n%s'%(krdantaWord, cols, dataDhatu))
    for item in dataDhatu:
        arthas_karmas = item[cols.index('Field8')].split('/')
        arthas = [word[:-2] for word in arthas_karmas]
        karmas = [int(word[len(word)-1]) for word in arthas_karmas]
        karmas = [Tkarmas[karma] for karma in karmas]
        # print('arthas %s\nkarmas %s'%(arthas, karmas))
    dhatuNo = dataDhatu[0][cols.index('Field1') + 1]
    return arthas, karmas, dhatuNo
def Krdanta_SortedList(dhatuNo, DhatuVidah, KrdantaVidah, KrdMode):
    # pratvidha = ["तव्य",  "अनीयर्",  "य",  "क्त",  "क्तवतु",  "शतृ",  "शानच्",  "स्यशतृ",  "स्यशानच्",  "तुमुन्",  "क्त्वा"].index(dialog.KrdMode.strip())
    # KrdVidha = ["विध्यर्थः",  "भूतः",  "वर्तमानः",  "भविष्यत्",  "कृदव्ययम्"].index(dialog.KrdantaVidah.strip())
    KrdCodeDicts = {"विध्यर्थः": {"तव्य": "a", "अनीयर्": "a", "य": "c"}, "विभूतः": {"तव्य": "d", "अनीयर्": "e"},
                    "य": {"तव्य": "f", "अनीयर्": "g"}, "क्त": {"तव्य": "h", "अनीयर्": "i"},
                    "क्तवतु": {"तव्य": "A", "अनीयर्": "B"}}
    KrdCode = KrdCodeDicts[KrdantaVidah][KrdMode] + \
              {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah]
    krdDatas = []
    qry = 'select * from krud where field4=? and field5=?'
    # print('qry %s param %s'%(qry,(KrdCode, dhatuNo)))
    cols, dataKrud = AmaraKosha_Subanta_Krdanta_Queries.sqlQuery(qry, (KrdCode, dhatuNo), maxrows=0)
    # print('krud field4=%s field5=%s %s\n%s'%(KrdCode,dhatuNo, cols, dataKrud))
    erbInColumn = cols.index('Field1') + 1  # pick duplicate col
    sabdaInColumn = cols.index('Field3') + 1
    forms = []
    for item in dataKrud:
        krdDataInstance = krdData()
        krdDataInstance.dhatuVidhah = DhatuVidah
        krdDataInstance.krdantaVidhah = KrdantaVidah
        krdDataInstance.pratyayaVidhah = KrdMode
        if not KrdantaVidah == "भविष्यत्":
            qry = 'select * from Sufcode where code=?'
            code = item[2][:4]
            # print('Sufcode: qry %s code %s'%(qry,code))
            cols, dataSufcode = AmaraKosha_Subanta_Krdanta_Queries.sqlQuery(qry, code, duplicate=False, maxrows=0)
            # print(('sufcode %s cols %s\n%s')%(param, cols, dataSufcode))
            krdDataInstance.erb = item[erbInColumn]
            krdDataInstance.sabda = AmaraKosha_Subanta_Krdanta_Queries.iscii_unicode(item[sabdaInColumn])
            krdDataInstance.linga = AmaraKosha_Subanta_Krdanta_Queries.iscii_unicode(Sandhi_Convt.lingas[int(code[1])])
            suffixes = str(dataSufcode[0][2]).split(' ')
            # from VB SplitAndDisplay routine
            subforms = []
            for sufcode in suffixes:
                subforms.append(Sandhi_Convt.Convt(sufcode))
            # print('subforms %s'%([erb+item for item in subforms]))
            # print([Kosha_Subanta_Synonyms_Queries.iscii_unicode(erb+item) for item in subforms])
            subforms_with_sandhi = [AmaraKosha_Subanta_Krdanta_Queries.iscii_unicode(
                Sandhi_Convt.Sandhi(krdDataInstance.erb + item)) for item in subforms]
            # print([Sandhi_Convt.Sandhi(erb + item) for item in subforms])
            forms += [subforms_with_sandhi[0:3], subforms_with_sandhi[3:6], subforms_with_sandhi[6:9],
                     subforms_with_sandhi[9:12], subforms_with_sandhi[12:15], subforms_with_sandhi[15:18],
                     subforms_with_sandhi[18:21], subforms_with_sandhi[21:24]]
            # from VB GetAnalysedInfo routine
            qry = 'Select * from Sdhatu where field1=?'
            cols, dataAnalysed = AmaraKosha_Subanta_Krdanta_Queries.sqlQuery(qry, dhatuNo, maxrows=0)
            # print('%s\nData Analysed %s'%(cols, dataAnalysed))
            # for item in dataAnalysed:
            item = dataAnalysed[0]  # there will be only one record!
            krdDataInstance.verb = item[cols.index('Field2')]
            krdDataInstance.nijverb = item[cols.index('Field3')]
            krdDataInstance.sanverb = item[cols.index('Field4')]
            krdDataInstance.GPICode = item[cols.index('Field9')]
            krdDataInstance.gana = Tganas[int(krdDataInstance.GPICode[0]) - 1]
            krdDataInstance.padi = Tpadis[int(krdDataInstance.GPICode[1]) - 1]
            krdDataInstance.it = Tyits[int(krdDataInstance.GPICode[2]) - 1]
            krdDataInstance.combinedM = item[cols.index('Field10')]
            krdDatas.append(krdDataInstance)
    vacanas = ['एकवचन', 'द्विवचन', 'बहुवचन']
    vibhaktis = ['प्रथमा', 'द्वितीया', 'तृतीया', 'चतुर्थि', 'पंचमि', 'शष्टि', 'सप्तमि', 'सं प्रथम'] * 3
    # print('no. of items %i subforms with sandhi %s' % (len(forms), forms))
    # for item in krdDatas:
    #     attributes = inspect.getmembers(item, lambda a: not (inspect.isroutine(a)))
    #     print([a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))])
    return forms, vacanas, vibhaktis, krdDatas
def Krdanta_Ganas(krdantaWord, DhatuVidah, KrdantaVidah, KrdMode, Gana):
    qry = 'select * from Sdhatu where field2 = ?'
    param = krdantaWord
    cols, data = AmaraKosha_Subanta_Krdanta_Queries.sqlQuery(qry, param, maxrows=0)
def Krdanta_Padis(krdantaWord, DhatuVidah, KrdantaVidah, KrdMode, Padi):
    qry = 'select * from Sdhatu where field2 = ?'
    param = krdantaWord
    cols, data = AmaraKosha_Subanta_Krdanta_Queries.sqlQuery(qry, param, maxrows=0)
def Krdanta_Karmas(krdantaWord, DhatuVidah, KrdantaVidah, KrdMode, Karma):
    qry = 'select * from Sdhatu where field2 = ?'
    param = krdantaWord
    cols, data = AmaraKosha_Subanta_Krdanta_Queries.sqlQuery(qry, param, maxrows=0)
def Krdanta_Its(krdantaWord, DhatuVidah, KrdantaVidah, KrdMode, It):
    qry = 'select * from Sdhatu where field2 = ?'
    param = krdantaWord
    cols, data = AmaraKosha_Subanta_Krdanta_Queries.sqlQuery(qry, param, maxrows=0)




