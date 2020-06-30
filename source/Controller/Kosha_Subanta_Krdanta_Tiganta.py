from source.Controller import Sandhi_Convt, Transliterate, blast
from source.Controller.Transliterate import transliterate_lines, IndianLanguages
from source.Model import AmaraKosha_Database_Queries

Tganas = ["भ्वादिगणः", "अदादिगणः",  "जुहोत्यादिगणः",  "दिवादिगणः",  "स्वादिगणः",  "तुदादिगणः",  "रुधादिगणः",  "तनादिगणः",  "क्रयादिगणः",  "चुरादिगणः"]
Tkarmas = ["सकर्मकः", "अकर्मकः",  "द्विकर्मकः"]
Tpadis = ["परस्मैपदी",  "आत्मनेपदी",  "उभयपदी"]
Tyits = ["सेट्", "अनिट्", "वेट्"]
purushas = ["प्रथमपुरुषः", "मध्यमपुरुषः", "उत्तमपुरुषः"]
vacanas = ['एकवचन', 'द्विवचन', 'बहुवचन']
vibhaktis = ['प्रथमा', 'द्वितीया', 'तृतीया', 'चतुर्थि', 'पंचमि', 'शष्टि', 'सप्तमि', 'सं प्रथम']
lakara = ["लट्", "लिट्", "लुट्", "लृट्", "लोट्", "लङ्", "विधिलिङ्", "अशीर्लिङ्", "लुङ्", "लृङ्"]
voice = ["कर्तरि", "कर्मणि"]
DhatuVidha = ["केवलकृदन्तः", "णिजन्तः", "सन्नन्तः"]


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
def Amarakosha(amaraWord, requested_script=1):
    qry = 'select * from Janani1 where Words like ?'
    param = '%' + amaraWord + '%'
    cols, dbdata = AmaraKosha_Database_Queries.sqlQuery(qry, param, maxrows=0, duplicate=False, script=requested_script)
    # print('%s\n%s' % (cols, dbdata))
    KanWord = [item[cols.index('KanWord')] for item in dbdata]
    EngWord = [item[cols.index('EngWord')] for item in dbdata]
    HinWord = [item[cols.index('HinWord')] for item in dbdata]
    synonyms = (words.split(' ') for words in [r for r in [rec[1] for rec in dbdata] if
                                               AmaraKosha_Database_Queries.iscii_unicode(amaraWord, script=requested_script) in r.split(' ')])
    synonyms = to_2dList(list(synonyms)[0], 4)
    KanWord = [Transliterate.transliterate_lines(item, 'kannada') for item in list(map(lambda i : i or '', KanWord))]
    HinWord = [Transliterate.transliterate_lines(item, 'devanagari') for item in list(map(lambda i : i or '', HinWord))]
    return synonyms, KanWord, EngWord, HinWord
def to_2dList(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]
def Subanta(base, requested_script=1):
    # do sandhi and find vibhakti and vachana forms as per SubGeneration and SubAnalysis in the legacy VB Code
    forms, vacanas, vibhaktis, anta, linga = [],[],[],'',''
    base = str(base)[:-1]
    qry = 'select * from Subanta where Base=?'
    cols, dbdata = AmaraKosha_Database_Queries.sqlQuery(qry, base, maxrows=0, script=requested_script)
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
        cols, dbSufcode = AmaraKosha_Database_Queries.sqlQuery(qry, param, maxrows=0)
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
        subforms_with_sandhi = [AmaraKosha_Database_Queries.iscii_unicode(
            Sandhi_Convt.Sandhi(erb + item + ' '), script=requested_script) for item in subforms]
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
def krdanta_arthas_karmas(krdantaWord, requested_script=1):
    qry = 'select * from Sdhatu where field2 = ?'
    cols, dataDhatu = AmaraKosha_Database_Queries.sqlQuery(qry, krdantaWord, maxrows=0)
    # print('Sdhatu field2=%s %s\n%s'%(krdantaWord, cols, dataDhatu))
    for item in dataDhatu:
        arthas_karmas = item[cols.index('Field8')].split('/')
        arthas = [transliterate_lines(word[:-2], Transliterate.IndianLanguages[requested_script - 1]) for word in arthas_karmas]
        karmas = [int(word[len(word)-1]) - 1 for word in arthas_karmas]
        karmas = [transliterate_lines(Tkarmas[karma], Transliterate.IndianLanguages[requested_script - 1]) for karma in karmas]
        # print('arthas %s\nkarmas %s'%(arthas, karmas))
    dhatuNo = dataDhatu[0][cols.index('Field1') + 1]
    # print('cols %s\nlendata %s\ndataDhatu %s'%(cols,len(dataDhatu),dataDhatu))
    return arthas, karmas, dhatuNo, dataDhatu, cols
def krdanta_Gana(gana, requested_script=1):
    qry = 'select * from Sdhatu where field9 like ?'
    param = str(Tganas.index(gana)) + '__'
    return krdantaResults(qry, param, requested_script)
def krdanta_Padi(padi, requested_script=1):
    qry = 'select * from Sdhatu where field9 like ?'
    param = '_' + str(Tpadis.index(padi) + 1) + '_'
    return krdantaResults(qry, param, requested_script)
def krdanta_Karma(karma, requested_script=1):
    qry = 'select * from Sdhatu where field8 like ?'
    param = '%' + str(Tkarmas.index(karma) + 1) + '%'
    return krdantaResults(qry, param, requested_script)
def krdanta_It(it, requested_script=1):
    qry = 'select * from Sdhatu where field9 like ?'
    param = '__' + str(Tyits.index(it) + 1)
    return krdantaResults(qry, param, requested_script)
def krdantaResults(qry, param, requested_script=1):
    cols, dataDhatu = AmaraKosha_Database_Queries.sqlQuery(qry, param, maxrows=0, script=requested_script)
    # print('Sdhatu param %s %s\n%s'%(param, cols, dataDhatu))
    # return dataDhatu
    arthas, karmas = [], []
    for item in dataDhatu:
        arthas_karmas = item[cols.index('Field8')].split('/')
        # print('arthas_karmas %s'%arthas_karmas)
        arthas += [transliterate_lines(word[:-2], Transliterate.IndianLanguages[requested_script - 1]) for word in arthas_karmas]
        karmaIndex = [int(word[len(word)-1]) - 1 for word in arthas_karmas]
        karmas += [transliterate_lines(Tkarmas[karma], Transliterate.IndianLanguages[requested_script - 1]) for karma in karmaIndex if karma < len(Tkarmas)]
    # print('arthas %s\nkarmas %s'%(arthas, karmas))
    dhatuNo = dataDhatu[0][cols.index('Field1') + 1]
    # print('param %s cols %s\nlendata %s\ndataDhatu %s'%(param, cols,len(dataDhatu),dataDhatu))
    return arthas, karmas, dhatuNo, dataDhatu, cols
def KrdantaGeneration(dhatuNo, DhatuVidah, KrdantaVidah, KrdMode, requested_script=1):
    # pratvidha = ["तव्य",  "अनीयर्",  "य",  "क्त",  "क्तवतु",  "शतृ",  "शानच्",  "स्यशतृ",  "स्यशानच्",  "तुमुन्",  "क्त्वा"].index(dialog.KrdMode.strip())
    # KrdVidha = ["विध्यर्थः",  "भूतः",  "वर्तमानः",  "भविष्यत्",  "कृदव्ययम्"].index(dialog.KrdantaVidah.strip())
    KrdCodeDicts = {"विध्यर्थः": {"तव्य": "a", "अनीयर्": "a", "य": "c"}, "भूतः": {"तव्य": "d", "अनीयर्": "e"},
                    "वर्तमानः": {"तव्य": "f", "अनीयर्": "g"}, "भविष्यत्": {"तव्य": "h", "अनीयर्": "i"}, "कृदव्ययम्": {"तव्य": "A", "अनीयर्": "B"}}
    if not KrdantaVidah == "कृदव्ययम्": KrdCode = KrdCodeDicts[KrdantaVidah][KrdMode] + {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah]
    else: KrdCode = {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah] + KrdCodeDicts[KrdantaVidah][KrdMode]
    krdDatas = []
    forms = []
    qry = 'select * from krud where field4=? and field5=?'
    # print('qry %s param %s'%(qry,(KrdCode, dhatuNo)))
    cols, dataKrud = AmaraKosha_Database_Queries.sqlQuery(qry, (KrdCode, dhatuNo), maxrows=0)
    # print('krud field4=%s field5=%s %s\n%s'%(KrdCode,dhatuNo, cols, dataKrud))
    erbInColumn = cols.index('Field1') + 1  # pick duplicate col
    sabdaInColumn = cols.index('Field3') + 1
    for item in dataKrud:
        krdDataInstance = krdData()
        krdDataInstance.dhatuVidhah = transliterate_lines(DhatuVidah, IndianLanguages[requested_script-1])
        krdDataInstance.krdantaVidhah = transliterate_lines(KrdantaVidah, IndianLanguages[requested_script-1])
        krdDataInstance.pratyayaVidhah = transliterate_lines(KrdMode, IndianLanguages[requested_script-1])
        qry = 'select * from Sufcode where code=?'
        code = item[2][:4]
        for entry in Sandhi_Convt.antas:
            if code[0] == entry[0]:
                krdDataInstance.anta = AmaraKosha_Database_Queries.iscii_unicode(entry[2] + '³ÚÏÚÆèÂ£', requested_script)
                break
        # print('Sufcode: qry %s code %s'%(qry,code))
        cols, dataSufcode = AmaraKosha_Database_Queries.sqlQuery(qry, code, duplicate=False, maxrows=0)
        # print(('sufcode %s cols %s\n%s')%(param, cols, dataSufcode))
        krdDataInstance.erb = item[erbInColumn]
        krdDataInstance.sabda = AmaraKosha_Database_Queries.iscii_unicode(item[sabdaInColumn], requested_script)
        krdDataInstance.linga = AmaraKosha_Database_Queries.iscii_unicode(Sandhi_Convt.lingas[int(code[1])], requested_script)
        suffixes = str(dataSufcode[0][2]).split(' ')
        # from VB SplitAndDisplay routine
        subforms = []
        for sufcode in suffixes:
            subforms.append(Sandhi_Convt.Convt(sufcode))
        # print('subforms %s'%([erb+item for item in subforms]))
        # print([Kosha_Subanta_Synonyms_Queries.iscii_unicode(erb+item) for item in subforms])
        subforms_with_sandhi = [AmaraKosha_Database_Queries.iscii_unicode(
            Sandhi_Convt.Sandhi(krdDataInstance.erb + item), requested_script) for item in subforms]
        # print([Sandhi_Convt.Sandhi(erb + item) for item in subforms])
        forms += [subforms_with_sandhi[0:3], subforms_with_sandhi[3:6], subforms_with_sandhi[6:9],
                 subforms_with_sandhi[9:12], subforms_with_sandhi[12:15], subforms_with_sandhi[15:18],
                 subforms_with_sandhi[18:21], subforms_with_sandhi[21:24]]
        # from VB GetAnalysedInfo routine
        qry = 'Select * from Sdhatu where field1=?'
        cols, dataAnalysed = AmaraKosha_Database_Queries.sqlQuery(qry, dhatuNo, maxrows=0, script=requested_script)
        # print('%s\nData Analysed %s'%(cols, dataAnalysed))
        # for item in dataAnalysed:
        item = dataAnalysed[0]  # there will be only one record!
        krdDataInstance.verb = item[cols.index('Field2')]
        krdDataInstance.nijverb = item[cols.index('Field3')]
        krdDataInstance.sanverb = item[cols.index('Field4')]
        krdDataInstance.GPICode = item[cols.index('Field9')]
        krdDataInstance.gana = transliterate_lines(Tganas[int(krdDataInstance.GPICode[0])], IndianLanguages[requested_script-1])
        krdDataInstance.padi = transliterate_lines(Tpadis[int(krdDataInstance.GPICode[1]) - 1], IndianLanguages[requested_script-1])
        krdDataInstance.it = transliterate_lines(Tyits[int(krdDataInstance.GPICode[2]) - 1], IndianLanguages[requested_script-1])
        krdDataInstance.combinedM = item[cols.index('Field10')]
        krdDatas.append(krdDataInstance)

    # print('no. of items %i subforms with sandhi %s' % (len(forms), forms))
    # for item in krdDatas:
    #     attributes = inspect.getmembers(item, lambda a: not (inspect.isroutine(a)))
    #     print([a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))])
    return forms, vacanas, vibhaktis, krdDatas
def Krdanta_SortedList_KrDantavyayam(dhatuNo, DhatuVidah, KrdantaVidah, KrdMode, dataDhatu, cols_dataDhatu, requested_script=1):
    KrdCodeDicts = {"विध्यर्थः": {"तव्य": "a", "अनीयर्": "a", "य": "c"}, "भूतः": {"तव्य": "d", "अनीयर्": "e"},
                    "वर्तमानः": {"तव्य": "f", "अनीयर्": "g"}, "भविष्यत्": {"तव्य": "h", "अनीयर्": "i"},
                    "कृदव्ययम्": {"तव्य": "A", "अनीयर्": "B"}}
    if not KrdantaVidah == "कृदव्ययम्":KrdCode = KrdCodeDicts[KrdantaVidah][KrdMode] + {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah]
    else: KrdCode = {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah] + KrdCodeDicts[KrdantaVidah][KrdMode]
    krdDatas = []
    forms = []
    qry = 'select * from krudav where field2 = ? and field1 = ?'
    cols, datakrdAvyaya = AmaraKosha_Database_Queries.sqlQuery(qry, (KrdCode, dhatuNo), duplicate=False, maxrows=0, script=requested_script)
    for item in datakrdAvyaya:
        krdDataInstance = krdData()
        krdDataInstance.sabda = item[cols.index('Field3')]
        # print(cols_dataDhatu.index('Field2'), len(dataDhatu))
        krdDataInstance.dhatuVidhah = DhatuVidah
        krdDataInstance.krdantaVidhah = KrdantaVidah
        krdDataInstance.pratyayaVidhah = KrdMode
        krdDataInstance.verb = dataDhatu[0][cols_dataDhatu.index('Field2')]
        krdDataInstance.nijverb = dataDhatu[0][cols_dataDhatu.index('Field3')]
        krdDataInstance.sanverb = dataDhatu[0][cols_dataDhatu.index('Field4')]

        krdDataInstance.GPICode = dataDhatu[0][cols_dataDhatu.index('Field9')]
        krdDataInstance.gana = Tganas[int(krdDataInstance.GPICode[0])]
        krdDataInstance.padi = Tpadis[int(krdDataInstance.GPICode[1]) - 1]
        krdDataInstance.it = Tyits[int(krdDataInstance.GPICode[2]) - 1]
        krdDataInstance.combinedM = dataDhatu[0][cols_dataDhatu.index('Field10')]
        arthas_karmas = dataDhatu[0][cols_dataDhatu.index('Field8')].split('/')
        krdDataInstance.arthas = [word[:-2] for word in arthas_karmas]
        krdDataInstance.karmas = [int(word[len(word) - 1]) for word in arthas_karmas]
        krdDataInstance.karmas = [Tkarmas[karma] for karma in krdDataInstance.karmas]

        # print('arthas %s\nkarmas %s'%(krdDataInstance.arthas, krdDataInstance.karmas))
        krdDatas.append(krdDataInstance)
    return krdDatas

class tiganta:
    def __init__(self):
        self.upasarga, self.tigerr, self.tigsuf = None, None, None
    def get(self):
        return {'tigerr': self.tigerr, 'upasarga': self.upasarga, 'tigsuf:': self.tigsuf}
    def __str__(self):
        return ','.join(self.get())
class tigantaData:
    def __init__(self):
        self.tigform = ''
        self.verb = None
        self.nijverb = None
        self.sanverb = None
        self.GPICode = None
        self.gana = None
        self.padi = None
        self.it = None
        self.dhatuVidhah = None
        self.karma = None
        self.meaning = None
        self.vacana = None
        self.purusha = None
        self.base = None
        self.dhatuVidah = None
        self.lakara = None
        self.Dno = None
    def get(self):
        return {'tigform':self.tigform, 'verb':self.verb, 'nijverb':self.nijverb, 'sanverb':self.sanverb, 'GPICode':self.GPICode, 'gana':self.gana,
                'padi':self.padi, 'it':self.it, 'dhatuVidhah':self.dhatuVidhah, 'pratyayaVidhah':self.pratyayaVidhah, 'karma':self.karma,
                'meaning':self.meaning, 'vacana':self.vacana, 'purusha':self.purusha, 'lakara':self.lakara}
    def __str__(self):
        return ','.join(self.get())
class tigResult:
    def __init__(self):
        self.tigforms = [''] * 9
        self.roopam = None
    def get(self):
        return {'tigforms': self.tigforms, 'roopam': self.roopam}
    def __str__(self):
        return ','.join(self.get())

def TigantaGeneration(dhatuNo, DhatuVidah, voice, lakara, prefixUpasarga = False, requested_script=1):
    lakaraIndex = ["लट्", "लिट्", "लुट्", "लृट्", "लोट्", "लङ्", "विधिलिङ्", "अशीर्लिङ्", "लुङ्", "लृङ्"].index(lakara.strip())
    voiceIndex = ["कर्तरि", "कर्मणि"].index(voice.strip())
    dhatuVidhaIndex = {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah]
    lvstr = dhatuVidhaIndex + chr(2 * lakaraIndex + voiceIndex + ord('A'))
    tigDatas = []
    forms = []
    qry = 'select * from upacode where DhatuNo=?'
    # print('qry %s dhatuNo %s'%(qry,dhatuNo))
    colsUpacode, dataUpacode = AmaraKosha_Database_Queries.sqlQuery(qry, dhatuNo, maxrows=0, script=requested_script)
    # print('upacode dhatuNo=%s %s\n%s'%(dhatuNo, cols, dataUpacode))
    tiggenData = []
    tigDataInstance = tigantaData()
    if len(dataUpacode) == 0:
        tigDataInstance.upasarga = ''
    else:
        upacode = dataUpacode[0][colsUpacode.index('UpaCode') + 1]
        if prefixUpasarga and not upacode == None:
            qry = 'select * from upasarga'
            colsUpasarga, dataUpasarga = AmaraKosha_Database_Queries.sqlQuery(qry, param=None, maxrows=0)
            lstUpa = []
            for ch in upacode:
                for uparec in dataUpasarga:
                    if ord(ch) - ord('a') + 1 == uparec[colsUpasarga.index('ID')]: lstUpa.append[uparec[colsUpasarga.index('ID')]]
    tigDatas.append(tigDataInstance)

    # from VB Function TigantaSetAll
    tiggenDataInstance = tiganta()
    tigResforms = []
    qry = 'select * from stinnew where field2 = ? and field3 like ?'
    colsStinnew, dataStinnew = AmaraKosha_Database_Queries.sqlQuery(qry, (dhatuNo, '%' + lvstr + '%'), maxrows=0)
    for stinrec in dataStinnew:
        tiggenDataInstance.tigerr = stinrec[colsStinnew.index('Field1') + 1]
        tiggenDataInstance.tigsuf = stinrec[colsStinnew.index('Field3') + 1]
        tiggenDataInstance.upasarga = upacode if prefixUpasarga else ''
        tiggenData.append(tiggenDataInstance)
    # VB Function strtgencb
    qry = 'select * from stinfin where field2 = ? and field3 = ?'
    colsStinfin, dataStinfin = AmaraKosha_Database_Queries.sqlQuery(qry, (dhatuNo, lvstr), maxrows=0)
    tigResformsInstance = tigResult()
    for stinfinRec in dataStinfin:
        tigResformsInstance.tigforms[int(colsStinfin.index('Field4'))] = stinfinRec[colsStinfin.index('Field1')]
        tigResforms.append(tigResformsInstance)
    if len(dataStinfin) == 0: tigResforms.append(tigResformsInstance)
    # VB Function tigantaForms
    for tiggenDataInstance in tiggenData:
        words = tiggenDataInstance.tigsuf.split(' ')
        # print('words=%s'%words)
        for word in words:  # only if padi=2 and dhatuVidhaIndex=2?
            tigResformsInstance.roopam = "" if word[:1] == lvstr and dhatuVidhaIndex == 2 else "¥ÂèÌÆáÈÄÛÆÛ ÏÞÈÌè" if word[2] == "0" else "ÈÏ×èÌâÈÄÛÆÛ ÏÞÈÌè "
            suffixCode = word[3:len(word) - len(lvstr)] if dhatuVidhaIndex == 2 and lvstr[1] == "O" else word[2:len(word) - len(lvstr)]
            if word[:2] == lvstr:
                qry = 'select * from stinsuf where field1 = ?'  # VB genTigforms
                colsStinsuf, dataStinsuf = AmaraKosha_Database_Queries.sqlQuery(qry, lvstr[0], maxrows=0)
                for sufrec in dataStinsuf:
                    tstr = sufrec[colsStinsuf.index('Field2')+1].split(' ')
                    # print('tstr=%s\n%s'%(tstr, [AmaraKosha_Subanta_Krdanta_Queries.iscii_unicode(c) for c in tstr]))
                    for x, wrd in enumerate(tstr):
                        if '/' in wrd:
                            subwrd = wrd.split('/')
                            for s in subwrd:
                                tstr1 = blast.performBlast(tiggenDataInstance.tigerr) + blast.performBlast(s)
                                tigantaForm = blast.phoneticallyJoin(tstr1)
                                if tigDataInstance.upasarga != '':
                                    tigantaForm = blast.phoneticallyJoin(
                                        Sandhi_Convt.doSandhiofUpasargaAndTigantaForm(tigantaForm, tigDataInstance.upasarga))
                                tigResformsInstance.tigform[x] += tigantaForm
                        else:
                            tstr1 = blast.performBlast(tiggenDataInstance.tigerr)
                            # print('tstr1=%s %s'%(tstr1, AmaraKosha_Subanta_Krdanta_Queries.iscii_unicode(tstr1)))
                            tstr2 = blast.performBlast(wrd)
                            # print('tstr2=%s %s'%(tstr2, AmaraKosha_Subanta_Krdanta_Queries.iscii_unicode(tstr2)))
                            tstr1 += tstr2
                            tigantaForm = blast.phoneticallyJoin(tstr1)
                            # print('tiganthaform=%s'%AmaraKosha_Subanta_Krdanta_Queries.iscii_unicode(tigantaForm))
                            if not (tiggenDataInstance.upasarga == '' or tiggenDataInstance.upasarga == None):
                                tigantaForm = blast.phoneticallyJoin(
                                    Sandhi_Convt.doSandhiofUpasargaAndTigantaForm(tigantaForm, tiggenDataInstance.upasarga))
                            # print('tiganthaform=%s %s'%(tigantaForm, AmaraKosha_Subanta_Krdanta_Queries.iscii_unicode(tigantaForm)))
                            tigResformsInstance.tigforms[x] += AmaraKosha_Database_Queries.iscii_unicode(tigantaForm, script=requested_script)
    for tigResformsInstance in tigResforms:
        forms += [tigResformsInstance.tigforms[:3], tigResformsInstance.tigforms[3:6], tigResformsInstance.tigforms[6:9]] #to_2dList(tigResformsInstance.tigforms,3)
    # print('tigData %s\n%s\ntiggenData %s\n%s\n tgResforms %s\n%s'%(colsUpacode, tigDatas, colsStinnew, tiggenData, colsStinfin, forms))
    # print('no. of items %i subforms with sandhi %s' % (len(forms), forms))
    # for item in tigDatas:
    #     attributes = inspect.getmembers(item, lambda a: not (inspect.isroutine(a)))
    #     print([a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))])
    return forms, vacanas, purushas, tigDatas




