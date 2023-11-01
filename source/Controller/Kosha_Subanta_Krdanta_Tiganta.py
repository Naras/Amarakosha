__author__ = 'NarasMG'

import json #, icecream as ic
from typing import List

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
lakaras = ["लट्", "लिट्", "लुट्", "लृट्", "लोट्", "लङ्", "विधिलिङ्", "अशीर्लिङ्", "लुङ्", "लृङ्"]
voices = ["कर्तरि", "कर्मणि"]
DhatuVidhas = ["केवलकृदन्तः", "णिजन्तः", "सन्नन्तः"]
DhatuVidhasTiganta = ["केवलतिगंतः", "णिजन्तः", "सन्नन्तः"]
pratyayaVidhahs = ["तव्य", "अनीयर्", "य", "क्त", "क्तवतु", "शतृ", "शानच्", "स्यशतृ", "स्यशानच्", "तुमुन्", "क्त्वा"]
krdantaVidhahs = ["विध्यर्थः", "भूतः",  "वर्तमानः",   "भविष्यत्",  "कृदव्ययम्"]

class RecordNotFound(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
         return repr(self.value)

class krdData:
    def __init__(self):
        self.anta = None
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
        self.karmaCode = None
        self.karma = None
        self.meaning = None
        self.vibvach = None
        self.vacana = None
        self.vibhakti = None
        self.sabda = None      #KRUD.field3
        self.erb = None        #KRUD.Field1
        self.det = None        #KRUD.field2
        self.ddet = None        #KRUD.field4
        self.Dno = None        #int(KRUD.Field5)
        self.CombinedM = None  #KRUD.field10
    def get(self):
        return {'anta': self.anta, 'linga': self.linga, 'verb': self.verb, 'nijverb': self.nijverb, 'sanverb': self.sanverb, 'GPICode': self.GPICode, 'gana': self.gana,
                'padi': self.padi, 'it': self.it, 'dhatuVidhah': self.dhatuVidhah, 'krdantaVidhah': self.krdantaVidhah, 'combinedM': self.combinedM,
                'wtype': self.wtype, 'pratyayaVidhah': self.pratyayaVidhah, 'karmaCode': self.karmaCode, 'karma': self.karma, 'meaning': self.meaning, 'vibvach': self.vibvach,
                'vacana': self.vacana, 'vibhakti': self.vibhakti, 'sabda': self.sabda, 'erb': self.erb, 'det': self.det, 'ddet': self.ddet, 'Dno': self.Dno}
    def __str__(self):
        return json.dumps(self.get())
class krdAnalyData:
    def __init__(self):
        self.erb = None
        self.suf = None
    def get(self):
        return {'erb':self.erb, 'suf':self.suf}
    def __str__(self):
        return json.dumps(self.get())
class subantaDetails:
    def __init__(self):
        self.base, self.vib, self.vach, self.anta, self.linga, self.rupam, self.erb, self.vibvach, self.det, self.wtype = '', '', '', '', '', '', '', '', '', None
        self.subforms = ['']*23
    def get(self):
        return {'base': self.base, 'vib': self.vib, 'vach':self.vach, 'rupam': self.rupam, 'erb': self.erb, 'vibvach': self.vibvach, 'det': self.det, 'wtype': self.wtype}
    def __str__(self):
        return json.dumps(self.get())
class subAnalBase:
    def __init__(self):
        self.erb, self.suf = '', ''
    def get(self):
        return {'erb':self.erb, 'suf':self.suf}
    def __str__(self):
        return json.dumps(self.get())

def Amarakosha(amaraWord: str, requested_script=1) -> (List[str], str, str, str):
    qry = 'select * from Janani1 where Words like ?'
    param = '%' + amaraWord + '%'
    cols, dbJanani1 = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param, maxrows=0, script=requested_script)
    synonyms = []
    for rec in dbJanani1:
        wordsJanani1 = rec[cols.index('Words')].split(' ')
        # ic.ic(wordsJanani1, [transliterate_lines(word, IndianLanguages[requested_script-1]) for word in wordsJanani1])
        if amaraWord in wordsJanani1:
            qryMn = 'select * from Janani1 where ID=?'
            colsMn, dbAmara = AmaraKosha_Database_Queries.sqlQueryUnicode(qryMn, str(rec[cols.index('ID')]), maxrows=0, script=requested_script)

            KanWord = [item[colsMn.index('KanWord')] for item in dbAmara]
            EngWord = [item[colsMn.index('EngWord')] for item in dbAmara]
            HinWord = [item[colsMn.index('HinWord')] for item in dbAmara]
            synonyms.append(to_2dList([transliterate_lines(word, IndianLanguages[requested_script-1]) for word in wordsJanani1], 4))
            KanWord = [Transliterate.transliterate_lines(item, 'kannada') for item in list(map(lambda i: i or '', KanWord))]
            HinWord = [Transliterate.transliterate_lines(item, 'devanagari') for item in list(map(lambda i: i or '', HinWord))]
    if synonyms == []:
        raise RecordNotFound('No Synonyms found in database(table Janani1) for %s'%param)
    return synonyms, KanWord, EngWord, HinWord
def to_2dList(l: int, n: int):
    return [l[i:i + n] for i in range(0, len(l), n)]
def subanta_Generation(base: str, requested_script=1) -> (List[str], str, str):
    # do sandhi and find vibhakti and vachana forms as per SubGeneration and SubAnalysis in the legacy VB Code
    forms, anta, linga = [],'',''
    base = str(base)[:-1]
    qry = 'select * from Subanta where Base=?'
    cols_subanta, dbdata_subanta = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, base, maxrows=0, script=requested_script)
    if dbdata_subanta == []: raise RecordNotFound('Subanta Generation - No record found for %s - table Subanta'%base)
    for row in dbdata_subanta:
        suffixes = []
        erb = row[cols_subanta.index('Erb')]
        code = row[cols_subanta.index('Code')]
        qry = 'select * from Sufcode where code=?'
        cols_sufcode, dbSufcode = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, code[:4], maxrows=0)
        for item in dbSufcode: suffixes += str(item[cols_sufcode.index('SufStr')]).split(" ")
        subforms = []
        for sufcode in suffixes: subforms.append(Sandhi_Convt.Convt(sufcode))
        subforms_with_sandhi = [transliterate_lines(Sandhi_Convt.Sandhi(erb + item + ' '), IndianLanguages[requested_script - 1]) for item in subforms]
        if code[0] in Sandhi_Convt.antas:
            anta = Sandhi_Convt.antas[code[0]] + "ान्तः" if code[0] == 'A' else Sandhi_Convt.antas[code[0]] + "कारान्तः"
            anta = transliterate_lines(anta, IndianLanguages[requested_script - 1])
        linga = transliterate_lines(Sandhi_Convt.lingas[int(code[1:2])], IndianLanguages[requested_script - 1])
        forms = [subforms_with_sandhi[0:3], subforms_with_sandhi[3:6], subforms_with_sandhi[6:9], subforms_with_sandhi[9:12],
                 subforms_with_sandhi[12:15], subforms_with_sandhi[15:18], subforms_with_sandhi[18:21],
                 list(map(lambda word: transliterate_lines('हे', IndianLanguages[requested_script - 1]) + ' ' + word, subforms_with_sandhi[0:3]))]
    return forms, anta, linga
def tiganta_krdanta_arthas_karmas(word: str, requested_script=1) -> (List[str], List[str], str, List[str], List[str]):
    qry = 'select * from Sdhatu where field2 = ?'
    cols, dataDhatu = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, word, maxrows=0)
    if dataDhatu == []: raise RecordNotFound('No record found for %s - table Sdhatu, function tiganta_krdanta_arthas_karmas'%word)
    if len(dataDhatu) > 1: print('function tiganta_krdanta_arthas_karmas - Sdhatu data %d, is this ok? dataDhata %s'%(len(dataDhatu), dataDhatu[:2]))
    for item in dataDhatu:
        arthas_karmas = item[cols.index('Field8')].split('/')
        arthas = [transliterate_lines(word[:-1], Transliterate.IndianLanguages[requested_script - 1]) for word in arthas_karmas]
        karmas = [int(word[len(word)-1]) - 1 for word in arthas_karmas]
        karmas = [transliterate_lines(Tkarmas[karma], Transliterate.IndianLanguages[requested_script - 1]) for karma in karmas]
    dhatuNo = dataDhatu[0][cols.index('Field1')]
    return arthas, karmas, dhatuNo, dataDhatu, cols
def krdanta_Gana(gana: str, requested_script=1) -> (List[str], List[str], str, List[str], List[str]):
    qry = 'select * from Sdhatu where cast(field9 as text) like ?'
    param = str(Tganas.index(gana)) + '__' if Tganas.index(gana) > 0 else '__'
    return krdanta_Results(qry, param, requested_script)
def krdanta_Padi(padi: str, requested_script=1) -> (List[str], List[str], str, List[str], List[str]):
    qry = 'select * from Sdhatu where cast(field9 as text) like ?'
    param = '_' + str(Tpadis.index(padi) + 1) + '_'
    return krdanta_Results(qry, param, requested_script)
def krdanta_Karma(karma: str, requested_script=1) -> (List[str], List[str], str, List[str], List[str]):
    qry = 'select * from Sdhatu where field8 like ?'
    param = '%' + str(Tkarmas.index(karma) + 1) + '%'
    return krdanta_Results(qry, param, requested_script)
def krdanta_It(it: str, requested_script=1) -> (List[str], List[str], str, List[str], List[str]):
    qry = 'select * from Sdhatu where cast(field9 as text) like ?'
    param = '__' + str(Tyits.index(it) + 1)
    return krdanta_Results(qry, param, requested_script)
def krdanta_Results(qry: str, param: str, requested_script=1) -> (List[str], List[str], str, List[str], List[str]):
    cols, dataDhatu = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param, maxrows=0, script=requested_script)
    if dataDhatu == []: raise Exception('qry %s parameter %s - empty set  .. function krdanta_Results'%(qry, param))
    arthas, karmas = [], []
    try:
        for item in dataDhatu:
            arthas_karmas = item[cols.index('Field8')].split('/')
            arthas += [transliterate_lines(word[:-2], Transliterate.IndianLanguages[requested_script - 1]) for word in arthas_karmas]
            karmas = []
            for word in arthas_karmas:
                try:
                    last = int(word[-1])
                    karmaIndex = last - 1
                    karmas.append(transliterate_lines(Tkarmas[karmaIndex], Transliterate.IndianLanguages[requested_script - 1]))
                except:
                    karmas.append(transliterate_lines(Tkarmas[0], Transliterate.IndianLanguages[requested_script - 1]))
            # ic.ic(karmas, arthas, karmaIndex, arthas_karmas)
        dhatuNo = dataDhatu[0][cols.index('Field1')]
    except Exception as e:
        # ic.ic(karmas, arthas, len(karmas), len(arthas), karmaIndex, arthas_karmas, e, item)
        raise Exception(str(e) + ' .. problem in field ' + arthas_karmas + ' - function krdanta_Results')
    return arthas, karmas, dhatuNo, dataDhatu, cols
def krdanta_Generation(dhatuNo: str, DhatuVidah: str, KrdantaVidah: str, KrdMode: str, requested_script=1) -> (List[str], List[krdData]):
    # pratvidha = ["तव्य",  "अनीयर्",  "य",  "क्त",  "क्तवतु",  "शतृ",  "शानच्",  "स्यशतृ",  "स्यशानच्",  "तुमुन्",  "क्त्वा"].index(dialog.KrdMode.strip())
    # KrdVidha = ["विध्यर्थः",  "भूतः",  "वर्तमानः",  "भविष्यत्",  "कृदव्ययम्"].index(dialog.KrdantaVidah.strip())
    KrdCode = None
    KrdCodeDicts = {"विध्यर्थः": {"तव्य": "a", "अनीयर्": "a", "य": "c"}, "भूतः": {"तव्य": "d", "अनीयर्": "e"},
                    "वर्तमानः": {"तव्य": "f", "अनीयर्": "g"}, "भविष्यत्": {"तव्य": "h", "अनीयर्": "i"}, "कृदव्ययम्": {"तव्य": "A", "अनीयर्": "B"}}
    if not KrdantaVidah == "कृदव्ययम्" and KrdMode in ['तव्य', 'अनीयर्']: KrdCode = KrdCodeDicts[KrdantaVidah][KrdMode] + {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah]
    elif KrdMode in ['तव्य', 'अनीयर्']: KrdCode = {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah] + KrdCodeDicts[KrdantaVidah][KrdMode]
    if KrdCode == None: return [], []
    forms, krdDatas = [], []
    qry = 'select * from krud where field4=? and field5=?'
    # print('qry %s param %s'%(qry,(KrdCode, dhatuNo)))
    colsKrud, dataKrud = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, (KrdCode, dhatuNo), maxrows=0)
    # print('krud field4=%s field5=%s %s\n%s'%(KrdCode, dhatuNo, cols, dataKrud))
    erbInColumn = colsKrud.index('Field1')
    sabdaInColumn = colsKrud.index('Field3')
    for item in dataKrud:
        krdDetail = krdData()
        krdDetail.dhatuVidhah = transliterate_lines(DhatuVidah, IndianLanguages[requested_script-1])
        krdDetail.krdantaVidhah = transliterate_lines(KrdantaVidah, IndianLanguages[requested_script-1])
        krdDetail.pratyayaVidhah = transliterate_lines(KrdMode, IndianLanguages[requested_script-1])
        qry = 'select * from Sufcode where code=?'
        # if len(item) < 2: return [], None
        code = item[colsKrud.index('Field2')][:4]
        if code[0] in Sandhi_Convt.antas: krdDetail.anta = transliterate_lines(Sandhi_Convt.antas[code[0]] + 'कारान्तः', IndianLanguages[requested_script - 1])
        cols, dataSufcode = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, code, maxrows=0)
        # print(('krdGener sufcode %s cols %s\n%s')%(code, cols, dataSufcode))
        krdDetail.erb = item[erbInColumn]
        krdDetail.sabda = transliterate_lines(item[sabdaInColumn], IndianLanguages[requested_script - 1])
        krdDetail.linga = transliterate_lines(Sandhi_Convt.lingas[int(code[1])], IndianLanguages[requested_script - 1])
        if dataSufcode != [] and len(dataSufcode[0]) > 2: suffixes = str(dataSufcode[0][2]).split(' ')
        else: return [], None
        # from VB SplitAndDisplay routine
        subforms = []
        for sufcode in suffixes:
            subforms.append(Sandhi_Convt.Convt(sufcode))
        # print('subforms %s'%([erb+item for item in subforms]))
        # print([Kosha_Subanta_Synonyms_Queries.iscii_unicode(erb+item) for item in subforms])
        subforms_with_sandhi = [transliterate_lines(Sandhi_Convt.Sandhi(krdDetail.erb + item), IndianLanguages[requested_script - 1]) for item in subforms]
        # print('krdanta gen %s'%[Sandhi_Convt.Sandhi(krdDetail.erb + item) for item in subforms])
        forms += [subforms_with_sandhi[0:3], subforms_with_sandhi[3:6], subforms_with_sandhi[6:9],
                 subforms_with_sandhi[9:12], subforms_with_sandhi[12:15], subforms_with_sandhi[15:18],
                 subforms_with_sandhi[18:21],
                 list(map(lambda word: transliterate_lines('हे', IndianLanguages[requested_script - 1]) + ' ' + word, subforms_with_sandhi[0:3]))]
                  # subforms_with_sandhi[21:24]]
        krdDatas.append(getAnalysedinfo(krdDetail, dhatuNo, requested_script))

    # print('no. of items %i subforms with sandhi %s' % (len(forms), forms))
    # for item in krdDatas:
    #     attributes = inspect.getmembers(item, lambda a: not (inspect.isroutine(a)))
    #     print([a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))])
    return forms, krdDatas
def getAnalysedinfo(krdDetail: krdData, dhatuNo: str, requested_script=1):
    # from VB GetAnalysedInfo routine
    qry = 'Select * from Sdhatu where field1=?'
    cols, dataAnalysed = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, dhatuNo, maxrows=0, script=requested_script)
    if dataAnalysed == []: # qry failed due to iscii akshara in non-Devanagari ... try Devanagari
        cols, dataAnalysed = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, dhatuNo, maxrows=0)
    # print('getAnalysedinfo cols %s\nData Analysed %s'%(cols, dataAnalysed))
    # for item in dataAnalysed:
    arthas, karmas = [], []
    for item in dataAnalysed:  # there will be only one record!
        krdDetail.verb = item[cols.index('Field2')]
        krdDetail.nijverb = transliterate_lines(item[cols.index('Field3')], IndianLanguages[requested_script - 1])
        krdDetail.sanverb = transliterate_lines(item[cols.index('Field4')], IndianLanguages[requested_script - 1])
        krdDetail.GPICode = item[cols.index('Field9')]
        krdDetail.gana = transliterate_lines(Tganas[krdDetail.GPICode // 100], IndianLanguages[requested_script - 1])
        krdDetail.padi = transliterate_lines(Tpadis[(krdDetail.GPICode % 100) // 10 - 1], IndianLanguages[requested_script - 1])
        krdDetail.it = transliterate_lines(Tyits[krdDetail.GPICode % 10 - 1], IndianLanguages[requested_script - 1])
        krdDetail.CombinedM = item[cols.index('Field10')]
        arthas_karmas = item[cols.index('Field8')].split('/')
        # print('getAnalysedinfo arthas_karmas %s'%arthas_karmas)
        arthas += [transliterate_lines(word[:-2], Transliterate.IndianLanguages[requested_script - 1]) for word in arthas_karmas]
        karmaCodes = [int(word[len(word)-1]) - 1 for word in arthas_karmas]
        krdDetail.karmaCode = ''.join([str(code) for code in karmaCodes])
        karmas += [transliterate_lines(Tkarmas[karma], Transliterate.IndianLanguages[requested_script - 1]) for karma in karmaCodes if karma < len(Tkarmas)]
        krdDetail.meaning = ' '.join(arthas)
        krdDetail.karma = ' '.join(karmas)
    return krdDetail
def krdanta_SortedList_KrDantavyayam(dhatuNo: str, DhatuVidah: str, KrdantaVidah: str, KrdMode: str, dataDhatu: List[str], cols_dataDhatu: List[str], requested_script=1):
    KrdCodeDicts = {"विध्यर्थः": {"तव्य": "a", "अनीयर्": "a", "य": "c"}, "भूतः": {"तव्य": "d", "अनीयर्": "e"},
                    "वर्तमानः": {"तव्य": "f", "अनीयर्": "g"}, "भविष्यत्": {"तव्य": "h", "अनीयर्": "i"},
                    "कृदव्ययम्": {"तव्य": "A", "अनीयर्": "B"}}
    if not KrdantaVidah == "कृदव्ययम्":KrdCode = KrdCodeDicts[KrdantaVidah][KrdMode] + {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah]
    else: KrdCode = {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah] + KrdCodeDicts[KrdantaVidah][KrdMode]
    krdDatas = []
    forms = []
    qry = 'select * from krudav where field2 = ? and field1 = ?'
    cols, datakrdAvyaya = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, (KrdCode, dhatuNo), maxrows=0, script=requested_script)
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

def subanta_Analysis(word, requested_script=1):
    anusvara = 2306
    # print('word %s %s'%(word, AmaraKosha_Database_Queries.iscii_unicode(word)))
    if word != '' and ord(word[len(word) - 1]) == anusvara: word = word[:len(word) - 1] + 'म्'  # Ìè
    qry ='select * from subfin where Finform=?'
    cols_subfin, dbdata_subfin = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, word, maxrows=0, script=requested_script)
    for row in dbdata_subfin:
        codes = row[cols_subfin.index('Code')]
        subDetail = subantaDetails()
        subDetails = []
        for codeset in codes.split(' '):
            subDetail.vibvach = int(codeset.split(',')[1]) - 1
            subDetail.vib = Sandhi_Convt.vibstr[subDetail.vibvach//3]
            subDetail.vach = Sandhi_Convt.vachstr[subDetail.vibvach%3]
            subDetail.linga = Sandhi_Convt.lingas[int(codeset[1:2])]
            if codeset[0] in Sandhi_Convt.antas: subDetail.anta = Sandhi_Convt.antas[codeset[0]] + "ान्तः" if codeset[0] == 'A' else Sandhi_Convt.antas[codeset[0]] + "कारान्तः"
            subDetail.wtype = 1
            qry = 'select * from fincode where code like ?'
            cols_fincode, dbdata_fincode = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, codeset[0]+'__', maxrows=0, script=requested_script)
            for sufrec in dbdata_fincode:
                if sufrec[cols_fincode.index('code')][:3] == codeset[0]:
                    subDetail.base = sufrec[cols_fincode.index('finroot')]
                    subDetail.det = sufrec[cols_fincode.index('code')]
                    subDetail.erb = None
                    subDetails.append(subDetail)
    # wrd = AmaraKosha_Database_Queries.unicode_iscii(word)
    # print('subanaly about to do visandhi %s(%s) %s %s'%(word, AmaraKosha_Database_Queries.unicode_iscii(word), [ord(ch) for ch in word], [hex(ord(ch)) for ch in word]))
    word_visandhi = Sandhi_Convt.visandhi(word)
    # ic.ic(word, word_visandhi, AmaraKosha_Database_Queries.iscii_unicode(word),AmaraKosha_Database_Queries.iscii_unicode(word_visandhi))
    # print('subAnaly-visandhi word %s(%s) visandhi %s %s'%(word, AmaraKosha_Database_Queries.unicode_iscii(word), word_visandhi, AmaraKosha_Database_Queries.iscii_unicode(word_visandhi)))
    halanth = chr(0x094d)   # AmaraKosha_Database_Queries.iscii_unicode(chr(232))
    subDetails = []
    for i in range(len(word_visandhi)-1):
        # print('visandhi left %s'%word_visandhi[::-1][i])
        if not word_visandhi[::-1][i] == halanth:
            subDetail = subantaDetails()
            subDetail.erb = Sandhi_Convt.Sandhi(word_visandhi[:-(i+1)])
            subDetail.suf = Sandhi_Convt.Sandhi(word_visandhi[len(word_visandhi)-(i+1):])
            # print('subAnaly 1 erb %s -> %s(%s) suf %s -> %s(%s)'%(word_visandhi[:-(i+1)], AmaraKosha_Database_Queries.unicode_iscii(subDetail.erb), subDetail.erb, word_visandhi[len(word_visandhi)-(i+1):], AmaraKosha_Database_Queries.unicode_iscii(subDetail.suf), subDetail.suf))
            # splits += 1
            subDetails.append(subDetail)
    # print('subAnaly 2 erb', [det.erb for det in subDetails], 'suf', [[AmaraKosha_Database_Queries.unicode_iscii(det.suf), det.suf] for det in subDetails])
    subforms_with_sandhi = []
    subRecs = []
    for subDetailsRec in subDetails:
        # print('subAnaly erb %s(%s) suf %s(%s)' % (AmaraKosha_Database_Queries.unicode_iscii(subDetailsRec.erb), subDetailsRec.erb, AmaraKosha_Database_Queries.unicode_iscii(subDetailsRec.suf), subDetailsRec.suf))
        for j, scode in enumerate(Sandhi_Convt.Suffix):
            if scode != '' and subDetailsRec.suf == scode:
                chCode = Sandhi_Convt.decode(j)
                # ic.ic(j, scode, AmaraKosha_Database_Queries.iscii_unicode(scode), chCode)
                qry = 'select * from subanta where erb = ?'
                if "'" in subDetailsRec.erb:
                    param = subDetailsRec.erb.split("'")
                    param = param[0] + "''" + param[1]
                else: param = subDetailsRec.erb
                # print('param %s %s'%(AmaraKosha_Database_Queries.unicode_iscii(param), param))
                cols_subanta, dbdata_subanta = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param, maxrows=0, script=requested_script)
                for subantaDetailRec in dbdata_subanta:
                    if subDetailsRec.erb == subantaDetailRec[cols_subanta.index('Erb')]:
                        qry = 'select * from sufcode where code=?'
                        cols_sufcode, dbSufcode = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, subantaDetailRec[cols_subanta.index('Code')][:4], maxrows=0, script=requested_script)
                        subforms = []
                        for sufrec in dbSufcode:
                            if sufrec[cols_sufcode.index('Code')] == subantaDetailRec[cols_subanta.index('Code')][:4]:
                                sufixes = sufrec[cols_sufcode.index('SufStr')]
                                if chCode in sufixes:
                                    for sufcode in sufixes.split(' '):
                                        if '/' in sufcode:
                                            ss = ''
                                            for s in sufcode.split('/'):
                                                ss += '/' + Sandhi_Convt.Convt(s)
                                            ss = ss[1:]
                                        else:
                                            ss = Sandhi_Convt.Convt(sufcode)
                                        if ss != '': subforms.append(ss)
                                    for subformItemNo, subformItem in enumerate(subforms):
                                        for tstr in subformItem.split('/'):
                                            if Sandhi_Convt.Sandhi(subDetailsRec.erb + tstr) == word:
                                                subDetail = subantaDetails()
                                                subDetail.vibvach = subformItemNo
                                                subDetail.vib = transliterate_lines(Sandhi_Convt.vibstr[subformItemNo // 3], IndianLanguages[requested_script - 1])
                                                subDetail.vach = transliterate_lines(Sandhi_Convt.vachstr[subformItemNo % 3], IndianLanguages[requested_script - 1])
                                                subDetail.base = subantaDetailRec[cols_subanta.index('Base')]
                                                subDetail.erb = subantaDetailRec[cols_subanta.index('Erb')]
                                                subDetail.det = subantaDetailRec[cols_subanta.index('Code')]
                                                if subantaDetailRec[cols_subanta.index('Code')][0] in Sandhi_Convt.antas: subDetail.anta = Sandhi_Convt.antas['A'] + "ान्तः" if subantaDetailRec[cols_subanta.index('Code')][0] == 'A' else Sandhi_Convt.antas[subantaDetailRec[cols_subanta.index('Code')][0]] + "कारान्तः"
                                                subDetail.anta = transliterate_lines(subDetail.anta, IndianLanguages[requested_script - 1])
                                                subDetail.linga = transliterate_lines(Sandhi_Convt.lingas[int(subantaDetailRec[cols_subanta.index('Code')][1:2])], IndianLanguages[requested_script - 1])
                                                subDetail.rupam = transliterate_lines(Sandhi_Convt.Sandhi(subDetailsRec.erb + tstr), IndianLanguages[requested_script - 1])
                                                subRecs.append(subDetail)
                            # print([erb+item for item in subforms])
                            # print([AmaraKosha_Database_Queries.iscii_unicode(subDetails[i].erb+item) for item in subforms])
                            subforms_with_sandhi += [Sandhi_Convt.Sandhi(subDetailsRec.erb + item + ' ') for item in subforms]
                # print(len(subforms_with_sandhi),subforms_with_sandhi)
    subforms_with_sandhi = [transliterate_lines(item, IndianLanguages[requested_script - 1]) for item in subforms_with_sandhi]
    if subforms_with_sandhi == []:
        raise Exception('Subanta Forms for ' + word + ' not found in Database')
    else:
        forms = [subforms_with_sandhi[0:3], subforms_with_sandhi[3:6], subforms_with_sandhi[6:9], subforms_with_sandhi[9:12],
             subforms_with_sandhi[12:15], subforms_with_sandhi[15:18], subforms_with_sandhi[18:21],
             # subforms_with_sandhi[21:24]]
             list(map(lambda word: 'हे ' + word, subforms_with_sandhi[0:3]))]
        return forms, subRecs
def krdanta_Analysis(word, requested_script=1):
    word_visandhi = Sandhi_Convt.visandhi(word)
    halanth = chr(0x094d)  # chr(232)
    krdAnalyDetails, krdDetails = [], []
    forms = []
    for i in range(len(word_visandhi)-1):
        if not word_visandhi[::-1][i] == halanth:
            krdAnalyDetail = krdAnalyData()
            krdAnalyDetail.erb = Sandhi_Convt.Sandhi(word_visandhi[:-(i + 1)])
            krdAnalyDetail.suf = Sandhi_Convt.Sandhi(word_visandhi[len(word_visandhi) - (i + 1):])
            # print('krdAnaly erb %s -> %s(%s) suf %s -> %s(%s)'%(word_visandhi[:-(i+1)], krdAnalyDetail.erb,AmaraKosha_Database_Queries.iscii_unicode(krdAnalyDetail.erb), word_visandhi[len(word_visandhi)-(i+1):], krdAnalyDetail.suf, AmaraKosha_Database_Queries.iscii_unicode(krdAnalyDetail.suf)))
            krdAnalyDetails.append(krdAnalyDetail)
    subforms_with_sandhi = []
    for krdAnalyDetail in krdAnalyDetails:
        for j, scode in enumerate(Sandhi_Convt.Suffix):
            if scode != '' and krdAnalyDetail.suf == scode:
                chCode = Sandhi_Convt.decode(j)
                # print('chcode %s j %s scode %s'%(chCode, j, scode))
                qry = 'select * from Krud where Field1 = ?'
                cols_krdanta, dataKrdanta = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, krdAnalyDetail.erb, maxrows=0)
                for krdDetailRec in dataKrdanta:
                    qry = 'select * from Sufcode where code=?'
                    code = krdDetailRec[cols_krdanta.index('Field2')][:4]
                    # print('krdAnaly Sufcode: qry %s code %s' % (qry, code))
                    cols_sufcode, dataSufcode = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, code, maxrows=0)
                    subforms = []
                    for sufrec in dataSufcode:
                        if sufrec[cols_sufcode.index('Code')] == code:
                            sufixes = sufrec[cols_sufcode.index('SufStr')]
                            if chCode in sufixes:
                                for sufcode in sufixes.split(' '):
                                    subforms.append(Sandhi_Convt.Convt(sufcode))
                                # print('krdAnaly 1 subforms %s'%subforms)
                                for subformItemNo, subformItem in enumerate(subforms):
                                    for tstr in subformItem.split('/'):
                                        if Sandhi_Convt.Sandhi(krdAnalyDetail.erb + tstr) == word:
                                            krdDetail = krdData()
                                            krdDetail.vibvach = subformItemNo
                                            krdDetail.vibhakti = transliterate_lines(Sandhi_Convt.vibstr[subformItemNo // 3], IndianLanguages[requested_script - 1])
                                            krdDetail.vacana = transliterate_lines(Sandhi_Convt.vachstr[subformItemNo % 3], IndianLanguages[requested_script - 1])
                                            krdDetail.sabda = transliterate_lines(krdDetailRec[cols_krdanta.index('Field3')], IndianLanguages[requested_script-1])
                                            krdDetail.erb = krdDetailRec[cols_krdanta.index('Field1')]
                                            krdDetail.det = krdDetailRec[cols_krdanta.index('Field2')]
                                            krdDetail.ddet = krdDetailRec[cols_krdanta.index('Field4')]
                                            krdDetail.Dno = krdDetailRec[cols_krdanta.index('Field5')]
                                            krdDetail.linga = transliterate_lines(Sandhi_Convt.lingas[int(code[1])], IndianLanguages[requested_script - 1])
                                            if code[0] in Sandhi_Convt.antas: krdDetail.anta = transliterate_lines(Sandhi_Convt.antas[code[0]] + 'कारान्तः', IndianLanguages[requested_script - 1])
                                            KrdCode = krdDetailRec[cols_krdanta.index('Field4')][0]
                                            krdDetail.pratyayaVidhah = transliterate_lines(pratyayaVidhahs[ord(KrdCode) - ord('a')], IndianLanguages[requested_script-1])
                                            krdDetail.dhatuVidhah = transliterate_lines(DhatuVidhas[int(krdDetailRec[cols_krdanta.index('Field4')][1])], IndianLanguages[requested_script-1])
                                            krdDetail.krdantaVidhah = transliterate_lines(krdantaVidhahs[{'a':0, 'b':0, 'c':0, 'd':1, 'e':1, 'f':2, 'g':2, 'h':3, 'i':3}[KrdCode]], IndianLanguages[requested_script-1])

                                            krdDetails.append(getAnalysedinfo(krdDetail, krdDetailRec[cols_krdanta.index('Field5')], requested_script))
                                subforms_with_sandhi += [transliterate_lines(Sandhi_Convt.Sandhi(krdAnalyDetail.erb + item + ' '), IndianLanguages[requested_script - 1]) for item in subforms]
                        # print('krdAnaly %i %s'%(len(subforms_with_sandhi),subforms_with_sandhi))
    if subforms_with_sandhi == []:
        raise Exception('Krdanta Forms for ' + word + ' not found in Database')
    subforms_with_sandhi = [transliterate_lines(item, IndianLanguages[requested_script - 1]) for item in subforms_with_sandhi]
    for grp in range(len(subforms_with_sandhi)//24):
        indx = grp*3
        forms += [subforms_with_sandhi[indx:indx+3], subforms_with_sandhi[indx+3:indx+6],subforms_with_sandhi[indx+6:indx+9],
                  subforms_with_sandhi[indx+9:indx+12],subforms_with_sandhi[indx+12:indx+15], subforms_with_sandhi[indx+15:indx+18],
                  subforms_with_sandhi[indx+18:indx+21], subforms_with_sandhi[indx+21:indx+24]]
    # ic.ic(AmaraKosha_Database_Queries.iscii_unicode(word), len(subforms_with_sandhi), subforms_with_sandhi, len(forms), forms)
    return forms, krdDetails
def tiganta_Analysis(word, requested_script=1):
    halanth = chr(0x094d)  # chr(232)
    tigDatas = []
    qry = 'Select * from stinfin where Field1=?'
    cols_stinfin, data_stinfin = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, word, maxrows=0, script=requested_script)
    # if data_stinfin != []: ic(cols_stinfin, data_stinfin)
    for row in data_stinfin:
        dhatuNo = row[cols_stinfin.index('Field2')]
        pralak = row[cols_stinfin.index('Field3')]
        purvach = row[cols_stinfin.index('Field4')]
        tigDatas = WriteAnalysedInformation(pralak, dhatuNo, purvach, word, row[cols_stinfin.index('Field1')])
    wordUni = word
    word = blast.performBlast(word)
    # ic.ic(word, wordUni, tigDatas)
    tiggenDatas = []
    tigResforms = []
    forms = []
    for i in range(len(word)-1):  #from VB SplitTheWord function
        if not word[::-1][i] == halanth:
            tiggenData = tiganta()
            fword = word[:-(i + 1)]
            sword = word[len(word) - (i + 1):]
            tiggenData.tigerr = blast.phoneticallyJoin(fword)
            tiggenData.tigsuf = blast.phoneticallyJoin(sword)
            # ic.ic(tiggenData.get())
            tiggenDatas.append(tiggenData)

    for tiggenData in tiggenDatas: #VB Function searchForError
        qry = 'select * from stinnew where field1=?'
        cols_stinnew, data_stinnew = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, tiggenData.tigerr)
        # ic.ic(tiggenData.tigerr, cols_stinnew, data_stinnew)
        for tiggen in data_stinnew:
            dhatu = tiggen[cols_stinnew.index('Field2')]
            suffixStr = tiggen[cols_stinnew.index('Field3')]
            for sufwrd in suffixStr.split(' '):  #VB Function SearcForSuffix
                start = 1 if (dhatu==2 and sufwrd[0:1]=='O1') else 2
                scode = sufwrd[start:]
                qry = 'select * from stinsuf where Field1=?'
                cols_stinsuf, data_stinsuf = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, scode, script=requested_script)
                # ic.ic(scode, cols_stinsuf, data_stinsuf)
                for sufrec in data_stinsuf:
                    for sufxStr in sufrec[cols_stinsuf.index('Field2')].split('/'):
                        for s, sufx in enumerate(sufxStr.split(' ')):
                          if sufx == tiggenData.tigsuf:
                            tigData = WriteAnalysedInformation(sufwrd, dhatu, s, word, tiggen[cols_stinnew.index('Field1')])
                            tigDatas.append(tigData)
                            tigResform = genTigforms(sufwrd, tigData, tiggenData, tigData.dhatuVidah, tigData.voice, tigData.lakara, requested_script)
                            tigResforms.append(tigResform)
    if tigResforms == []:
        raise Exception('Tiganta Forms for ' + wordUni + ' not found in Database')
    for tigResformsInstance in tigResforms:
        forms += [tigResformsInstance.tigforms[:3], tigResformsInstance.tigforms[3:6], tigResformsInstance.tigforms[6:9]]
    return forms, tigDatas
def WriteAnalysedInformation(pralak, dhatuNo, purvach, word, base, requested_script=1):
    purusha, vacana = purvach // 3, purvach % 3
    qry = "select * from sdhatu where field1 = ?"
    cols_sdhatu, data_sdhatu = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, dhatuNo, maxrows=0, script=requested_script)
    # tigDatas = []
    for tigDetRec in data_sdhatu:
        tigData = tigantaData()
        tigData.base = base
        tigData.Dno = tigDetRec[cols_sdhatu.index('Field1')]
        tigData.tigform = word
        tigData.verb = tigDetRec[cols_sdhatu.index('Field2')]
        tigData.nijverb = tigDetRec[cols_sdhatu.index('Field3')]
        tigData.sanverb = tigDetRec[cols_sdhatu.index('Field4')]
        tigData.GPICode = tigDetRec[cols_sdhatu.index('Field9')]
        tigData.CombinedM = tigDetRec[cols_sdhatu.index('Field10')]
        tigData.pralak = pralak
        tigData.purvach = purvach + 1
        tigData.purusha = purushas[purusha]
        tigData.vacana = vacanas[vacana]
        tigData.meaning, tigData.karma = '', ''
        for arthas_karmas in tigDetRec[cols_sdhatu.index('Field8')].split('/'):
            tigData.meaning += arthas_karmas + '/'
            karmaIndex = int(arthas_karmas[len(arthas_karmas) - 1]) - 1
            tigData.karmaCode = karmaIndex + 1
            tigData.karma += transliterate_lines(Tkarmas[karmaIndex], Transliterate.IndianLanguages[requested_script - 1])
        tigData.gana = Tganas[tigData.GPICode // 100]   #  int(tigData.GPICode[0]
        tigData.padi = Tpadis[(tigData.GPICode % 100) // 10 - 1]
        tigData.it = Tyits[(tigData.GPICode % 100) % 10 - 1]
        tigData.dhatuVidah = DhatuVidhasTiganta[int(pralak[0])-1]
        indx = ord(pralak[1]) - 65
        tigData.lakara = lakaras[indx // 2]
        tigData.voice = voices[indx % 2]
        # tigDatas.append(tigData)
    return tigData  # only one

class tiganta:
    def __init__(self):
        self.upasarga, self.tigerr, self.tigsuf = None, None, None
    def get(self):
        return {'tigerr': self.tigerr, 'upasarga': self.upasarga, 'tigsuf:': self.tigsuf}
    def __str__(self):
        return json.dumps(self.get())
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
        self.karmaCode = None
        self.karma = None
        self.meaning = None
        self.purvach = None
        self.vacana = None
        self.purusha = None
        self.base = None
        self.dhatuVidah = None
        self.pralak = None
        self.lakara = None
        self.Dno = None
        self.combinedM = None
        self.voice = None
    def get(self):
        return {'tigform':self.tigform, 'verb':self.verb, 'nijverb':self.nijverb, 'sanverb':self.sanverb, 'GPICode':self.GPICode, 'gana':self.gana,
                'padi':self.padi, 'it':self.it, 'dhatuVidah':self.dhatuVidah, 'karma':self.karma,
                'meaning':self.meaning, 'vacana':self.vacana, 'purusha':self.purusha, 'purvach':self.purvach, 'lakaras':self.lakara}
    def __str__(self):
        return json.dumps(self.get())
class tigResult:
    def __init__(self):
        self.tigforms = [''] * 9
        self.roopam = None
    def get(self):
        return {'tigforms': self.tigforms, 'roopam': self.roopam}
    def __str__(self):
        return json.dumps(self.get())
def genTigforms(word: str, tigDataInstance: tigantaData, tiggenDataInstance: tiganta, DhatuVidah: str, voice: str, lakara: str, requested_script=1) -> tigResult:
    lakaraIndex = lakaras.index(lakara.strip())
    voiceIndex = voices.index(voice.strip())
    dhatuVidhaIndex = {"केवलतिगंतः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah]
    lvstr = dhatuVidhaIndex + chr(2 * lakaraIndex + voiceIndex + ord('A'))
    tigResformsInstance = tigResult()
    tigResformsInstance.roopam = "" if word[:1] == lvstr and dhatuVidhaIndex == 2 else "आत्मनेपदिनि रूपम्" if word[2] == "0" else "परस्मैपदिनि रूपम् "
    suffixCode = word[3:len(word) - len(lvstr)] if dhatuVidhaIndex == 2 and lvstr[1] == "O" else word[2:len(word) - len(lvstr)]
    if word[:2] == lvstr:
        qry = 'select * from stinsuf where field1 = ?'  # VB genTigforms
        colsStinsuf, dataStinsuf = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, lvstr[0], maxrows=0)
        for sufrec in dataStinsuf:
            tstr = sufrec[colsStinsuf.index('Field2')].split(' ')
            for x, wrd in enumerate(tstr):
                if '/' in wrd:
                    subwrd = wrd.split('/')
                    for s in subwrd:
                        tstr1 = blast.performBlast(tiggenDataInstance.tigerr) + blast.performBlast(s)
                        tigantaForm = blast.phoneticallyJoin(tstr1)
                        if tigDataInstance.upasarga != '':
                            tigantaForm = blast.phoneticallyJoin(Sandhi_Convt.doSandhiofUpasargaAndTigantaForm(tigantaForm, tigDataInstance.upasarga))
                        tigResformsInstance.tigform[x] += tigantaForm
                else:
                    tstr1 = blast.performBlast(tiggenDataInstance.tigerr)
                    tstr2 = blast.performBlast(wrd)
                    tstr1 += tstr2
                    tigantaForm = blast.phoneticallyJoin(tstr1)
                    if not (tiggenDataInstance.upasarga == '' or tiggenDataInstance.upasarga == None):
                        tigantaForm = blast.phoneticallyJoin( Sandhi_Convt.doSandhiofUpasargaAndTigantaForm(tigantaForm, tiggenDataInstance.upasarga))
                    tigResformsInstance.tigforms[x] += tigantaForm
    return tigResformsInstance
def tiganta_Generation(dhatuNo: str, DhatuVidah: str, voice: str, lakara: str, prefixUpasarga=False, requested_script=1) -> (List[str], List[tigResult]):
    lakaraIndex = lakaras.index(lakara.strip())
    voiceIndex = voices.index(voice.strip())
    dhatuVidhaIndex = {"केवलतिगंतः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah]
    lvstr = dhatuVidhaIndex + chr(2 * lakaraIndex + voiceIndex + ord('A'))
    tigDatas = []
    forms = []
    qry = 'select * from upacode where DhatuNo=?'
    # print('qry %s dhatuNo %s'%(qry,dhatuNo))
    colsUpacode, dataUpacode = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, dhatuNo, maxrows=0, script=requested_script)
    # print('upacode dhatuNo=%s %s\n%s'%(dhatuNo, colsUpacode, dataUpacode))
    tiggenData = []
    tigDataInstance = tigantaData()
    if len(dataUpacode) == 0:
        tigDataInstance.upasarga = ''
    else:
        upacode = dataUpacode[0][colsUpacode.index('UpaCode')]
        if prefixUpasarga and not upacode == None:
            qry = 'select * from upasarga'
            colsUpasarga, dataUpasarga = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param=None, maxrows=0)
            lstUpa = []
            for ch in upacode:
                for uparec in dataUpasarga:
                    if ord(ch) - ord('a') + 1 == uparec[colsUpasarga.index('ID')]: lstUpa.append[uparec[colsUpasarga.index('ID')]]
    tigDatas.append(tigDataInstance)

    # from VB Function TigantaSetAll
    tiggenDataInstance = tiganta()
    tigResforms = []
    qry = 'select * from stinnew where field2 = ? and field3 like ?'
    colsStinnew, dataStinnew = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, (dhatuNo, '%' + lvstr + '%'), maxrows=0)
    for stinrec in dataStinnew:
        tiggenDataInstance.tigerr = stinrec[colsStinnew.index('Field1')]
        tiggenDataInstance.tigsuf = stinrec[colsStinnew.index('Field3')]
        tiggenDataInstance.upasarga = upacode if prefixUpasarga else ''
        tiggenData.append(tiggenDataInstance)
    # VB Function strtgencb
    qry = 'select * from stinfin where field2 = ? and field3 = ?'
    colsStinfin, dataStinfin = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, (dhatuNo, lvstr), maxrows=0)
    tigResformsInstance = tigResult()
    for stinfinRec in dataStinfin:
        tigResformsInstance.tigforms[int(colsStinfin.index('Field4'))] = stinfinRec[colsStinfin.index('Field1')]
        tigResforms.append(tigResformsInstance)
    # if len(dataStinfin) == 0: tigResforms.append(tigResformsInstance)
    # VB Function tigantaForms
    for tiggenDataInstance in tiggenData:
        words = tiggenDataInstance.tigsuf.split(' ')
        for word in words:  # only if padi=2 and dhatuVidhaIndex=2?
            tigResform = genTigforms(word, tigDataInstance, tiggenDataInstance, DhatuVidah, voice, lakara, requested_script)
            if not tigResform.tigforms == ['']*9: tigResforms.append(tigResform)
    for tigResformsInstance in tigResforms: forms += [tigResformsInstance.tigforms[:3], tigResformsInstance.tigforms[3:6], tigResformsInstance.tigforms[6:9]]
    # print('tigData %s\n%s\ntiggenData %s\n%s\n tgResforms %s\n%s'%(colsUpacode, tigDatas, colsStinnew, tiggenData, colsStinfin, forms))
    # print('no. of items %i subforms with sandhi %s' % (len(forms), forms))
    # for item in tigDatas:
    #     attributes = inspect.getmembers(item, lambda a: not (inspect.isroutine(a)))
    #     print([a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))])
    return forms, tigDatas
def nishpatthi(amaraWord: str) -> List[str]:
    qry = 'select Nishpatti from N_Sanskrit N, Amara_Words A where N.IdNo = A.ID and A.Word = ?'
    # print('amaraword:', amaraWord)
    cols, dbdata = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param=amaraWord, maxrows=0)
    return dbdata
def vyutpatthi(amaraWord:str, language='Sanskrit') -> List[str]:
    table = ['V_Sanskrit', 'V_Hindi', 'V_Odiya'][['Sanskrit', 'Hindi', 'Odiya'].index(language)]
    qry = 'select Vytpatti from '+ table + ' V, Amara_Words A where V.IdNo = A.ID and A.Word = ?'
    # print('amaraword:', amaraWord)
    cols, dbdata = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param=amaraWord, maxrows=0)
    return dbdata
def avyayaAnalysis(word: str, requested_script=1) -> List[str]:
    qry = 'select * from avyaya where field2=?'
    cols, avySuffix = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param=word, maxrows=0, script=requested_script)
    avyayas =[]
    for avyaya in avySuffix:
        avyaya.inpword = word
        avyaya.Avycode = avySuffix[cols.index('Field1') + 1]
        avyayas.append(avyaya)
    return avyayas