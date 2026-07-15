__author__ = 'NarasMG'

import json
from typing import List

from source.Controller import Sandhi_Visandhi, Transliterate, blast
from source.Controller.Transliterate import transliterate_lines, IndianLanguages
from source.Model import AmaraKosha_Database_Queries

from source.Controller import constants
Tganas = constants.TGANAS
Tkarmas = constants.TKARMAS
Tpadis = constants.TPADIS
Tyits = constants.TYITS
purushas = constants.PURUSHAS
vacanas = constants.VACANAS
vibhaktis = constants.VIBHAKTIS
lakaras = constants.LAKARAS
voices = constants.VOICES
DhatuVidhas = constants.DHATU_VIDHAS
DhatuVidhasTiganta = constants.DHATU_VIDHAS_TIGANTA
pratyayaVidhahs = constants.PRATYAYA_VIDHAHS
krdantaVidhahs = constants.KRDANTA_VIDHAHS

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

def Amarakosha(amaraWord: str, requested_script="devanagari") -> (List[str], str, str, str):
    qry = 'select * from synonym_groups where Words like ?'
    param = '%' + amaraWord + '%'
    cols, dbSynonymGroups = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param, maxrows=0, script=requested_script)
    synonyms = []
    for rec in dbSynonymGroups:
        wordsSynonymGroups = rec[cols.index('Words')].split(' ')
        # ic.ic(wordsSynonymGroups, [transliterate_lines(word, requested_script) for word in wordsSynonymGroups])
        if amaraWord in wordsSynonymGroups:
            qryMn = 'select * from synonym_groups where ID=?'
            colsMn, dbAmara = AmaraKosha_Database_Queries.sqlQueryUnicode(qryMn, str(rec[cols.index('ID')]), maxrows=0, script=requested_script)

            KanWord = [item[colsMn.index('KanWord')] for item in dbAmara]
            EngWord = [item[colsMn.index('EngWord')] for item in dbAmara]
            HinWord = [item[colsMn.index('HinWord')] for item in dbAmara]
            synonyms.append(to_2dList([transliterate_lines(word, requested_script) for word in wordsSynonymGroups], 4))
            KanWord = [Transliterate.transliterate_lines(item, 'kannada') for item in list(map(lambda i: i or '', KanWord))]
            HinWord = [Transliterate.transliterate_lines(item, 'devanagari') for item in list(map(lambda i: i or '', HinWord))]
    if synonyms == []:
        raise RecordNotFound('No Synonyms found in database(table synonym_groups) for %s'%param)
    return synonyms, KanWord, EngWord, HinWord
def to_2dList(l: int, n: int):
    return [l[i:i + n] for i in range(0, len(l), n)]
def subanta_Generation(base: str, requested_script="devanagari") -> (List[str], str, str):
    try:
        forms, anta, linga = [],'',''
        base = str(base)[:-1]
        qry = 'select * from subanta_forms where base=?'
        cols_subanta, dbdata_subanta = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, base, maxrows=0, script=requested_script)
        if dbdata_subanta == []: raise RecordNotFound('Subanta Generation - No record found for %s - table subanta_forms'%base)
        for row in dbdata_subanta:
            suffixes = []
            erb = row[cols_subanta.index('erb')]
            code = row[cols_subanta.index('code')]
            qry = 'select suffix from nominal_declension_suffix_elements where paradigm_code=? order by position_index'
            cols_sufcode, dbSufcode = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, code[:4], maxrows=0)
            suffixes = [item[0] for item in dbSufcode]
            subforms = []
            for sufcode in suffixes: subforms.append(Sandhi_Visandhi.base36_to_suffix(sufcode))
            subforms_with_sandhi = [transliterate_lines(Sandhi_Visandhi.apply_basic_sandhi(erb + item + ' '), requested_script) for item in subforms]
            if code[0] in Sandhi_Visandhi.antas:
                anta = Sandhi_Visandhi.antas[code[0]] + "ान्तः" if code[0] == 'A' else Sandhi_Visandhi.antas[code[0]] + "कारान्तः"
                anta = transliterate_lines(anta, requested_script)
            linga = transliterate_lines(Sandhi_Visandhi.lingas[int(code[1:2])], requested_script)
            forms = [subforms_with_sandhi[0:3], subforms_with_sandhi[3:6], subforms_with_sandhi[6:9], subforms_with_sandhi[9:12],
                     subforms_with_sandhi[12:15], subforms_with_sandhi[15:18], subforms_with_sandhi[18:21],
                     list(map(lambda word: transliterate_lines('हे', requested_script) + ' ' + word, subforms_with_sandhi[0:3]))]
    except Exception as e:
        print(f"Subanta Generation exception {e}")
    return forms, anta, linga
def query_dhatu_metadata_with_meanings(where_clause: str, param, slice_len: int, requested_script="devanagari"):
    qry = f"""
        SELECT 
            m.seq_id, 
            m.dhatu_id, 
            m.verb_root, 
            m.nijanta_root, 
            m.sannanta_root, 
            '*' as f5, '*' as f6, '*' as f7,
            GROUP_CONCAT(mn.meaning || mn.transitivity_id, '/') AS meanings_list,
            (m.gana_id * 100 + m.padi_id * 10 + m.it_id) AS gpi_code,
            m.combined_meaning
        FROM (
            SELECT ROW_NUMBER() OVER (ORDER BY verb_root) as seq_id, * 
            FROM dhatu_metadata
        ) m
        LEFT JOIN (
            SELECT * 
            FROM dhatu_meanings 
            ORDER BY id
        ) mn ON m.dhatu_id = mn.dhatu_id
        WHERE {where_clause}
        GROUP BY m.dhatu_id
    """
    if param is None: cols, dataDhatu = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param=None, maxrows=0)
    else: cols, dataDhatu = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param, maxrows=0)
        
    if dataDhatu == []:  return [], [], None, [], []
        
    descriptive_cols = ['seq_id', 'dhatu_id', 'verb_root', 'nijanta_root', 'sannanta_root', 'unused5', 'unused6', 'unused7', 'meanings_list', 'gpi_code', 'combined_meaning']
    arthas, karmas = [], []
    for item in dataDhatu:
        meanings_str = item[descriptive_cols.index('meanings_list')]
        if not meanings_str: continue
        arthas_karmas = meanings_str.split('/')
        if slice_len == 1: arthas += [transliterate_lines(w[:-1], requested_script) for w in arthas_karmas]
        else: arthas += [transliterate_lines(w[:-2], requested_script) for w in arthas_karmas]
            
        for w in arthas_karmas:
            try:
                last = int(w[-1])
                karmaIndex = last - 1
                karmas.append(transliterate_lines(Tkarmas[karmaIndex], requested_script))
            except:
                karmas.append(transliterate_lines(Tkarmas[0], requested_script))
                
    dhatuNo = dataDhatu[0][descriptive_cols.index('dhatu_id')]
    return arthas, karmas, dhatuNo, dataDhatu, descriptive_cols

def tiganta_krdanta_arthas_karmas(word: str, requested_script="devanagari") -> (List[str], List[str], str, List[str], List[str]):
    arthas, karmas, dhatuNo, dataDhatu, cols = query_dhatu_metadata_with_meanings("m.verb_root = ?", word, slice_len=1, requested_script=requested_script)
    if dataDhatu == []: raise RecordNotFound('No record found for %s - table dhatu_metadata, function tiganta_krdanta_arthas_karmas'%word)
    return arthas, karmas, dhatuNo, dataDhatu, cols
def krdanta_Gana(gana: str, requested_script="devanagari") -> (List[str], List[str], str, List[str], List[str]):
    gana_idx = Tganas.index(gana)
    if gana_idx > 0:
        qry = 'select * from dhatu_metadata where gana_id = ?'
        param = gana_idx
    else:
        qry = 'select * from dhatu_metadata'
        param = None
    return krdanta_Results(qry, param, requested_script)
def krdanta_Padi(padi: str, requested_script="devanagari") -> (List[str], List[str], str, List[str], List[str]):
    padi_idx = Tpadis.index(padi) + 1
    qry = 'select * from dhatu_metadata where padi_id = ?'
    return krdanta_Results(qry, padi_idx, requested_script)
def krdanta_Karma(karma: str, requested_script="devanagari") -> (List[str], List[str], str, List[str], List[str]):
    karma_idx = Tkarmas.index(karma) + 1
    qry = 'select distinct dm.dhatu_id from dhatu_meanings dm where dm.transitivity_id = ?'
    return krdanta_Results(qry, karma_idx, requested_script)
def krdanta_It(it: str, requested_script="devanagari") -> (List[str], List[str], str, List[str], List[str]):
    it_idx = Tyits.index(it) + 1
    qry = 'select * from dhatu_metadata where it_id = ?'
    return krdanta_Results(qry, it_idx, requested_script)
def krdanta_Results(qry: str, param: str, requested_script="devanagari") -> (List[str], List[str], str, List[str], List[str]):
    if 'gana_id' in qry:
        where_clause = "m.gana_id = ?"
    elif 'padi_id' in qry:
        where_clause = "m.padi_id = ?"
    elif 'it_id' in qry:
        where_clause = "m.it_id = ?"
    elif 'dhatu_meanings' in qry:
        where_clause = "m.dhatu_id IN (SELECT DISTINCT list.dhatu_id FROM dhatu_meanings list WHERE list.transitivity_id = ?)"
    elif 'dhatu_metadata' in qry and param is None:
        where_clause = "1=1"
    else:
        raise Exception("Unrecognized query pattern in krdanta_Results: %s" % qry)

    arthas, karmas, dhatuNo, dataDhatu, cols = query_dhatu_metadata_with_meanings(where_clause, param, slice_len=2, requested_script=requested_script)
    if dataDhatu == []: raise Exception('qry %s parameter %s - empty set  .. function krdanta_Results'%(qry, param))
    return arthas, karmas, dhatuNo, dataDhatu, cols
def krdanta_Generation(dhatuNo: str, DhatuVidah: str, KrdantaVidah: str, KrdMode: str, requested_script="devanagari") -> (List[str], List[krdData]):
    KrdCode = None
    KrdCodeDicts = {"विध्यर्थः": {"तव्य": "a", "अनीयर्": "a", "य": "c"}, "भूतः": {"तव्य": "d", "अनीयर्": "e"},
                    "वर्तमानः": {"तव्य": "f", "अनीयर्": "g"}, "भविष्यत्": {"तव्य": "h", "अनीयर्": "i"}, "कृदव्ययम्": {"तव्य": "A", "अनीयर्": "B"}}
    if not KrdantaVidah == "कृदव्ययम्" and KrdMode in ['तव्य', 'अनीयर्']: KrdCode = KrdCodeDicts[KrdantaVidah][KrdMode] + {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah]
    elif KrdMode in ['तव्य', 'अनीयर्']: KrdCode = {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah] + KrdCodeDicts[KrdantaVidah][KrdMode]
    if KrdCode == None: return [], []
    forms, krdDatas = [], []
    qry = 'select * from krdanta_dictionary where krd_suffix_code=? and dhatu_id=?'
    colsKrud, dataKrud = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, (KrdCode, dhatuNo), maxrows=0)
    erbInColumn = colsKrud.index('sabda_base')
    sabdaInColumn = colsKrud.index('pratipadika')
    for item in dataKrud:
        krdDetail = krdData()
        krdDetail.dhatuVidhah = transliterate_lines(DhatuVidah, requested_script)
        krdDetail.krdantaVidhah = transliterate_lines(KrdantaVidah, requested_script)
        krdDetail.pratyayaVidhah = transliterate_lines(KrdMode, requested_script)
        qry = 'select suffix from nominal_declension_suffix_elements where paradigm_code=? order by position_index'
        code = item[colsKrud.index('vibhakti_vacana_code')][:4]
        if code[0] in Sandhi_Visandhi.antas: krdDetail.anta = transliterate_lines(Sandhi_Visandhi.antas[code[0]] + 'कारान्तः', requested_script)
        cols_sufcode, dataSufcode = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, code, maxrows=0)
        krdDetail.erb = item[erbInColumn]
        krdDetail.sabda = transliterate_lines(item[sabdaInColumn], requested_script)
        krdDetail.linga = transliterate_lines(Sandhi_Visandhi.lingas[int(code[1])], requested_script)
        if dataSufcode != []: suffixes = [row[0] for row in dataSufcode]
        else: return [], None
        subforms = []
        for sufcode in suffixes:
            subforms.append(Sandhi_Visandhi.base36_to_suffix(sufcode))
        subforms_with_sandhi = [transliterate_lines(Sandhi_Visandhi.apply_basic_sandhi(krdDetail.erb + item), requested_script) for item in subforms]
        forms += [subforms_with_sandhi[0:3], subforms_with_sandhi[3:6], subforms_with_sandhi[6:9],
                 subforms_with_sandhi[9:12], subforms_with_sandhi[12:15], subforms_with_sandhi[15:18],
                 subforms_with_sandhi[18:21],
                 list(map(lambda word: transliterate_lines('हे', requested_script) + ' ' + word, subforms_with_sandhi[0:3]))]
        krdDatas.append(getAnalysedinfo(krdDetail, dhatuNo, requested_script))
    if krdDatas: krdDatas[0].erb = transliterate_lines(krdDatas[0].erb, requested_script)
    return forms, krdDatas
def getAnalysedinfo(krdDetail: krdData, dhatuNo: str, requested_script="devanagari"):
    qry = 'Select * from dhatu_metadata where dhatu_id=?'
    cols, dataAnalysed = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, dhatuNo, maxrows=0, script=requested_script)
    if dataAnalysed == []:
        cols, dataAnalysed = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, dhatuNo, maxrows=0)
    arthas, karmas = [], []
    for item in dataAnalysed:
        krdDetail.verb = transliterate_lines(item[cols.index('verb_root')], requested_script)
        krdDetail.nijverb = transliterate_lines(item[cols.index('nijanta_root')], requested_script)
        krdDetail.sanverb = transliterate_lines(item[cols.index('sannanta_root')], requested_script)
        gpi_code = int(f"{item[cols.index('gana_id')]}{item[cols.index('padi_id')]}{item[cols.index('it_id')]}")
        krdDetail.GPICode = gpi_code
        krdDetail.gana = transliterate_lines(Tganas[item[cols.index('gana_id')]], requested_script)
        krdDetail.padi = transliterate_lines(Tpadis[item[cols.index('padi_id')] - 1], requested_script)
        krdDetail.it = transliterate_lines(Tyits[item[cols.index('it_id')] - 1], requested_script)
        krdDetail.CombinedM = item[cols.index('combined_meaning')]
        
        meanings_qry = 'select meaning, transitivity_id from dhatu_meanings where dhatu_id = ?'
        m_cols, m_rows = AmaraKosha_Database_Queries.sqlQueryUnicode(meanings_qry, dhatuNo, maxrows=0)
        m_parts = []
        for m_row in m_rows:
            m_parts.append(f"{m_row[m_cols.index('meaning')]}{m_row[m_cols.index('transitivity_id')]}")
        arthas += [transliterate_lines(word[:-2], requested_script) for word in m_parts]
        karmaCodes = [m_row[m_cols.index('transitivity_id')] - 1 for m_row in m_rows]
        krdDetail.karmaCode = ''.join([str(code) for code in karmaCodes])
        karmas += [transliterate_lines(Tkarmas[karma], requested_script) for karma in karmaCodes if karma < len(Tkarmas)]
        krdDetail.meaning = ' '.join(arthas)
        krdDetail.karma = ' '.join(karmas)
    return krdDetail
def krdanta_SortedList_KrDantavyayam(dhatuNo: str, DhatuVidah: str, KrdantaVidah: str, KrdMode: str, dataDhatu: List[str], cols_dataDhatu: List[str], requested_script="devanagari"):
    KrdCodeDicts = {"विध्यर्थः": {"तव्य": "a", "अनीयर्": "a", "य": "c"}, "भूतः": {"तव्य": "d", "अनीयर्": "e"},
                    "वर्तमानः": {"तव्य": "f", "अनीयर्": "g"}, "भविष्यत्": {"तव्य": "h", "अनीयर्": "i"},
                    "कृदव्ययम्": {"तव्य": "A", "अनीयर्": "B"}}
    if not KrdantaVidah == "कृदव्ययम्":KrdCode = KrdCodeDicts[KrdantaVidah][KrdMode] + {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah]
    else: KrdCode = {"केवलकृदन्तः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah] + KrdCodeDicts[KrdantaVidah][KrdMode]
    krdDatas = []
    dhatu_vidha = int(KrdCode[0])
    krdav_type = KrdCode[1]
    qry = 'select * from krdanta_indeclinables where dhatu_vidha = ? and krdav_type = ? and dhatu_id = ?'
    cols, datakrdAvyaya = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, (dhatu_vidha, krdav_type, dhatuNo), maxrows=0, script=requested_script)
    for item in datakrdAvyaya:
        krdDataInstance = krdData()
        krdDataInstance.sabda = item[cols.index('word')]
        krdDataInstance.dhatuVidhah = DhatuVidah
        krdDataInstance.krdantaVidhah = KrdantaVidah
        krdDataInstance.pratyayaVidhah = KrdMode
        krdDataInstance.verb = dataDhatu[0][cols_dataDhatu.index('Field2')]
        krdDataInstance.nijverb = dataDhatu[0][cols_dataDhatu.index('Field3')]
        krdDataInstance.sanverb = dataDhatu[0][cols_dataDhatu.index('Field4')]
        krdDataInstance.GPICode = dataDhatu[0][cols_dataDhatu.index('Field9')]
        # Extract from GPICode string
        gpi_str = str(krdDataInstance.GPICode).zfill(3)
        krdDataInstance.gana = Tganas[int(gpi_str[0])]
        krdDataInstance.padi = Tpadis[int(gpi_str[1]) - 1]
        krdDataInstance.it = Tyits[int(gpi_str[2]) - 1]
        krdDataInstance.combinedM = dataDhatu[0][cols_dataDhatu.index('Field10')]
        arthas_karmas = dataDhatu[0][cols_dataDhatu.index('Field8')].split('/')
        krdDataInstance.arthas = [word[:-2] for word in arthas_karmas]
        krdDataInstance.karmas = [int(word[len(word) - 1]) for word in arthas_karmas]
        krdDataInstance.karmas = [Tkarmas[karma] for karma in krdDataInstance.karmas]
        krdDatas.append(krdDataInstance)
    return krdDatas

def subanta_Analysis(word, requested_script="devanagari"):
    anusvara = 2306
    if word != '' and ord(word[len(word) - 1]) == anusvara: word = word[:len(word) - 1] + 'म्'
    word_visandhi = Sandhi_Visandhi.split_matras_to_vowels(word)
    halanth = chr(0x094d)
    subDetails = []
    for i in range(len(word_visandhi)-1):
        if not word_visandhi[::-1][i] == halanth:
            subDetail = subantaDetails()
            subDetail.erb = Sandhi_Visandhi.apply_basic_sandhi(word_visandhi[:-(i + 1)])
            subDetail.suf = Sandhi_Visandhi.apply_basic_sandhi(word_visandhi[len(word_visandhi) - (i + 1):])
            subDetails.append(subDetail)
    subforms_with_sandhi = []
    subRecs = []
    for subDetailsRec in subDetails:
        for j, scode in enumerate(Sandhi_Visandhi.Suffix):
            if scode != '' and subDetailsRec.suf == scode:
                chCode = Sandhi_Visandhi.encode_index_base36(j)
                qry = 'select * from subanta_forms where erb = ?'
                if "'" in subDetailsRec.erb:
                    param = subDetailsRec.erb.split("'")
                    param = param[0] + "''" + param[1]
                else: param = subDetailsRec.erb
                cols_subanta, dbdata_subanta = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param, maxrows=0, script=requested_script)
                for subantaDetailRec in dbdata_subanta:
                    if subDetailsRec.erb == subantaDetailRec[cols_subanta.index('erb')]:
                        qry = 'select suffix from nominal_declension_suffix_elements where paradigm_code=? order by position_index'
                        cols_sufcode, dbSufcode = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, subantaDetailRec[cols_subanta.index('code')][:4], maxrows=0, script=requested_script)
                        suffixes = [row[0] for row in dbSufcode]
                        if any(chCode in s for s in suffixes):
                            subforms = []
                            for sufcode in suffixes:
                                if '/' in sufcode:
                                    ss = ''
                                    for s in sufcode.split('/'):
                                        ss += '/' + Sandhi_Visandhi.base36_to_suffix(s)
                                    ss = ss[1:]
                                else:
                                    ss = Sandhi_Visandhi.base36_to_suffix(sufcode)
                                if ss != '': subforms.append(ss)
                            for subformItemNo, subformItem in enumerate(subforms):
                                for tstr in subformItem.split('/'):
                                    if Sandhi_Visandhi.apply_basic_sandhi(subDetailsRec.erb + tstr) == word:
                                        subDetail = subantaDetails()
                                        subDetail.vibvach = subformItemNo
                                        subDetail.vib = transliterate_lines(Sandhi_Visandhi.vibstr[subformItemNo // 3], requested_script)
                                        subDetail.vach = transliterate_lines(Sandhi_Visandhi.vachstr[subformItemNo % 3], requested_script)
                                        subDetail.base = subantaDetailRec[cols_subanta.index('base')]
                                        subDetail.erb = subantaDetailRec[cols_subanta.index('erb')]
                                        subDetail.det = subantaDetailRec[cols_subanta.index('code')]
                                        if subantaDetailRec[cols_subanta.index('code')][0] in Sandhi_Visandhi.antas: subDetail.anta = Sandhi_Visandhi.antas['A'] + "ान्तः" if subantaDetailRec[cols_subanta.index('code')][0] == 'A' else Sandhi_Visandhi.antas[subantaDetailRec[cols_subanta.index('code')][0]] + "कारान्तः"
                                        subDetail.anta = transliterate_lines(subDetail.anta, requested_script)
                                        subDetail.linga = transliterate_lines(Sandhi_Visandhi.lingas[int(subantaDetailRec[cols_subanta.index('code')][1:2])], requested_script)
                                        subDetail.rupam = transliterate_lines(Sandhi_Visandhi.apply_basic_sandhi(subDetailsRec.erb + tstr), requested_script)
                                        subRecs.append(subDetail)
                            subforms_with_sandhi += [Sandhi_Visandhi.apply_basic_sandhi(subDetailsRec.erb + item + ' ') for item in subforms]
    if subforms_with_sandhi == []:
        raise Exception('Subanta Forms for ' + word + ' not found in Database')
    else:
        forms = [subforms_with_sandhi[0:3], subforms_with_sandhi[3:6], subforms_with_sandhi[6:9], subforms_with_sandhi[9:12],
             subforms_with_sandhi[12:15], subforms_with_sandhi[15:18], subforms_with_sandhi[18:21],
             list(map(lambda word: 'हे ' + word, subforms_with_sandhi[0:3]))]
        return forms, subRecs

def krdanta_Analysis(word, requested_script="devanagari"):
    word_visandhi = Sandhi_Visandhi.split_matras_to_vowels(word)
    halanth = chr(0x094d)
    krdAnalyDetails, krdDetails = [], []
    forms = []
    for i in range(len(word_visandhi)-1):
        if not word_visandhi[::-1][i] == halanth:
            krdAnalyDetail = krdAnalyData()
            krdAnalyDetail.erb = Sandhi_Visandhi.apply_basic_sandhi(word_visandhi[:-(i + 1)])
            krdAnalyDetail.suf = Sandhi_Visandhi.apply_basic_sandhi(word_visandhi[len(word_visandhi) - (i + 1):])
            krdAnalyDetails.append(krdAnalyDetail)
    subforms_with_sandhi = []
    for krdAnalyDetail in krdAnalyDetails:
        for j, scode in enumerate(Sandhi_Visandhi.Suffix):
            if scode != '' and krdAnalyDetail.suf == scode:
                chCode = Sandhi_Visandhi.encode_index_base36(j)
                qry = 'select * from krdanta_dictionary where sabda_base = ?'
                cols_krdanta, dataKrdanta = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, krdAnalyDetail.erb, maxrows=0)
                for krdDetailRec in dataKrdanta:
                    qry = 'select suffix from nominal_declension_suffix_elements where paradigm_code=? order by position_index'
                    code = krdDetailRec[cols_krdanta.index('vibhakti_vacana_code')][:4]
                    cols_sufcode, dataSufcode = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, code, maxrows=0)
                    suffixes = [row[0] for row in dataSufcode]
                    if any(chCode in s for s in suffixes):
                        subforms = []
                        for sufcode in suffixes:
                            subforms.append(Sandhi_Visandhi.base36_to_suffix(sufcode))
                        for subformItemNo, subformItem in enumerate(subforms):
                            for tstr in subformItem.split('/'):
                                if Sandhi_Visandhi.apply_basic_sandhi(krdAnalyDetail.erb + tstr) == word:
                                    krdDetail = krdData()
                                    krdDetail.vibvach = subformItemNo
                                    krdDetail.vibhakti = transliterate_lines(Sandhi_Visandhi.vibstr[subformItemNo // 3], requested_script)
                                    krdDetail.vacana = transliterate_lines(Sandhi_Visandhi.vachstr[subformItemNo % 3], requested_script)
                                    krdDetail.sabda = transliterate_lines(krdDetailRec[cols_krdanta.index('pratipadika')], requested_script)
                                    krdDetail.erb = krdDetailRec[cols_krdanta.index('sabda_base')]
                                    krdDetail.det = krdDetailRec[cols_krdanta.index('vibhakti_vacana_code')]
                                    krdDetail.ddet = krdDetailRec[cols_krdanta.index('krd_suffix_code')]
                                    krdDetail.Dno = krdDetailRec[cols_krdanta.index('dhatu_id')]
                                    krdDetail.linga = transliterate_lines(Sandhi_Visandhi.lingas[int(code[1])], requested_script)
                                    if code[0] in Sandhi_Visandhi.antas: krdDetail.anta = transliterate_lines(Sandhi_Visandhi.antas[code[0]] + 'कारान्तः', requested_script)
                                    KrdCode = krdDetailRec[cols_krdanta.index('krd_suffix_code')][0]
                                    krdDetail.pratyayaVidhah = transliterate_lines(pratyayaVidhahs[ord(KrdCode) - ord('a')], requested_script)
                                    krdDetail.dhatuVidhah = transliterate_lines(DhatuVidhas[int(krdDetailRec[cols_krdanta.index('krd_suffix_code')][1])], requested_script)
                                    krdDetail.krdantaVidhah = transliterate_lines(krdantaVidhahs[{'a':0, 'b':0, 'c':0, 'd':1, 'e':1, 'f':2, 'g':2, 'h':3, 'i':3}[KrdCode]], requested_script)
                                    krdDetails.append(getAnalysedinfo(krdDetail, krdDetailRec[cols_krdanta.index('dhatu_id')], requested_script))
                        subforms_with_sandhi += [transliterate_lines(Sandhi_Visandhi.apply_basic_sandhi(krdAnalyDetail.erb + item + ' '), requested_script) for item in subforms]
    if subforms_with_sandhi == []:
        raise Exception('Krdanta Forms for ' + word + ' not found in Database')
    subforms_with_sandhi = [transliterate_lines(item, requested_script) for item in subforms_with_sandhi]
    for grp in range(len(subforms_with_sandhi)//24):
        indx = grp*3
        forms += [subforms_with_sandhi[indx:indx+3], subforms_with_sandhi[indx+3:indx+6],subforms_with_sandhi[indx+6:indx+9],
                  subforms_with_sandhi[indx+9:indx+12],subforms_with_sandhi[indx+12:indx+15], subforms_with_sandhi[indx+15:indx+18],
                  subforms_with_sandhi[indx+18:indx+21], subforms_with_sandhi[indx+21:indx+24]]
    return forms, krdDetails
def tiganta_Analysis(word, requested_script="devanagari"):
    halanth = chr(0x094d)
    tigDatas = []
    qry = 'Select * from tiganta_form_mappings where form=?'
    cols_stinfin, data_stinfin = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, word, maxrows=0, script=requested_script)
    for row in data_stinfin:
        dhatuNo = row[cols_stinfin.index('dhatu_id')]
        d_vidha = row[cols_stinfin.index('dhatu_vidha')]
        l_id = row[cols_stinfin.index('lakara_id')]
        pralak = f"{d_vidha}{chr(l_id + 65)}"
        purvach = row[cols_stinfin.index('purusha_vacana_code')]
        tigDatas.append(WriteAnalysedInformation(pralak, dhatuNo, purvach, word, row[cols_stinfin.index('form')]))
    wordUni = word
    word = blast.performBlast(word)
    tiggenDatas = []
    tigResforms = []
    forms = []
    for i in range(len(word)-1):
        if not word[::-1][i] == halanth:
            tiggenData = tiganta()
            fword = word[:-(i + 1)]
            sword = word[len(word) - (i + 1):]
            tiggenData.tigerr = blast.phoneticallyJoin(fword)
            tiggenData.tigsuf = blast.phoneticallyJoin(sword)
            tiggenDatas.append(tiggenData)

    for tiggenData in tiggenDatas:
        qry = 'select * from tiganta_mappings where form=?'
        cols_stinnew, data_stinnew = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, tiggenData.tigerr, maxrows=0)
        grouped = {}
        for row in data_stinnew:
            form = row[cols_stinnew.index('form')]
            d_id = row[cols_stinnew.index('dhatu_id')]
            d_vidha = row[cols_stinnew.index('dhatu_vidha')]
            l_id = row[cols_stinnew.index('lakara_id')]
            s_code = row[cols_stinnew.index('suffix_code')]
            if d_vidha == 1 and s_code.startswith('1') and chr(l_id + 65) == 'O':
                token = f"O1{s_code[1:]}"
            else:
                token = f"{d_vidha}{chr(l_id + 65)}{s_code}"
            key = (form, d_id)
            if key not in grouped: grouped[key] = []
            grouped[key].append(token)
        
        data_stinnew_legacy = []
        for (form, d_id), tokens in grouped.items():
            data_stinnew_legacy.append([form, d_id, ' '.join(tokens)])
        cols_stinnew_legacy = ['Field1', 'Field2', 'Field3']

        for tiggen in data_stinnew_legacy:
            dhatu = tiggen[cols_stinnew_legacy.index('Field2')]
            suffixStr = tiggen[cols_stinnew_legacy.index('Field3')]
            for sufwrd in suffixStr.split(' '):
                start = 1 if (dhatu==2 and sufwrd[0:1]=='O1') else 2
                scode = sufwrd[start:]
                qry = 'select suffix from tiganta_suffix_elements where suffix_code=? order by position_index'
                cols_stinsuf, data_stinsuf = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, scode, maxrows=0, script=requested_script)
                suffixes = [row[0] for row in data_stinsuf]
                for s, suffix_val in enumerate(suffixes):
                    for sufx in suffix_val.split('/'):
                        if sufx == tiggenData.tigsuf:
                            tigData = WriteAnalysedInformation(sufwrd, dhatu, s, word, tiggen[cols_stinnew_legacy.index('Field1')])
                            tigDatas.append(tigData)
                            tigResform = genTigforms(sufwrd, tigData, tiggenData, tigData.dhatuVidah, tigData.voice, tigData.lakara, requested_script)
                            tigResforms.append(tigResform)
    if tigResforms == []:
        raise Exception('Tiganta Forms for ' + wordUni + ' not found in Database')
    for i, tigResformsInstance in enumerate(tigResforms):
        for j, tigform in enumerate(tigResformsInstance.tigforms):
            tigResformsInstance.tigforms[j] = transliterate_lines(tigform, requested_script)
        tigResforms[i] = tigResformsInstance
    for tigResformsInstance in tigResforms:
        forms += [tigResformsInstance.tigforms[:3], tigResformsInstance.tigforms[3:6], tigResformsInstance.tigforms[6:9]]
    return forms, tigDatas
def WriteAnalysedInformation(pralak, dhatuNo, purvach, word, base, requested_script="devanagari"):
    purusha, vacana = purvach // 3, purvach % 3
    qry = "select * from dhatu_metadata where dhatu_id = ?"
    cols_sdhatu, data_sdhatu = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, dhatuNo, maxrows=0, script=requested_script)
    for item in data_sdhatu:
        tigData = tigantaData()
        tigData.base = base
        tigData.Dno = item[cols_sdhatu.index('dhatu_id')]
        tigData.tigform = word
        tigData.verb = item[cols_sdhatu.index('verb_root')]
        tigData.nijverb = item[cols_sdhatu.index('nijanta_root')]
        tigData.sanverb = item[cols_sdhatu.index('sannanta_root')]
        gpi_code = int(f"{item[cols_sdhatu.index('gana_id')]}{item[cols_sdhatu.index('padi_id')]}{item[cols_sdhatu.index('it_id')]}")
        tigData.GPICode = gpi_code
        tigData.CombinedM = item[cols_sdhatu.index('combined_meaning')]
        tigData.pralak = pralak
        tigData.purvach = purvach + 1
        tigData.purusha = purushas[purusha]
        tigData.vacana = vacanas[vacana]
        
        meanings_qry = 'select meaning, transitivity_id from dhatu_meanings where dhatu_id = ?'
        m_cols, m_rows = AmaraKosha_Database_Queries.sqlQueryUnicode(meanings_qry, dhatuNo, maxrows=0)
        tigData.meaning, tigData.karma = '', ''
        for m_row in m_rows:
            m_val = m_row[m_cols.index('meaning')]
            t_val = m_row[m_cols.index('transitivity_id')]
            tigData.meaning += f"{m_val}{t_val}/"
            karmaIndex = t_val - 1
            tigData.karmaCode = t_val
            tigData.karma += transliterate_lines(Tkarmas[karmaIndex], requested_script)
        gpi_str = str(gpi_code).zfill(3)
        tigData.gana = Tganas[int(gpi_str[0])]
        tigData.padi = Tpadis[int(gpi_str[1]) - 1]
        tigData.it = Tyits[int(gpi_str[2]) - 1]
        tigData.dhatuVidah = DhatuVidhasTiganta[int(pralak[0])-1]
        indx = ord(pralak[1]) - 65
        tigData.lakara = lakaras[indx // 2]
        tigData.voice = voices[indx % 2]
    return tigData

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
def genTigforms(word: str, tigDataInstance: tigantaData, tiggenDataInstance: tiganta, DhatuVidah: str, voice: str, lakara: str, requested_script="devanagari") -> tigResult:
    lakaraIndex = lakaras.index(lakara.strip())
    voiceIndex = voices.index(voice.strip())
    dhatuVidhaIndex = {"केवलतिगंतः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah]
    lvstr = dhatuVidhaIndex + chr(2 * lakaraIndex + voiceIndex + ord('A'))
    tigResformsInstance = tigResult()
    tigResformsInstance.roopam = "" if word[:1] == lvstr and dhatuVidhaIndex == 2 else "आत्मनेपदिनि रूपम्" if word[2] == "0" else "परस्मैपदिनि रूपम् "
    suffixCode = word[3:len(word) - len(lvstr)] if dhatuVidhaIndex == 2 and lvstr[1] == "O" else word[2:len(word) - len(lvstr)]
    if word[:2] == lvstr:
        qry = 'select suffix from tiganta_suffix_elements where suffix_code = ? order by position_index'  # VB genTigforms
        colsStinsuf, dataStinsuf = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, lvstr[0], maxrows=0)
        tstr = [row[0] for row in dataStinsuf]
        for x, wrd in enumerate(tstr):
                if '/' in wrd:
                    subwrd = wrd.split('/')
                    for s in subwrd:
                        tstr1 = blast.performBlast(tiggenDataInstance.tigerr) + blast.performBlast(s)
                        tigantaForm = blast.phoneticallyJoin(tstr1)
                        if tigDataInstance.upasarga != '':
                            tigantaForm = blast.phoneticallyJoin(Sandhi_Visandhi.join_prefix_and_form(tigantaForm, tigDataInstance.upasarga))
                        tigResformsInstance.tigform[x] += tigantaForm
                else:
                    tstr1 = blast.performBlast(tiggenDataInstance.tigerr)
                    tstr2 = blast.performBlast(wrd)
                    tstr1 += tstr2
                    tigantaForm = blast.phoneticallyJoin(tstr1)
                    if not (tiggenDataInstance.upasarga == '' or tiggenDataInstance.upasarga == None):
                        tigantaForm = blast.phoneticallyJoin(Sandhi_Visandhi.join_prefix_and_form(tigantaForm, tiggenDataInstance.upasarga))
                    tigResformsInstance.tigforms[x] += tigantaForm
    return tigResformsInstance
def tiganta_Generation(dhatuNo: str, DhatuVidah: str, voice: str, lakara: str, prefixUpasarga=False, requested_script="devanagari") -> (List[str], List[tigResult]):
    lakaraIndex = lakaras.index(lakara.strip())
    voiceIndex = voices.index(voice.strip())
    dhatuVidhaIndex = {"केवलतिगंतः": "1", "णिजन्तः": "2", "सन्नन्तः": "3"}[DhatuVidah]
    lvstr = dhatuVidhaIndex + chr(2 * lakaraIndex + voiceIndex + ord('A'))
    tigDatas = []
    forms = []
    # Retrieve prefixes from normalized dhatu_upasarga_sequence_elements
    combined_upasarga = ''
    if prefixUpasarga:
        qry = """
            SELECT u.Upasarga 
            FROM dhatu_upasarga_sequence_elements e
            JOIN Upasarga u ON e.upasarga_id = u.ID
            WHERE e.dhatu_id = ?
            ORDER BY e.position_index
        """
        colsUpasarga, dataUpasarga = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, dhatuNo, maxrows=0)
        lstUpa = [row[0] for row in dataUpasarga]
        for upax in lstUpa:
            if combined_upasarga == "":
                combined_upasarga = upax
            else:
                combined_upasarga = Sandhi_Visandhi.join_prefix_and_form(upax, combined_upasarga)

    tiggenData = []
    tigDataInstance = tigantaData()
    tigDataInstance.upasarga = combined_upasarga if prefixUpasarga else ''
    tigDatas.append(tigDataInstance)

    # from VB Function TigantaSetAll
    tiggenDataInstance = tiganta()
    tigResforms = []
    d_vidha = int(lvstr[0])
    l_id = ord(lvstr[1]) - 65
    qry = 'select * from tiganta_mappings where dhatu_id = ? and dhatu_vidha = ? and lakara_id = ?'
    colsStinnew, dataStinnew = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, (dhatuNo, d_vidha, l_id), maxrows=0)
    grouped = {}
    for row in dataStinnew:
        form = row[colsStinnew.index('form')]
        d_id = row[colsStinnew.index('dhatu_id')]
        s_code = row[colsStinnew.index('suffix_code')]
        if d_vidha == 1 and s_code.startswith('1') and chr(l_id + 65) == 'O':
            token = f"O1{s_code[1:]}"
        else:
            token = f"{d_vidha}{chr(l_id + 65)}{s_code}"
        key = (form, d_id)
        if key not in grouped: grouped[key] = []
        grouped[key].append(token)
    
    dataStinnew_legacy = []
    for (form, d_id), tokens in grouped.items():
        dataStinnew_legacy.append([form, d_id, ' '.join(tokens)])
    colsStinnew_legacy = ['Field1', 'Field2', 'Field3']

    for stinrec in dataStinnew_legacy:
        tiggenDataInstance.tigerr = stinrec[colsStinnew_legacy.index('Field1')]
        tiggenDataInstance.tigsuf = stinrec[colsStinnew_legacy.index('Field3')]
        tiggenDataInstance.upasarga = combined_upasarga if prefixUpasarga else ''
        tiggenData.append(tiggenDataInstance)
    # VB Function strtgencb
    qry = 'select * from tiganta_form_mappings where dhatu_id = ? and dhatu_vidha = ? and lakara_id = ?'
    colsStinfin, dataStinfin = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, (dhatuNo, d_vidha, l_id), maxrows=0)
    tigResformsInstance = tigResult()
    for stinfinRec in dataStinfin:
        tigResformsInstance.tigforms[int(stinfinRec[colsStinfin.index('purusha_vacana_code')])] = stinfinRec[colsStinfin.index('form')]
        tigResforms.append(tigResformsInstance)
    # if len(dataStinfin) == 0: tigResforms.append(tigResformsInstance)
    # VB Function tigantaForms
    for tiggenDataInstance in tiggenData:
        words = tiggenDataInstance.tigsuf.split(' ')
        for word in words:  # only if padi=2 and dhatuVidhaIndex=2?
            tigResform = genTigforms(word, tigDataInstance, tiggenDataInstance, DhatuVidah, voice, lakara, requested_script)
            if not tigResform.tigforms == ['']*9: tigResforms.append(tigResform)
    # transliterate to requested script
    for i, tigResformsInstance in enumerate(tigResforms):
        for j, tigform in enumerate(tigResformsInstance.tigforms):
            tigResformsInstance.tigforms[j] = transliterate_lines(tigform, requested_script)
        tigResforms[i] = tigResformsInstance
    for tigResformsInstance in tigResforms: forms += [tigResformsInstance.tigforms[:3], tigResformsInstance.tigforms[3:6], tigResformsInstance.tigforms[6:9]]
    # print('tigData %s\n%s\ntiggenData %s\n%s\n tgResforms %s\n%s'%(colsUpacode, tigDatas, colsStinnew, tiggenData, colsStinfin, forms))
    # print('no. of items %i subforms with sandhi %s' % (len(forms), forms))
    # for item in tigDatas:
    #     attributes = inspect.getmembers(item, lambda a: not (inspect.isroutine(a)))
    #     print([a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))])
    return forms, tigDatas

def generate_krdanta_by_dhatu(dhatu: str, DhatuVidah: str, KrdantaVidah: str, KrdMode: str, requested_script="devanagari"):
    arthas, karmas, dhatuNo, dataDhatu, cols = tiganta_krdanta_arthas_karmas(dhatu, requested_script)
    forms, krd = krdanta_Generation(dhatuNo, DhatuVidah, KrdantaVidah, KrdMode, requested_script)
    return forms, krd, arthas, karmas, dataDhatu, cols

def generate_krdanta_by_option(option: str, parameter: str, DhatuVidah: str, KrdantaVidah: str, KrdMode: str, requested_script="devanagari"):
    options = ['गण', 'पदि', 'कर्म', 'इट्']
    func = [krdanta_Gana, krdanta_Padi, krdanta_Karma, krdanta_It][options.index(option)]
    arthas, karmas, dhatuNo, dataDhatu, cols = func(parameter, requested_script)
    forms, krd = krdanta_Generation(dhatuNo, DhatuVidah, KrdantaVidah, KrdMode, requested_script)
    return forms, krd, arthas, karmas, dataDhatu, cols

def generate_tiganta_by_dhatu(dhatu: str, DhatuVidah: str, voice: str, lakara: str, requested_script="devanagari"):
    arthas, karmas, dhatuNo, dataDhatu, cols = tiganta_krdanta_arthas_karmas(dhatu, requested_script)
    forms, tig = tiganta_Generation(dhatuNo, DhatuVidah, voice, lakara, requested_script=requested_script)
    return forms, tig, arthas, karmas, dataDhatu, cols

def generate_tiganta_by_option(option: str, parameter: str, DhatuVidah: str, voice: str, lakara: str, requested_script="devanagari"):
    options = ['गण', 'पदि', 'कर्म', 'इट्']
    func = [krdanta_Gana, krdanta_Padi, krdanta_Karma, krdanta_It][options.index(option)]
    arthas, karmas, dhatuNo, dataDhatu, cols = func(parameter, requested_script)
    forms, tig = tiganta_Generation(dhatuNo, DhatuVidah, voice, lakara, requested_script=requested_script)
    return forms, tig, arthas, karmas, dataDhatu, cols