#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, icecream as ic
from typing import List, TextIO
maxstrlen = 100
halant = 'è'
eof = chr(255)

#SENGEN1,h
class subanta_data:
    def __init__(self):
        self.erb = [None] * 10  # List[str]
        self.base = [None] * 10  # List[str]
        self.code = None  # str
        self.count = None  # int
    def get(self):
        return {'erb':self.erb, 'base': self.base, 'code': self.code, 'count': self.count}
    def __str__(self):
        return json.dumps(self.get())
class tiganta_form:
    def __init__(self):
        self.form = None  # str
        self.artha = None  # str
        self.mode = None  # str
        self.karma = None  # str
        self.voice = None  # str
        self.purusha = None  # str
        self.vacana = None  # str
        self.numOfForms = None  # str
    def get(self):
        return {'form':self.form, 'artha': self.artha, 'mode':self.mode, 'karma':self.karma, 'voice':self.voice, 'purusha':self.purusha, 'vacana':self.vacana, 'numOfForms':self.numOfForms}
    def __str__(self):
        return json.dumps(self.get())
#DATA.H
class detail:
    def __init__(self):
        self.type = None  # str
        self.stem = None  # str
        self.code = [None] * 20  # List[str]
        self.subcode = None  # str
        self.specf = None  # str
        self.dispSpecf = None  # str
        self.mean_deno = None  # str
        self.word = None  # str
        self.stem = None  # str
        self.base= [None] * 20   # List[str]
        self.voice = None  # str
        self.linga = None  # int
        self.vibvach = None  # int
        self.mode = None  # int
        self.sub_no = None  # int
        self.no_base = None  # int
        self.no_codes = None  # int
        self.pos = None  # int
        self.matnoun = None  # int
        self.subinsen = None  # int
    def get(self):
        return {'type':self.type, 'code':self.code, 'specf':self.specf, 'dispSpecf':self.dispSpecf, 'mean_deno':self.mean_deno, 'word':self.word,
                    'stem':self.stem, 'base':self.base, 'voice':self.voice, 'linga':self.linga, 'vibvach':self.vibvach, 'mode':self.mode,
                    'sub_no':self.sub_no, 'no_base':self.no_base, '':self.no_codes, 'pos':self.pos, 'matnoun':self.matnoun, 'subinsen':self.subinsen}
    def __str__(self):
        return json.dumps(self.get())
class shasti:
    def __init__(self):
        self.specf = None  # str
        self.word = None  # str
        self.base = [None] * 8  # List[str]
        self.code = [None] * 8  # str
        self.sub_no = None  # str
        self.no_base = None  # str
    def get(self):
        return {'specf': self.specf, 'word': self.word, 'base': self.base[8], 'code': self.code, 'sub_no': self.sub_no, 'no_base': self.no_base}
    def __str__(self):
        return json.dumps(self.get())
class vibak:
    def __init__(self):
        self.arthaword = None  # str
        self.sent = None  # str
        self.specf = None  # str
        self.mean_deno = None  # str
        self.sword = None  # str
        self.bword = None  # str
        self.lword = None  # str
        self.ltype = None  # str
        self.stype = None  # str
        self.semlinga = None  # int
        self.spos = None  # int
        self.lpos = None  # int
        self.matnoun = None  # int
    def get(self):
        return {'arthaword':self.arthaword, 'sent':self.sent, 'specf':self.specf, 'mean_deno':self.mean_deno, 'sword':self.sword, 'bword':self.bword, 'lword':self.lword, 'ltype':self.ltype, 'stype':self.stype, 'semlinga':self.semlinga, 'spos':self.spos, 'lpos':self.lpos, 'matnoun':self.matnoun}
    def __str__(self):
        return json.dumps(self.get())
class display:
    def __init__(self):
        self.dispSpecf = None  # str
        self.Type = None  # str
        self.meanword = None  # str
        self.word = None  # str
        self.bword = None  # str
        self.mean_deno = None  # str
        self.stype = None  # str
        self.pos = None  # int
        self.disppos = None  # int
    def get(self):
        return {'dispSpecf':self.dispSpecf, 'Type':self.Type, 'meanword':self.meanword, 'word':self.word, 'bword':self.bword, 'mean_deno':self.mean_deno, 'pos':self.pos, 'disppos':self.disppos}
    def __str__(self):
        return json.dumps(self.get())
class disp_shasti:
    def __init__(self):
        self.specf = None  # str
        self.word = None  # str
    def get(self):
        return {'specf':self.specf, 'word':self.word}
    def __str__(self):
        return json.dumps(self.get())
class Menu:
    def __init__(self):
        self.items = [None] * 19  # List[str]
        self.count = None  # int
    def get(self):
        return {'items':self.items, 'count':self.count}
    def __str__(self):
        return json.dumps(self.get())
class LinkedList:
    def __init__(self, instance=None):
        if instance != None:
            self.__head == instance
            self.__allinstances.append(self.__head)
        else:
            self.__head == None
            self.__allinstances = []
    def __next__(self):
        if self.__next == None: raise StopIteration
        return self.__next
    def __iter__(self):
        return self
    def append(self, instance=None):
        if instance != None:
            self.__next == instance
            self.__allinstances.append(self.__next)
    def get(self):
        self.__head.get()
    def set(self, instance):
        self.__head = instance
    def getall(self):
        return [instance.get() for instance in self.__allinstances]
    def isEmpty(self):
        return True if self.__head == None else False
    def __str__(self):
        return json.dumps(self.getall())
class SPLIT:
    def __init__(self):
        self.firstword = [None] * 10  # str
        self. secondWord = [None] * 10 # str
        self.noofsplits = None
    def get(self):
        return {"firstWord":self.firstword, "secondWord":self.secondWord, "noofsplits":self.noofsplits}
    def __str__(self):
        return json.dumps(self.get())
def CheckMatchingNounForKrdanta(dfirst: List[detail]) -> (List[str], List[str], List[str], str):
    subform, genword = None, [None]*10
    rec, temptr, temptr1, newrec = detail(), detail(), detail(), None
    specfs = ["Subject", "Object","Instrument","Dative","Ablative", "Genitive","Locative","Vocative"]
    records = []
    for record in dfirst:
        record.matnoun = 0
        records.append(record)
    for rec in records:
        if rec.type == "Krdanta":
            temptr = rec
            if rec.specf == "Subject" and rec.type == "Noun": rec.matnoun = 1
            genword = "ÂÄè"
            if rec.matnoun == 0 and rec.specf == "Vocative":
                subform = getSubantaForm(rec.vibvach - 1, rec.subcode)
                temptr = dfirst[0]
                for i, specf in enumerate(specfs):
                    if specf == rec.specf: break
                for j in range(8):
                    if temptr.type == "Noun" and temptr.specf == specfs[j]:
                        if j > i: break
                        else: continue
                    break
                newrec = detail()
                newrec.type, newrec.specf, newrec.dispSpecf, newrec.voice, newrec.word, newrec.stem = \
                    "Noun", rec.specf, rec.dispSpecf, rec.voice, subform, "ÆÏ"
                newrec.linga, newrec.vibvach, newrec.mode, newrec.sub_no, newrec.no_base, newrec.no_codes, newrec.pos, newrec.matnoun, \
                newrec.subinsen = 0, 0, 0, 0, 0, 0, 0, 0, 0
    return records, temptr, subform, genword
def AssignSubCode(dfirst: detail,ifp: List[str]) -> List[str]:
    wordpos = 0
    records = []
    if dfirst.type == "Krdanta" and dfirst.specf == "Subject":
        for line in ifp:
            if line[0] == "\n": pass
            elif line[0] == "-": break
            word = line[:-1].split()
            if dfirst.specf == "Vocative":
                if word[2] != "3" and word[2] in ["1", "2"]:
                    record.subcode = word[5]
                    record.stem = word[3]
                    record.vibvach = int[word[6]]
                    record.pos = wordpos
                    break
            else:
                VocWord = "Øá " + word[0]
                if dfirst.word in [word[0], VocWord]:
                    if word[2] != "3" and word[2] in ["1", "2"]:
                        dfirst.subcode = word[5]
                        dfirst.stem = word[3]
                        dfirst.vibvach = int[word[6]]
                        dfirst.pos = wordpos
                        break
    records.append(dfirst)
    return records
def Assignsub(dfirst: detail, temptr: detail, ifp: List[str]) -> List[str]:
    for record in dfirst:
        if record.type == "Krdanta" and record.specf == "Subject":
            for line in ifp:
                if line[0] == "\n": pass
                elif line[0] == "-": break
                word = line[:-1].split()
                # num = len(word)
                if word[2] == "2":
                    if word[5][0] == "0":
                        temptr.word = ["×Ú", "Âá", "ÂÚ£"][int(word[6])]
                    elif word[5][0] == "1":
                        temptr.word = ["×£", "Âæ", "Âá"][int(word[6])]
                    elif word[5][0] == "2":
                        temptr.word = ["×ÂèÂ", "Âá", "ÂÚÆÛ"][int(word[6])]
                    temptr.stem = "ÆÏ"
                    temptr.linga, temptr.vibvach = 0, 0
        elif record.type == "Verb":
            for line in ifp:
                if line[0] == "\n": pass
                elif line[0] == "-": break
                word = line[:-1].split()
                # num = len(word)
                if word[2] == "5":
                    if word[5][0] == "0":
                        temptr.word = ["×£", "Âæ", "Âá"][int(word[11])]
                    temptr.stem = "ÆÏ"
                    temptr.linga, temptr.vibvach = 0, 0
    return temptr
def getSubantaForm(pvIndex: int, code: str) -> List[str]:
    return [[Form004, Form104, Form204][['004', '104', '204'].index(code + 1)]][pvIndex]
def searchroot(ifp_lines: List[str], afp_lines: List[str], rfp_lines: List[str], sfp_lines: List[str], Efp_lines: List[str], drecords: List[detail], sen: str, y: int) -> int:
    ans, upaflag, noofupa, Saflag, bodha = False, False, None, False, False
    specfs = ["Subject", "Object", "Instrument", "Dative", "Ablative", "Locative", "Genitive", "Avyaya", "Vocative", "Verb", "Krdanta", "Krdavyaya"]
    spefMean = ["³ÏèÂÚ", "³ÏèÌ", "³ÏÁÌè", "×ÌèÈèÏÄÚÆÌè", "¤ÈÚÄÚÆÌè", "¤ÄÛ³ÏÁÌè", "ÖÖè¾Û"]
    temp, vfirst, kfirst, sfirst, krdfirst, krdavy = None, None, None, None, None, None
    fshtptr, sshtptr = shasti(), shasti()
    # alst = open("r")
    no_words, wordpos = 0, 0
    for line in ifp_lines:
        wordpos += 1
        if line[0] == "-":
            bodha = False if Saflag else True
            for temp in drecords:
                if temp.type == "Noun" and temp.specf == "Subject" and temp.subinsen == 0:
                    drecord = Assignlingavib(drecord)
            ans = getcode(drecords, Efp_lines)
            if not ans: return False
            temp = drecords[0]
            if temp.specf == "Subject":
                sfirst = temp
                if temp.no_base == 0: temp.no_base, temp.sub_no, temp.mean_deno, temp.code[0], temp.base[0] = 1, 0, "³ÏèÂÚ", "AA", "ÆÏ£"
            for temp in drecords:
                # if temp.type == "Noun" and temp.specf == "Subject" : continue
                if temp.type != "Verb" and temp.specf == "Krdanta": kfirst = temp
            krdflag, krdavyf = False, False
            for temp in drecords:
                if temp.type == "Krdanta" and krdflag: krdflag, krdfirst = True, temp
                elif temp.type == "Krdavyaya" and krdavyf: krdavyf, krdfirst = True, temp
                elif temp.type == "Verb": vfirst = temp
                sshtptr = serch_shasti(drecords, sen)
        flag, rfp_lines = CheckCompatibility(LinkedList[sfirst], LinkedList[kfirst], LinkedList[vfirst], krdfirst, krdavy, sen, sshtptr, afp_lines, sfp_lines, y)
        if vfirst.get().no_base == 1 and bodha and flag: rfp_lines.append(artha(afp_lines, sfp_lines, drecord, sen, vfirst.get().base[0]))

    return temp, rfp_lines
def Assignlingavib(drecords: List[detail]) -> detail:
    for subrec in drecords:
        if subrec.type in ["Noun", "Subject"]: break
    for record in drecords:
        if record.type in ["Krdanta", "Subject"]:
            subrec.linga, subrec.vibvach = record.linga, record.vibvach
            break
    return subrec
def getcode(temp: List[detail], Efp: TextIO) -> bool:
    i, j, m = 0, 0, 0
    # n, no_base, flag, x, nocodes
    Nouncode = ["AA ¤×èÌÄè ÍÝÖèÌÄè ÆÏ ÌÆÝÖèÍ ÌÚÆÝÖ ÌÏèÂèÍ ÌÆÝº ÌÚÆÔ",
                         "AB ÆßÈ ÏÚºÆè ÏÚºè ÈÚÏèÃÛÔ ³èÖèÌÚËßÂè ËÞÈ ÌØÜ³èÖÛÂè",
                         "AC ¤ÕèÔ ¶å½³ ÔÜÂÛ ÂÝÏµ ÂÝÏ·èµ ÂÝÏ·èµÌ ÔÚºÛÆè ÔÚØ ¤ÏèÔÆè µÆèÅÏèÔ ØÍ ×âÆèÅÔ ×ÈèÂÛ ê",
                         "AD Ôß³èÖ ÌØÜÏÝØ ÕÚ´ÛÆè ÔÛ½ÈÛÆè ÈÚÄÈ ÂÏÝ ¤Æå³Ø ³Ý½ ×ÚÑ ÈÑÚÕÛÆè ÄèÏÝ ÄèÏÝÌ ¤µÌ",
                         "AE Ø×èÂ ÏÂèÆÛ",
                         "AF ÈÝÖèÈ ³Ý×ÝÌ ×ÝÌÆ×è ÈèÏ×ÞÆ ×ÝÌ",
                         "AG µßØ ÕÚÑÚ µáØ ¨ÄÔ×ÛÂ ÔáÕèÌÆè ×ÄèÌÆè ÆÛ³áÂÆ ÆÛÕÚÆèÂ Ô×èÂèÍ ×ÄÆ ËÔÆ ¥µÏ ÌÆèÄÛÏ ÆÛ³ÚÍèÍ ÆÛÑÍ ¥ÑÍ ÅÛÖèÁèÍÚ °³×è ÆÛÔ×Æ ×èÃÚÆ ¤Ô×Ã ÔÚ×èÂÝ ×¢×èÂèÍÚÍ ¨½ºÚ ÅÚÌÆè ÆÛÔáÕ ÕÏÁ ³èÖÍ",
                         "AH ºÑ ¤Èè ÔÚÏè ÔÚÏÜ ×ÑÛÑ ³ÌÑ ÈÍ×è ³ÜÑÚÑ ¤ÌßÂ ºÜÔÆ ËÝÔÆ ³ÊÆèÅ ¨Ä³ ÈÚÃ×è ÈÝÖè³Ï ×ÏèÔÂåÌÝ´ ¤ÌèË×è ¤ÏèÁ×è ÂåÍ ÈÚÆÜÍ ÆÜÏ ³èÖÜÏ ¤ÌèËÝ ÕÌèÊÏ ¶ÆÏ× Ìá¶ÈÝÖèÈ ³ßÈÜ½ ³ÚÁè¿ ºÜÔÆÜÍ ³ÝÕ ÔÛÖ",
                         "AI ³ÈÛ ÈèÑÔ·èµ ÈèÑÔµ ÕÚ´ÚÌßµ ÔÑÜÌÝ´ ÌÏè³½ ÔÚÆÏ ³ÜÕ ÔÆæ³×è",
                         "AJ °ÄÆ",
                         "AK µÛÏÛ ÈÏèÔÂ ÌØÜÅèÏ ÕÛ´ÏÛÆè ³èÖèÌÚËßÂè ¤ØÚÏèÍ ÅÏ ¤ÄèÏÛ µåÂèÏ µèÏÚÔÆè ¤¸Ñ ÕâÑ ÕÛÑå¸è¸Í",
                         "AL ÆáÂèÏ Ñå¸Æ ÆÍÆ §³èÖÁ ¸³èÖÝ×è ¤³èÖÛ ÄßÕè ÄßÖè½Û",
                         "AM ÉÑ ××èÍ",
                         "AN ÌÛÂèÏ ÔÍ×èÍ ×èÆÛµèÅ ×ÔÍ×è ×ÝØßÄè ×´Û ê",
                         "AO ÌÝ´ Ô³èÂèÏ ¥×èÍ ÔÄÆ ÂÝÁè¿ ¥ÆÆ ÑÈÆ ÔÄÆ",
                         "AP ¤µèÆÛ ÔâÕèÔÚÆÏ ÔØèÆÛ ÔÜÂÛØåÂèÏ ÅÆ¼èºÍ ³ßÈÜ½ÍåÆÛ ºèÔÑÆ ºÚÂÔáÄ×è ÂÆÞÆÈÚÂè ÊÏèØÛ×è ÕÝÖèÌÆè ³ßÖèÁÔÏèÂèÌÆè Õå¸ÛÖè³áÕ ¨ÖÏèÊÝÅ ¥ÕèÏÍÚÕ ÊßØÄèËÚÆÝ ³ßÕÚÆÝ ÈÚÔ³ ¤ÆÑ ÏåØÛÂÚÕèÔ ÔÚÍÝ×´ ÕÛ´ÚÔÂè ¥ÕÝÕÝ³èÖÁÛ ØÛÏÁèÍÏáÂ×è ØÝÂËÝ³è ÄØÆ ØÔèÍÔÚØÆ ×ÈèÂÚÏè¸ÛÖè ÄÌÝÆ×è ÕÝ³èÏ ¸ÛÂèÏËÚÆÝ ÔÛËÚÔ×Ý ÕÝ¸Û ¤ÈèÈÛÂèÂ ê",
                         "AQ ¤ÏÛ ÕÂèÏÝ ÏÛÈÝ ÔâÏÛÆè ×ÈÂèÆ ÄèÔÛÖÂè ÄèÔáÖÁ ÄÝÏèØßÄè ÄèÔÛÖè ÔÛÈ³èÖ ¤ØÛÂ ¤ÌÛÂèÏ Ä×èÍÝ ÕÚÂèÏÔ ¤ËÛ¶ÚÂÛÆè ÈÏ ¤ÏÚÂÛ ÈèÏÂèÍÏèÃÛÆè ÈÏÛÈÆèÃÛÆè",
                         "AR ³Û¢³Ï",
                         "AS µº ÄÆèÂÛÆè ÄÆèÂÚÔÑ Ø×èÂÛÆè ÄèÔÛÏÄ ¤Æá³È ÄèÔÛÈ ÌÂ·èµº ÆÚµ ³Ý¼èºÏ ÔÚÏÁ ³ÏÛÆè ¦Ë ×èÂÌèÊáÏÌ ÈÄèÌÛÆè ×ÛÆèÅÝÏ ×ÚÌº ³ÝÌèËÜ(³ÝÌèËÛÆè) ÌÚÂ·èµ ÌÄÚÔÑ ê",
                         "AT µèÏÚÌ ×¢Ô×Ã",
                         "AU ÔèÍÚ¶èÏ ÈÝÁè¿ÏÜ³ È¼è¸Æ´ ¸ÛÂèÏ³ÚÍ ÌßµÄèÔÛ½è ÕÚÏèÄÞÑ ÄèÔÜÈÛÆè",
                         "AV ×ÞÏèÍ ×ÞÏ ¤ÏèÍÌÆè ¥ÄÛÂèÍ ÄèÔÚÄÕÚÂèÌÆè ÄÛÔÚ³Ï ËÚ×è³Ï ¤Ø×è³Ï ÊèÏÅèÆ ÈèÏËÚ³Ï ÔÛËÚ³Ï ËÚ×èÔÂè ÔÛÔ×èÔÂè ×ÈèÂÚÕèÔ ØÏÛÄÕèÔ ¨ÖèÁÏÕèÌÛ ÔÛ³ÏèÂÆè ¤Ïè³ ÌÚÏèÂÁè¿ ÌÛØÛÏ ¤ÏÝÁ ÈÞÖÆè ÄèÍÝÌÁÛ ÂÏÁÛ ÌÛÂèÏ ¸ÛÂèÏËÚÆÝ ÔÛÏå¸Æ ÔÛËÚÔ×Ý µèÏØÈÂÛ ÂèÔÛÖÚÌèÈÂÛ ¤ØÏèÈÂÛ ËÚÆÝ Ø¢× ×Ø×èÏÚ¢ÕÝ ÂÈÆ ×ÔÛÂß ÏÔÛ ÈÄèÌÚ³èÖ Âáº×Ú¢ÏÚÕÛ ¹ÚÍÚÆÚÃ ÂÌÛ×èÏØÆè ³ÏèÌ×Ú³èÖÛÆè ºµ¸è¸³èÖÝÖè Ñå³ÊÆèÅÝ ¤¢ÕÝÌÚÑÛÆè ÂèÏÍÜÂÆÝ ÈèÏÄèÍåÂÆ ÄÛÆÌÁÛ ´ÄèÍåÂ Ñå³ÊÚÆèÅÔ ¦Æ Ëµ ÅÚÌÆÛÅÛ ¤ÊèºÆÜÈÂÛ ÈÄèÌÛÆÜÔÑèÑË ·ÏÛ ê",
                         "AW ×èÂáÆ",
                         "AX ÂßÁ ÕÖèÈ ÊÚÑÂßÁ ¶Ú× ÍÔ×  ¤ÏèºÝÆ ê",
                         "AY ÅÚÆèÍ",
                         "AZ ÈÝ×èÂ³",
                         "BA ÌÚ¢× ÈÛÕÛÂ ÂÏ× ÈÑÑ ³èÏÔèÍ ¥ÌÛÖ ê",
                         "BB ÔÚÍ× ³Ú³ ³Ï½ ¤ÏÛÖè½ ÊÑÛÈÝÖè½ ×³ßÂèÈèÏº×è ÅèÔÚ·è³èÖ ¥ÂèÌ¶åÖ ÈÏËßÂè ÊÑÛËÝºèè ÔÚÍ× ¸ÛÏ¼èºÜÔÜ ¬³ÄßÖè½Û Ìæ³ÝÑÛ ÈÛ³ÔÏèÅÆ ê",
                         "BC ³½ ÕèÏåÁÛÉÑ³ ê",
                         "BD ÄÁè¿",
                         "BE Æ´ ÈÝÆÏèËÔ ³ÏÏÝØ Æ´Ï ê",
                         "BF ÕÏÜÏ ³ÑáÔÏ µÚÂèÏ ÔÈÝ×è ×¢ØÆÆ ÔÏèÖèÌÆè ÔÛµèÏØ ³ÚÍ ÄáØ ÌÞÏèÂÛ ÂÆÝ ÂÆÞ ê",
                         "BG ÕÚ×èÂèÏ",
                         "BH ÕÜÏèÖ ÕÛÏ×è ¨ÂèÂÌÚ·èµ ÌÞÏèÅÆè Ì×èÂ³",
                         "BI ³èÏåÅ ³åÈ ¤ÌÏèÖ ÏåÖ ÈèÏÂÛ¶Ú ÏÝÖè ³èÏÝÅè",
                         "BJ ¥³ÚÕ   ÄèÍå ÄÛÔè ¤ËèÏ ÔèÍåÌÆè ÈÝÖè³Ï ¤ÌèÊÏ ÆË×è ¤ÆèÂÏÛ³èÖ µµÆ ¤ÆÆèÂ ×ÝÏÔÏèÂèÌÆè ÔÛÍÂè ÔÛÖèÁÝÈÄ ÔÛØÚÍ×è ÏÔ ÔÛØÚÍ× ÆÚ³ ÄèÍÝ×è ÂÚÏÚÈÃ ¤ÆèÂÏÛ³èÖ Ìá¶ÄèÔÚÏ ÕÊèÄµÝÁá ÌØÚÔÛÑ",
                         "BK ÌåÄ³",
                         "BL ¸ÆèÄèÏ ØÛÌÚ¢ÕÝ ¸ÆèÄèÏÌ×è ¦ÆèÄÝ ³ÝÌÝÄÊÚÆèÅÔ ÔÛÅÝ ×Ý¶Ú¢ÕÝ ÕÝËèÏÚ¢ÕÝ °ÖÅÜÖ ÆÛÕÚÈÂÛ ¤Êèº ºâÔÚÂß³ ×åÌ µèÑæ ÌßµÚ·è³ ³ÑÚÆÛÅÛ ÄèÔÛºÏÚº ÕÕÅÏ Æ³èÖÂèÏáÕ ³èÖÈÚ³Ï",
                         "BM ±ÖÅ ËáÖº   ËâÖºèÍ ¤µÄ ºÚÍÝ",
                         "BN ÍÝÄèÅ",
                         "BO ÏÃ ×èÍÆèÄÆ ÕÂÚ·èµ",
                         "BP ´ÆÛÂèÏ",
                         "BQ ´¿èµ  µÁè¿³  ´¿èµÛÆè",
                         "BR ÕÏ µÝÆèÄèÏ ÂáºÆ³",
                         "BS ÈÚÄ",
                         "BT ºÆ",
                         "BU ¨ÄèÍÚÆ ¥³èÏÜ¿ ÔÆ",
                         "BV ³ßÖèÁ µåÈÚÑ ÏÚÌ ÔÛÖèÁÝ ÆÚÏÚÍÁ Ôâ³ÝÁè¾ ÔÛÖè½ÏÕèÏÔ×è ÄÚÌåÄÏ ØßÖÜ³áÕ ³áÕÔ ÌÚÅÔ ×èÔËÞ ÄâÂèÍÚÏÛ ÈÝÁè¿ÏÜ³Ú³èÖ µåÔÛÆèÄ µÏÝ¿ÅèÔº ÈÜÂÚÌèÊÏ ¤¸èÍÝÂ ÕÚÏè·èµÛÆè ÔÛÖèÔ³è×áÆ ºÆÚÏèÅÆ ¨ÈáÆèÄèÏ ¦ÆèÄèÏÚÔÏº ¸³èÏÈÚÁÛ ¸ÂÝÏèËÝº ÈÄèÌÆÚË ÌÅÝÏÛÈÝ ÔÚ×ÝÄáÔ ÂèÏÛÔÛ³èÏÌ ÄáÔ³ÜÆÆèÄÆ ÕæÏÛ ÕèÏÜÈÂÛ ÈÝÏÝÖåÂèÂÌ ÔÆÌÚÑÛÆè ÊÑÛÅèÔ¢×ÛÆè ³¢×ÚÏÚÂÛ ¤Åå³èÖº ÔÛÕèÔÌèËÏ ³â½ËºÛÂè ÔÛÅÝ ÕèÏÜÔÂè×ÑÚ¼è¹Æ µÄÚµèÏº ÌÝ¼èº³áÕ ÄÚÕÚÏèØ ÄÕÏÞÈËßÂè ê",
                         "BW ³ÆèÍÚ ³ÝÌÚÏÜ",
                         "BX ÈÝÂèÏ ¥ÂèÌº ÂÆÍ ×ÝÆÝ ×ÝÂ",
                         "BY ×´Ü ¥ÑÛ ÔÍ×èÍÚ",
                         "BZ ÕÛÕÝ ÈåÂ ÈÚ³ ¤ÏèË³ ¿ÛÌèË ÈßÃÝ³ ÕÚÔ³"]
    Nouncodes = 52;
    Actioncodes = 27;
    Actioncode = ["aa ×ÂèÂÚÍÚÌè ËÝÔÛ",
                           "ab ÈèÏÚÄÝÏèËÚÔá",
                           "ac ÈèÏÚÁÅÚÏÁá",
                           "ad ºè¼ÚÆá",
                           "ae Õæ¸á",
                           "af Ë³èÖÁá ËåºÆá",
                           "ag µÂæ",
                           "ah È¾Æá ÔèÍ³èÂÔÚ¸Û ÔèÍ³èÂÚÍÚ¢ÔÚ¸Û",
                           "ai ÕèÏÔÁá",
                           "aj ¤ÕèÏÝÔÛÌå¸Æá",
                           "ak Ø×Æá",
                           "al ÕÊèÄá",
                           "am ØÛ¢×ÚÍÚ¢µÂæ ØÛ¢×ÚÍÚ¢ ØÆÆá ³åÈá ³èÏåÅá ¥¶ÚÂá",
                           "an ³ÏÁá",
                           "ao Ï³èÖÁá ÈÚÑÆá",
                           "ap ÔÛØÚÏá ÂÝÖè½æ",
                           "aq ÄÏèÕÆá ÈèÏá³èÖÁá",
                           "ar ÑÛ´ÛÂÚ³èÖÏÔÚ¸Æá",
                           "as ÔÛØÚÍ×ÚµÂæ",
                           "at ÈÚÆá",
                           "au Ô³èÂèÏ×¢Íåµá",
                           "av ×èÂáÍá",
                           "aw ÈÞºÚÍÚÌè ×èÂÝÂæ",
                           "ax ºÍá ¤ËÛËÔá",
                           "ay ÄÚÆá",
                           "az ÈèÏ×Ôá ÈèÏÚÁÛµÏèËÔÛÌå¸Æá",
                           "ba ÆÏèÂÆá"
                           ]
    result = []
    for line in Nouncode:
        words = line.split()
        for recptr in temp:
            if recptr.sub_no != 7 and recptr.type == "Noun":
                # recptr.no_base, recptr.no_codes = 0, 0
                for word in words:
                    if recptr.stem == word:
                        recptr.base[recptr.no_base] == word
                        recptr.code[recptr.no_base] == words[0]
                        recptr.no_base += 1
                        recptr.no_codes += 1
                        break
    for recptr in temp:
        for line in Actioncode:
            words = line.split()
            j = len(words)
            if recptr.sub_no != 7 and recptr.type == "Noun":
                for m in range(recptr.no_base):
                    for i in range(j):
                        if words[i] == recptr.base[m]:
                            recptr.code[m] == words[0]
                            recptr.no_codes += 1
    flag = True
    for recptr in temp:
        if recptr.type == "Avyaya" and recptr.no_codes == 0:
            result.append(" No Code for %s %s \n "%(recptr.stem, recptr.Type))
            flag = False
        elif recptr.type == "Verb":
            nocodes = 0
            for i in range(recptr.no_base):
                if recptr.code[i] == "":
                    nocodes += 1
                    result.append(" No Code for %s %s \n "%(recptr.stem, recptr.base[i]))
            if nocodes == recptr.no_base: flag = False
    if result:
        Efp.writelines(result)
    return flag
def serch_shasti(drecords: List[detail], sent: str) -> List[shasti]:
    fshtptr, shtptr, tmpsht, secsht = None, None, None, None
    words = sent.split()
    j = len(words)
    shtptrs = []  # List[shasti]
    for dshtptr in drecords:
        if dshtptr.type == "Verb":
            for i, word in enumerate(words):
                if dshtptr.word == word and i != 2:
                    the_word, the_i = word, i
                    break
            if the_word[0] in ["S", "N", "="]: continue
            the_i -= 1
            for temptr in drecords:
                if temptr.word == word[the_i]: break
            if temptr.sub_no == 6:
                shtptr = shasti()
                shtptr.specf, shtptr.word = temptr.specf, temptr.word
                for m in range(temptr.no_base):
                    shtptr.base[m], shtptr.code[m] = temptr.base[m], temptr.code[m]
                shtptr.sub_no, shtptr.no_base = temptr.sub_no, temptr.no_base
                shtptrs.append(shtptr)
                the_i += 1
                for temptr in drecords:
                    if temptr.word == word[the_i]: break
                shtptr = shasti()
                shtptr.specf, shtptr.word = temptr.specf, temptr.word
                for m in range(temptr.no_base):
                    shtptr.base[m], shtptr.code[m] = temptr.base[m], temptr.code[m]
                shtptr.sub_no, shtptr.no_base = temptr.sub_no, temptr.no_base
                shtptr.sub_no, shtptr.no_base = temptr.sub_no, temptr.no_base
                shtptrs.append(shtptr)
    return shtptrs
def CheckCompatibility(srecord: LinkedList[detail], krecord: LinkedList[detail], vrecord: LinkedList[detail], krdfirst: detail, krdavy: detail,sent: str, sshtptr: LinkedList[shasti],
                       afp_lines: List[str], sfp_lines:  List[str], y: int) -> (bool, List[str]):
    a, i, j, m, n, no_vsub, no_ksub, num_sub, Naflag = 0, 0, 0, 0, 0, 0, 0, None, False
    flag, krdflag, krdavyf, verflag, karflag, shaflag = True, False, False, False, 0, False
    krdmismatch, mismatch, krdpos, avypos, Saflag, Sapos = False, False, None, None, 0, None
    krdoth, no_krdoth, krdsuc, subver = 0, None, 1, 0
    afppos, pos = None, None
    firstptr = None,  # detail
    subptr = None,  # detail
    fstptr = None,  # detail
    subunmatch = None # detail
    karptr = None,  # detail
    un_match = None,  # detail
    karmatch = None  # detail
    verptr = None,  # detail
    krdrecord = krdfirst,  # detail
    krdunmatch = None,  # detail
    krdmatch = None,  # detail
    avyrecord = krdavy  # detail
    shrvib = None  # shasti,
    tshrvib = None  # shasti
    verptr = vrecord.get()
    krdpos = False

    rfp_lines = []
    cfp = open("comptble.aci", "r")
    cfp_lines = cfp.readlines()
    for subptr in iter(srecord):
        if subptr.word == "Æ": Naflag = True
        elif subptr.word == "×Ø":
            Saflag = True
            Sapos = subptr.pos
        else: break
    if krdfirst != None:
        if krdrecord.type == "Krdanta" or krdrecord.specf == "Subject":
            krdflag = True
            krdpos = krdrecord.pos
    if krdavy != None:
        if krdavy.type == "Krdavyaya": krdavyf = True
    verflag = False
    for verptr in iter(vrecord):
        if verptr.dispSpecf == "Verb": verflag = True
    verptr = vrecord.get()
    for karptr in iter(krecord):
        if not (krdflag or krdavyf):
            if karptr.sub_no != 7 and karptr.pos != Sapos - 1: no_vsub += 1
            if karptr == verptr: break
        elif verflag and krdflag:
            if karptr.sub_no != 6:
                if karptr.pos > krdfirst.pos or krdfirst.specf == "Subject": no_vsub += 1
            else:
                if karptr.pos != krdfirst.pos or krdfirst.specf == "Subject": no_vsub += 1
            if karptr == krdfirst: break
        elif verflag and krdavyf:
            if karptr.pos > krdfirst.pos: no_vsub += 1
            if karptr == krdavy: break
        else: break
    rfp_lines.append(sent)
    if fstptr == None:
        for subptr in iter(srecord):
            rfp_lines.append(subptr.type)
            if subptr.type in ["Noun", "Krdanta"]: rfp_lines.append(subptr.specf)
            rfp_lines.append(subptr.word)
        subptr, shaflag = srecord.get(), False
    else:
        rfp_lines.append(sha_disp(cfp_lines, sent))
        shaflag = True
    rfp_lines.append("-------------------")
    karptr, subptr = krdrecord.get(), srecord.get()
    if verptr == None: verptr = vrecord.get()
    for srecget in iter(srecord):
        if krdflag: mrecord = krdrecord
        elif krdavyf: mrecord = avyrecord
        for m in range(mrecord.no_base):
                num_sub, karflag, un_match = no_ksub, 0, None
                for rec in iter(krecord):
                    if rec.specf == "Subject" and karptr != None and karptr.pos < rec.pos and karptr.sub_no != 6: karflag += 1
                    if rec.type in ["Krdanta", "Krdavyaya"]: break
                krdoth, no_krdoth = 0, 0
                for rec in iter(krdrecord):
                    if rec.type == "Krdanta" and rec.specf == "Subject":
                        krdoth += 1
                        no_krdoth += 1
                    if rec.type != "Krdanta": break
                krdrecord = krdfirst #???
                for n in range(srecord.get().no_base):
                    num_sub = no_ksub
                    mismatch, krdmismatch = False, False
                    for line in cfp_lines:
                        line = line.strip()
                        if line == "": continue
                        word = line.split()
                        j = len(word)
                        code1 = line[:2]
                        karptr = krecord.get()
                        krdrecord = krdfirst
                        srecget = srecord.get()
                        if srecget.code[n] == code1 and krdrecord.type == "Krdanta":
                            if srecget.voice == "karmani"  or (srecget.voice == "karthari" and srecget.linga == krdrecord.linga and srecget.vibvach == krdrecord.vibvach):
                                code2 = line[3:5]
                                karptr = krecord.get()
                                if karflag == 0 and code2 == "00":
                                    mismatch = krdrecord.code[m] in word[1]
                                else:
                                    if karptr != None:
                                        for karptr in iter(krecord):
                                            if karptr.pos < krecord.get().pos and karptr.code[m] == code2 and karptr.sub_no != 6:
                                                if word[karptr.sub_no] == krecord.get().code[m]:
                                                    mismatch = False
                                                    karflag -= 1
                                                else:
                                                    mismatch = True
                                                    krdunmatch = krdrecord.get()
                                                    un_match = karptr
                                            if karptr.type == "Krdanta": break
                        if krdoth > 0:
                            code2 = line[3:5]
                            if karptr != None:
                                for karptr in iter(krdfirst):
                                    for krdrec in iter(krdrecord):
                                        if krdrec.sub_no == 6:
                                            for shrvib in iter(sshtptr):
                                                if shrvib.word == krdrec.word: continue
                                            if shrvib.code == code1 and code2 == "00" and karptr.specf == krdrec.specf:
                                                if krdrec.code[m] in word[1]:
                                                    if krdmatch:
                                                        no_krdoth -= 1
                                                        krdmatch = krdrec
                                                        karmatch = karptr
                                                else:
                                                    krdmismatch = True
                                                    krdunmatch = krdrec
                                                    karmatch = karptr
                                                break
                                        if krdrec.type != "Krdanta": break
                                    if karptr.type == "Krdanta": break
                            else:
                                for krdrec in iter(krdrecord):
                                    if krdrec.type == "Verb" and krdrec.sub_no != 6:
                                        if code1 == "AA" and code2 == "00" and krdrec.specf == "Subject":
                                            if krdrec.code[m] in word[1]:
                                                if krdmatch:
                                                    no_krdoth -= 1
                                                    krdmatch = krdrec
                                            else:
                                                krdmismatch = True
                                                krdunmatch = krdrec
                        if not Naflag:
                            if not verflag:
                                if krdoth == 0:
                                    if not (mismatch or karflag):
                                        krdsuc, flag = True, True
                                        rfp_lines.append("The Krdanta is Semantically Compatible if  %s root means %s and subject is %s "%
                                                         (krdfirst.stem, krdfirst.base[m], srecord.base[n]))
                                    else:
                                        krdsuc, flag = False, False
                                        rfp_lines.append("Verb %s is not compatible with subject %s"%(verptr.word, srecord.word))
                                        if un_match != None: rfp_lines.append("if %s is %s"%(un_match.dispSpecf, un_match.word))
                                else:
                                    if mismatch and karflag and no_krdoth == 0:
                                        krdsuc, flag = True, True
                                        if karptr != None: rfp_lines.append("%s %s  %s is compatible with %s %s %s"%
                                                            (karmatch.type, karmatch.specf, karmatch.word, krdmatch.type, krdmatch.specf, krdmatch.word))
                                        else: rfp_lines.append("%s %s %s is semantically compatible"%(karmatch.type, karmatch.specf, karmatch.word))
                                    elif (mismatch or karflag) and no_krdoth > 0:
                                        krdsuc, flag = False, False
                                        if mismatch: rfp_lines.append("%s %s %s  is not compatble with %s is %s"%
                                                              (krdunmatch.type, krdunmatch.specf, krdunmatch.word, un_match.dispSpecf, un_match.word))
                                    elif krdmismatch:
                                        krdsuc, flag = False, False
                                        rfp_lines.append("%s %s  %s is not compatible with %s %s %s if Krdanta base is %s " %
                                                         (karmatch.type, karmatch.specf, karmatch.word, krdunmatch.dispSpecf, krdunmatch.word))
                                        if un_match: rfp_lines.append("if %s is %s "%(un_match.dispSpecf, un_match.word))
                            else:
                                if krdoth == 0:
                                    if not (mismatch or karflag):
                                        krdsuc = True
                                        rfp_lines.append("The Krdanta is Semantically Compatible if  %s root means %s and subject is %s "%
                                                         (krdfirst.stem, krdfirst.base[m], srecord.base[n]))
                                    else:
                                        krdsuc = False
                                        rfp_lines.append("Verb %s is not compatible with subject %s"%(verptr.word, srecord.word))
                                        if un_match != None: rfp_lines.append("if %s is %s"%(un_match.dispSpecf, un_match.word))
                                else:
                                    if mismatch and karflag and no_krdoth == 0:
                                        krdsuc, flag = True, True
                                        if karptr != None: rfp_lines.append("%s %s  %s is compatible with %s %s %s"%
                                                            (karmatch.type, karmatch.specf, karmatch.word, krdmatch.type, krdmatch.specf, krdmatch.word))
                                        else: rfp_lines.append("%s %s %s is semantically compatible"%(karmatch.type, karmatch.specf, karmatch.word))
                                    elif (mismatch or karflag) and no_krdoth > 0:
                                        krdsuc, flag = False, False
                                        if mismatch: rfp_lines.append("%s %s %s  is not compatble with %s is %s"%
                                                              (krdunmatch.type, krdunmatch.specf, krdunmatch.word, un_match.dispSpecf, un_match.word))
                                    elif krdmismatch:
                                        krdsuc, flag = False, False
                                        rfp_lines.append("%s %s  %s is not compatible with %s %s %s if Krdanta base is %s " %
                                                         (karmatch.type, karmatch.specf, karmatch.word, krdunmatch.dispSpecf, krdunmatch.word))
                                        if un_match: rfp_lines.append("if %s is %s "%(un_match.dispSpecf, un_match.word))
                        else: krdsuc, flag = True, True
        if verflag:
            subver = True
            for verptr in iter(vrecord):
                if verptr.specf == "Verb" and verptr.dispSpecf in ["Verb", "Krdanta"]:
                    for m in range(verptr.no_base):
                        num_sub = no_vsub
                        if verptr.code[m] != "":
                            for n in range(srecord.get().no_base):
                                num_sub = no_vsub
                                mismatch, krdmismatch = False, False
                                for line in cfp_lines:
                                    line = line.strip()
                                    if line == "": continue
                                    word = line.split()
                                    j = len(word)
                                    code1, code2 = line[:2], line[3:5]
                                    karptr = krecord.get()
                                    # srecget = srecord.get()
                                    if not shaflag:
                                        if code2 == "00":
                                            if srecget.code[n] == code1:
                                                if verptr.code[m] in word[1]: subver = True
                                                else: subver, subunmatch = False, srecget
                                            if karptr == None or no_vsub == 0:
                                                flag = not verptr.code[m] in word[1] or (krdflag and krdsuc)
                                        elif not krdflag:
                                            for karptr in iter(krecord):
                                                if verptr.code[m] in word[karptr.sub_no]:
                                                    karmatch = karptr
                                                    num_sub -= 1
                                                else: un_match = karptr
                                        elif no_vsub > 0:
                                            for karptr in iter(krecord):
                                                if karptr.specf == "Verb" and karptr.code[0] == code2 and krdfirst.specf == "Subject" or \
                                                        (karptr.pos > krdpos and krdfirst.specf == "Subject"):
                                                    if code2 in word[karptr.sub_no]:
                                                        karmatch = karptr
                                                        num_sub -= 1
                                                    else: un_match = karptr
                                    else:
                                        for karptr in iter(krecord):
                                            if karptr.specf not in ["Verb", "Krdanta", "Krdavyaya"]:
                                                code2 = line[3:5]
                                                if code2 == "00":
                                                    if not verptr.code[m] in word[1]: subver, subunmatch = False, srecget
                                                    else: subver = True
                                                if karptr.sub_no < 6 and code1 in srecget.code[n]:
                                                    if karptr.code[0] == code2 and karptr.pos > krdpos:
                                                        if verptr.code[m] in word[karptr.sub_no]:
                                                            karmatch = karptr
                                                            num_sub -= 1
                                                        else: un_match = karptr
                                    if code2 == "00" and Saflag:
                                        for subptr in iter(fstptr):
                                            if subptr.type == "Noun" and subptr.specf == "Instrument" and subptr.pos == Sapos - 1:
                                                if code1 in subptr.code[n]: subver = True
                                                else: subver, subunmatch = False, srecget
                                if not Naflag:
                                    if not subver:
                                        flag = False
                                        rfp_lines.append("The Verb %s is not compatible with the Subject "%(verptr.word))
                                    else:
                                        if num_sub == 0:
                                            flag = True
                                            rfp_lines.append("The Verb %s is Semantically Compatible With Subject if Verb Root means %s "%(verptr.stem,verptr.base[m]))
                                            if no_vsub > 0: rfp_lines.append("and %s is %s "%(karmatch.specf, karmatch.base[m]))
                                        else:
                                            flag = False
                                            rfp_lines.append("The Verb %s is not compatible with Subject if %s is %s " % (verptr.word, un_match.specf, un_match.stem))
                                            if krdflag: flag = krdsuc
                                else: flag = Naflag
                            if verptr.no_base > 1:
                                y = Sabdabodha(afp_lines, sfp_lines, rfp_lines, firstptr, sent, flag, y, pos, Saflag,verptr.base[m], m)
                            if verptr.no_base == m + 1:
                                for lin in afp_lines():
                                    if lin[0] == "-": break
    if flag: rfp_lines.append("The Sentence is Semantically Compatible")
    else: rfp_lines.append("The Sentence is Semantically not Compatible")
    rfp_lines.append("-------------------")
    return flag, rfp_lines
def sha_disp(disptr: detail, sent: str) -> List[str]:
    j, k, = 0, 0
    search = None  # detail
    firrec = None  # display
    record = None  # display
    temrec = None  # detail
    word = sent.split()
    j = len(word)
    rfp_lines = []
    disptr = iter(LinkedList(disptr))
    for search in disptr:
        if search.sub_no != 6:
            if firrec == None:
                firrec = LinkedList(display())
                record = firrec.get()
            else:
                record = display()
                firrec.append(record)
        record.specf, record.word = search.specf, search.word
    for i in range(j-1, 5, -1):
        for search in disptr:
            if word[i - 1] == search.word: break
        if search.sub_no == 6:
            for record in firrec:
                temrec = record.get()
                if temrec.word == word[i]: break
            if record.get() == firrec.get():
                temrec = firrec.get()
                inst = display()
                inst.specf, inst.word == search.specf, search.word
                firrec.set(inst)
                firrec.append(temrec)
            else:
                inst = display()
                inst.specf, inst.word == search.specf, search.word
                firrec.append(inst)
                firrec.append(record)
    for record in firrec:
        if record.specf != "Verb":
            rfp_lines.append("%s %s"%(record.specf, record.word))
            break
    rfp_lines.append("%s %s " % (record.specf, record.word))
    return rfp_lines
def Sabdabodha(afp: TextIO, sfp: TextIO, rfp: List[str], firstptr: detail, sent: str, flag: bool, y: int, pos: int, Saflag: bool, base: str, m: int) -> (bool, List[str]):
    rfp_lines = []
    return y, rfp_lines
def artha(afp_lines: List[str], sfp_lines: List[str], drecord: LinkedList(detail), sentr: str, VerbMean: str) -> List[str]:
    noofmean, pos, mode, i, j, k, no_wor, yes, n, linga, x = 0, None, None, 0, None, None, 0, None, 0, 5, 4
    match, Verb, Krd, flag, Naflag = False, 1, 1, False, False
    fvibptr = None  # vibak
    tvibptr = None  # vibak
    dvibptr = None  # vibak
    record = None  # vibak
    verptr = None  # vibak
    temptr = None  # detail
    fstptr = None  # detail
    start = None  # disp_arth
    Vyalist = ["×ÂèÂÚÍÚÌè", "ËÝÔÛ"]
    rfp_lines = []
    temptr = drecord.get()
    voice = temptr.voice
    for temptr in iter(drecord):
        if temptr.specf == "Verb": break
    mode = temptr.mode
    noofmean = temptr.no_base
    for line in afp_lines:
        line = line.strip()
        words = line.split()
        no_wor = len(words)
        if words[0] == "ÔÚ³èÍÌè": fl, match, sen = n, False, line
        if line[0]=='-' and not match:
            tvibptr = fvibptr
            yes = choice(type[0], words, voice, pos, tvibptr, afp, fl, VerbMean)
            tvibptr = fvibptr
            Krd = 0

    return rfp_lines
def choice(tYpe: str, word: str, voice: str, pos, tvibptr: LinkedList[vibak], afp: TextIO, fl: int, VerbMean: str) -> bool:
    yes, success = False, True
    tvibptr_list = iter(tvibptr)
    for tvibptr in tvibptr_list:
        if (tvibptr.stype =='1' and tvibptr.specf == "dative") or tvibptr.stype in ['5', '2', '4']:
            # Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */
            yes = findverb(voice, tvibptr.sword, tvibptr, afp, fl, VerbMean)
    return yes
def findverb(voice: str, Word: str, tvibptr: vibak, afp: List[str], fl: int, VerbMean: str) -> int:
    found, i, j, pos = False, None, None, None
    vnum, vno, linga = 0, 0, 4
    line1, words, message, word, vword, typ, lword, ltype, temp = None, None, None, None, None, None, None, 'Z', None
    list = ["ÈÞÏèÔÚÁèØ", "¤ÈÏÚÁèØ", "ÄÛÆ", "ÏÚÂèÏÛ", "¤ØåÏÚÂèÏ", "×ÈèÂÚØ", "È³èÖ", "ÌÚ×", "×¢ÔÂè×Ï"]
    list1 = ["ºè¼ÚÆ", "×Ý´", "ÄÝ£´", "¦¸è¹Ú", "ÄèÔáÖ", "ÈèÏÍÂèÆ", "ÅÏèÌ", "¤ÅÏèÌ", "×¢×è³ÚÏ", "ËÚÔÆÚ", "ÔÛÔá³", "ÊåÅ", "ÊÝÄèÅÛ", "ÅÜ", "ÈèÏºè¼Ú", ]

    if tvibptr.stype == "2": typ = 0
    for line in afp:
        line = line.strip()
        if line[0] == "-":
            found = True
            break
        words = line.split()
        # if words[0] == "ÔÚ³èÍÌè": ???
        vno = len(words)
        typ = int(words[3][0])
        word = words[4]
        if typ == 1:
            linga = int(words[6]) + 2
            pos = int(words[7])
        elif typ == 4:
            lword = words[9]
            ltype = int(words[11]) + 1
        elif typ == 5:
            lword = VerbMean
            ltype = int(words[11]) + 1
            found = dispmea(voice, vnum, list, tvibptr, ltype, lword)
        elif typ == 2: lword == words[13]
        elif typ == 1 and pos in range(1, 3):
            for item in list1:
                if word == item:
                    message = ["×ÌÔáÂÚ", "×ÌÔáÂ£", "×ÌÔáÂ¢"][linga] + tvibptr.bword
                    # vword = tvibptr.bword
                    return True
        elif typ == 5 or ((type == 2 and tvibptr.stype == 2) or (type == 4 and tvibptr.stype == 4)) and Word == words[1]:
            found = dispmea(voice, vnum, list, tvibptr, ltype, lword)
            return found
    return False
def dispmea(voice: str, dhatunum, list: str, tvibptr: vibak, vachana: str, lword: str) -> (bool, vibak):
    i, j, re, success, endstar, retflag, flag = None, None, None, 0, 0, 0, 0
    Vyalist = ["×ÂèÂÚÍÚÌè","ËÝÔÛ"]
    message, temp, vword, line, flword, message1 = None, None, None, None, None, None
    vyapara = ["×ÂèÂÚÍÚÌè ËÔÆ", "ËÝÔÛ ¥ÅáÍÂèÔ", "ÈèÏÚÄÝÏèËÚÔá ¨ÂèÈÂèÂÛ",
                 "ÈèÏÚÁÅÚÏÁá ÈèÏÚÁÅÏÁ", "ºè¼ÚÆá ÔáÄÆ", "Õæ¸á ÕÝÄèÅÛ",
                 "µÂæ ÈÞÏèÔÄáÕÔÛËÚµÈÞÏèÔ³åÂèÂÏÄáÕ×¢Íåµ*", "Ë³èÖÁá µÑÊÛÑÚÅ×è×¢Íåµ*",
                 "ÑÛ´ÛÂÚ³èÖÏÔÚ¸Æ È¾Æ", "ÕèÏÔÁá ÕèÏÔÁ", "¤ÕèÏÝÔÛÌå¸Æá ¤ÕèÏÝÔÛÌå¸Æ",
                 "Ø×Æá Ø×Æ", "ÕÊèÄá µÚÍÆ", "ØÛ¢×ÚÍÚ¢ ØÆÆ", "ØÛ¢×ÚÍÚ¢µÂæ ØÆÆ",
                 "³ÏÁá ÔèÍÚÈÚÏ", "Ï³èÖÁá Ï³èÖÁ", "ÈÚÑÆá Ï³èÖÁ", "ÔÛØÚÏá ÔÛØÏÁ",
                 "ÄÏèÕÆá ÄÏèÕÆ", "ÈèÏá³èÖÁá ÄÏèÕÆ", "¤³èÖÏÔÛÆèÍÚ×á Ñá´Æ",
                 "ÔÛØÚÍ×ÚµÂæ ¿ÍÆ", "ÈÚÆá ÈÚÆ", "Ô³èÂèÏ×¢Íåµá Ô³èÂèÏ×¢Íåµ",
                 "×èÂáÍá ¸æÏèÍ", "ÈÞºÚÍÚÌè ÈÞºÆ", "ºÍá ºÍ", "ÄÚÆá ×èÔ×èÔÂèÂèÔÆÛÔßÂÛÈÞÏèÔ³ÈÏ×èÔÂèÂèÔÚÈÚÄÆ*",
                 "ÈèÏ×Ôá ÈèÏ×Ô", "ÔèÍ³èÂÔÚ¸Û È¾Æ"]

    if int(tvibptr.stype) == 1:
        for item in list:
            if tvibptr.bword == item:
                tvibptr.arthaword = "ÔèÍÚÈ³ÂÚÆÛÏÞÈ³" + item
                retflag = True
        if dhatunum in [55, 71, 102, 140, 345]:
            if tvibptr.spos in range(4,7):
                tvibptr.arthaword = "ÆÛÖè¾ÔÛÖÍÂÚÆÛÏÞÈ³ " + item
                retflag = True
        elif dhatunum == 23:
            if tvibptr.spos in range(4,7):
                tvibptr.arthaword = "ÆÛÖè¾ÈèÏÂÛÍåµÛÂÚÆÛÏÞÈ³ " + item
                retflag = True
        if dhatunum in [10, 68, 124, 206, 207, 211]:
            if tvibptr.spos in range(4,7):
                tvibptr.arthaword = "ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ " + item
                retflag = True
    elif int(tvibptr.stype) in [2, 4, 5]:
        if int(tvibptr.stype) == 5:
            tvibptr.arthaword = {"A":"ÔÏèÂÌÚÆ³ÚÑÔßÂèÂÛ ", "B":"ÔÏèÂÌÚÆ³ÚÑÔßÂèÂÛ ", "C":"ÈÏå³èÖËÞÂ³ÚÑÔßÂèÂÛ ", "D":"ÈÏå³èÖËÞÂ³ÚÑÔßÂèÂÛ ",
                             "L":"ËÞÂ³ÚÑÔßÂèÂÛ ", "R":"ËÞÂ³ÚÑÔßÂèÂÛ ", "K":"¤ÄèÍÂÆËÞÂ³ÚÑÔßÂèÂÛ ", "Q":"¤ÆÄèÍÂÆËÞÂ³ÚÑÔßÂèÂÛ ",
                             "E":"¤ÄèÍÂÆËÔÛÖèÍÂè³ÚÑÔßÂèÂÛ ", "I":"ØÛÂÈèÏÚÈèÂÛÔÛÖÍ³á¸è¹ÚÔÛÖÍ ", "G":"¤ÆÄèÍÂÆËÔÛÖèÍÂè³ÚÑÔßÂèÂÛ ",
                             "M":"ÔÛÅÛÔÛÖÍ ", "H":"ËÔÛÖèÍÂè³ÚÑÔßÂèÂÛ ", "S":"ËÔÛÖèÍÂè³ÚÑÔßÂèÂÛ ", "T":"ËÔÛÖèÍÂè³ÚÑÔßÂèÂÛ ",
                             "F":"ËÔÛÖèÍÂè³ÚÑÔßÂèÂÛ "}[vachana]
        for vyaword in vyapara:
            if vyaword == lword:
                message = flword
                flag, success = flword in Vyalist, True
                break
        if not success: return retflag
        if message[-1] == "*": endstar, message = True, message[:-1]
        temp = message
        if int(tvibptr.stype) in [2, 5]:
            splitword = splitTheWord(message)
            if not endstar: message += "Ú¤ÆÝ³ÞÑ"
            for i in range(splitword.noofsplits):
                if splitword.secondWord[i][0] == '¤': message = "Ú¤ÆÝ³ÞÑ"
                elif splitword.secondWord[i][0] == '¤': message = "Íè¤ÆÝ³ÞÑ"
        if int(tvibptr.stype) == 5: tvibptr.arthaword += message
        elif int(tvibptr.stype) == 4: tvibptr.arthaword = message
        elif int(tvibptr.stype) == 2:
            if tvibptr.ltype == 'e': tvibptr.arthaword = "ËÞÂ³ÚÑÔßÂèÂÛ" + message
            elif tvibptr.ltype in ['a', 'b']: tvibptr.arthaword = "ÊÑÔÄÆÛÖè¾ÚÆÆÝÊÆèÅÛ³ßÂÛ×ÚÅèÍáÖè½×ÚÅÆÂèÔ" + \
                                                      ["ÚÕèÏÍ ", "ÔÕÛÖè½ "][['a', 'b'].index(tvibptr.ltype)] + message
            elif tvibptr.ltype == 'e': tvibptr.arthaword = "ËÞÂ³ÚÑÜÆ " + message
            else: tvibptr.arthaword = message
        if endstar:
            if voice == "kartari":
                if int(tvibptr.stype) in [2, 5]: tvibptr.arthaword = " ÔèÍÚÈÚÏÚÆÝ³ÞÑ"
            elif voice == "karmani" and int(tvibptr.stype) == 2: tvibptr.arthaword = "ÔèÍÚÈÚÏ"
        if int(tvibptr.stype) == 2:
            if tvibptr.ltype in ['e', 'f', 'g', 'h', 'i']:
                if tvibptr.semlinga == 0 and tvibptr.lpos == 1: tvibptr.arthaword += "³ßÂèÍÚÕèÏÍÚËÛÆèÆÚ "
                elif tvibptr.semlinga == 1 and tvibptr.lpos == 1: tvibptr.arthaword += "³ßÂèÍÚÕèÏÍÚËÛÆèÆ£ "
                elif tvibptr.semlinga == 2 and tvibptr.lpos == 1: tvibptr.arthaword += "³ßÂèÍÚÕèÏÍÚËÛÆèÆÌè "
                elif tvibptr.semlinga == 0 and tvibptr.lpos == 2: tvibptr.arthaword += "³ßÂèÍÚÕèÏÍÚËÛÆèÆá "
                elif tvibptr.semlinga == 1 and tvibptr.lpos == 2: tvibptr.arthaword += "³ßÂèÍÚÕèÏÍÚËÛÆèÆæ "
                elif tvibptr.semlinga == 2 and tvibptr.lpos == 2: tvibptr.arthaword += "³ßÂèÍÚÕèÏÍÚËÛÆèÆá "
                elif tvibptr.semlinga == 0 and tvibptr.lpos == 3: tvibptr.arthaword += "³ßÂèÍÚÕèÏÍÚËÛÆèÆÚ£ "
                elif tvibptr.semlinga == 1 and tvibptr.lpos == 3: tvibptr.arthaword += "³ßÂèÍÚÕèÏÍÚËÛÆèÆÚ£ "
                elif tvibptr.semlinga == 2 and tvibptr.lpos == 3: tvibptr.arthaword += "³ßÂèÍÚÕèÏÍÚËÛÆèÆÚÆÛ "
                else: tvibptr.arthaword += "³ßÂèÍÚÕèÏÍÚËÛÆèÆ "
            elif tvibptr.ltype in ['a', 'b']: tvibptr.arthaword += "ºÆèÍÉÑÚÕèÏÍ£ "
        elif int(tvibptr.stype) == 4:
            tvibptr.arthaword += ["ÚÅÜÆá¸è¹ÚÔÛÖÍ×èÔÔÛÖÍ×ÌÚÆ³ÏèÂß³ ", "ÆÛÏÞÈÛÂ×èÔåÂèÂÏ³ÚÑÔßÂèÂÛ "][['a', 'b'].index(tvibptr.ltype)]
        if voice == "karmani" and (int(tvibptr.stype) == 5 or (int(tvibptr.stype) == 2 and tvibptr.ltype == "d")): tvibptr.arthaword += "ÔèÍÚÈÚÏ³ÏèÌÂèÔÚÕèÏÍ£ "

    return tvibptr, retflag
def splitTheWord(input: str) -> SPLIT:
    splitWords, splitWord = None, None
    fp, sp, count = "", "", 0
    splitWords = SPLIT()
    for k, ch in enumerate(reversed(input)):
        i = k - 2
        if ord(ch) in range(ord('¤'), ord('±')): sp, fp = ch, input[:i]
        elif ord(ch) in range(ord('³'), ord('Ø')):
            if ord(input[i + 1]) in range(ord('Ú'), ord('ß')): sp = chr(ord(input[i + 1]) - ord('Ú') + ord('¥')) + input[i + 2]
            elif ord(input[i + 1]) in range(ord('à'), ord('æ')): sp = chr(ord(input[i + 1]) - ord('à') + ord('«')) + input[i + 2]
            elif ord(input[i + 1]) in range(ord('¤'), ord('Ø')) or ord(input[i + 1]) <= ord('£'): sp = '¤' + input[i + 1]
            elif input[i + 1] == 'è': sp = input[i + 2]
            fp = input[:i] + "è"
        if ord(ch) in range(ord('¤'), ord('Ø')) and fp != "" and sp != "":
            splitWords.firstword[count], splitWords.secondWord[count] = fp, sp
            count += 1
        if count >= 8: break
    splitWords.noofsplits = count
    splitWord = SPLIT()
    j = 0
    for i in range(splitWords.noofsplits):
        splitWord.firstWord[j], splitWord.secondWord[j] = splitWords.firstWord[i], splitWords.secondWord[i]
        j += 1
        if splitWords.firstWord[i] == splitWords.firstWord[i + 1] and splitWords.secondWord[i] == splitWords.secondWord[i + 1]: i += 1
    splitWord.noofsplits = j
    return splitWord

VIBAK =  vibak()
DISP_ARTH = display()
SHASTI = shasti()
DISPLAY = disp_shasti()

#SUBFORMS.h
Form004 = ["¬ÖÚ","¬Âá","¬ÂÚ£","¬ÂÚÌè/¬ÆÚÌè","¬Âá/¬Æá","¬ÂÚ£/¬ÆÚ£","¬ÂÍÚ/¬ÆÍÚ",
"¬ÂÚËèÍÚÌè","¬ÂÚËÛ£","¬Â×èÍâ","¬ÂÚËèÍÚÌè","¬ÂÚËèÍ£","¬Â×èÍÚ£","¬ÂÚËèÍÚÌè",
"¬ÂÚËèÍ£","¬Â×èÍÚ£","¬ÆÍå£/¬ÂÍå£","¬ÂÚ×ÚÌè","¬Â×èÍÚÌè","¬ÆÍå£/¬ÂÍå£","¬ÂÚ×Ý"]
Form104 = ["¬Ö£","¬Âæ","¬Âá","¬ÂÌè/¬ÆÌè","¬Ææ/¬Âæ","¬ÂÚÆè/¬ÆÚÆè","¬ÂáÆ/¬ÆáÆ",
"¬ÂÚËèÍÚÌè","¬Ââ£","¬Â×èÌâ","¬ÂÚËèÍÚÌè","¬ÂáËèÍ£","¬Â×èÌÚÂè",
"¬ÂÚËèÍÚÌè","¬ÂáËèÍ£","¬Â×èÍ","¬ÂÍå£/¬ÆÍå£","¬ÂáÖÚÌè","¬Â×èÌÛÆè"
"¬ÂÍå£/¬ÆÍå£","¬ÂáÖÝ"]
Form204 = ["¬ÂÂè/¬ÂÄè","¬Âá","¬ÂÚÆÛ","¬ÂÂè/¬ÂÄè/¬ÆÂè/¬ÆÄè","¬Æá/¬Âá","¬ÂÚÆÛ/¬ÆÚÆÛ",
"¬ÂáÆ/¬ÆáÆ","¬ÂÚËèÍÚÌè","¬Ââ£","¬Â×èÌâ","¬ÂÚËèÍÚÌè","¬ÂáËèÍ£","¬ÂÚËèÍÚÌè",
"¬Â×èÌÚÂè","¬ÂáËèÍ£","¬Â×èÍ","¬ÂÍå£/¬ÆÍå£","¬ÂáÖÚÌè","¬Â×èÌÛÆè","¬ÂÍå£/¬ÆÍå£",
"¬ÂáÖÝ"]

def main():
    msg1, msg2, msg3, msg4, msg5, msg6 = 'not', 'The subject agrees', 'The sentence is syntactically compatible\n', 'Any subanta in',\
                                         'can be', "Any subanta other than ÍÝÖèÌÄè and ¤×èÌÄè ÕÊèÄ"
    types = ['Noun', 'Pronoun', 'Adjective',  'Verb', 'Upasarga', 'Krdavyaya', 'Avyaya']
    specfs = ['Subject', 'Object', 'Instrument', 'Dative', 'Ablative', 'Genitive', 'Locative', 'Vocative', 'Verb', 'Adjective',
              'Krdanta', 'Krdavyaya', 'Avyaya']
    senvoice = None
    dfirst, trecord, rec, newrec, temptr, temptr1 = None, detail(), detail(), detail(), detail(), detail()
    ifp = open("../../Semantic/FINRES.ACI","r")
    afp = open("../../Semantic/SENOUT.ACI","r")
    rfp = open("Semreslt.aci","w")
    sfp = open("arthaf.aci","w")
    Efp = open("nocode.aci","w")
    y, t, i, j, flag, uncom = None, 0, 0, 0, 0, False
    # stment, subpres, Vocflag = False, False, False
    Asub, Usub, Upaflag = False, False, False
    ifp_lines = ifp.readlines()
    trecords = []
    for line in ifp_lines:
        sub = line[:-1].strip()
        if sub == "": continue
        word = sub.split()
        if msg1 in sub:
            uncom = True
            continue
        elif any([str in sub for str in [msg2, msg3, msg4, msg5, msg6]]):
            if msg5 in sub:
                Asub, Usub = 0, 0
                if sub in ["¤ØÌè", "¥ÔÚÌèè", "ÔÍÌè"]: Asub = 1
                elif sub in ["ÂèÔÌè", "ÍÝÔÚÌèè", "ÍÝÍÌè"]: Usub = 1
            continue
        # num = len(word)
        if word[0] == "ÔÚ³èÍÌè":
            sen = sub
            continue
        if line[0] == "+":
            # trecords.append(dfirst)  # c linked list has to be made into a list!
            noofwords = len(trecords)
            subpres = False
            for trecord in trecords:
                if trecord.type == "Noun" and trecord.specf == "Subject":
                    trecord.subinsen, subpres = 1, True
                    break
                else: continue # only executed if the inner loop did NOT break
            # break # only executed if the inner loop DID break
            if subpres:
                # temptr1 = dfirst
                temptr = detail()
                if Asub == 1 or Usub == 1: temptr.word = sub
                else:
                    temptr = Assignsub(dfirst, temptr, ifp)
                temptr.type, temptr.specf, temptr.dispSpecf, temptr.no_base, temptr.no_codes = "Noun", "Subject", "Subject", 0, 0
                temptr.voice = ["kartari", "karmani"][["ACTIVE", "PASSIVE"].index(senvoice)]
                if Asub == 1: temptr.stem = "¤×èÌÄè"
                elif Usub == 1: temptr.stem = "ÍÝÖèÌÄè"
                temptr.linga, temptr.vibvach, temptr.mode, temptr.sub_no, temptr.no_base, temptr.no_codes, temptr.pos, temptr.matnoun,\
                temptr.subinsen = 0, 0, 0, 0, 0, 0, 0, 0, 0
                dfirst = temptr
            dfirst = AssignSubCode(dfirst, ifp)
            trecords, temptr, subform, genword = CheckMatchingNounForKrdanta(dfirst)
            Vocflag = False
            for trecord in trecords:
                flag = True
                if trecord.specf in ["Vocative", "Adjective"]:
                    Vocflag, flag = True, False
                    break
            if Vocflag:
                if trecord.pos in [1, noofwords]:
                    rfp.writelines(["----------------", "Semantic Analysis of %s  %s  %s Case Not handled"%(trecord.word, trecord.Type, trecord.specf), "----------------"])
                else:
                    rfp.writelines(["----------------", "Incorrect Positioning of %s Vocative \nHence Sentence is Semantically Incompatible\n" % trecord.Type, "----------------"])
            n = 0
            if uncom: flag = False
            if flag: n = searchroot(ifp_lines, afp, rfp, sfp, Efp, dfirst, sen, y)
            if n == 0:
                for aline in afp.readlines():
                    if aline[0] == "-": break
                if flag:
                    for line in ifp_lines:
                        if line[0] == "-": break
            temptr1, temptr, dfirst == None, None, None
            Asub, Usub, uncom, Upaflag = False, False, False, False
            continue
        Vspecf, specf = False, False
        if "VOICE" in word:
            senvoice = word[word.index("VOICE") - 1]
            continue
        # Tspecf, temp = 0, word[1][:-3]
        # for t in range(7):
        #     if temp in types[t]:
        #         Type = types[t]
        #         Tspecf = t + 1
        #         break
        Type = word[0]
        if Type[-3:] == "(s)": Type = Type[:-3]
        Tspecf = types.index(Type) if Type in types else 0
        if Type == "Avyaya": #Tspecf > 0 and t == 6:
                Upaflag = True
                Upaword = word[2]
        # for j in range(13):
        #     if temp in specfs[j]:
        #         if any([temp in str for str in ["Verb", "Krdanta", "Krdavyaya"]]): Vspecf = True
        #         specf = True
        if Type in specfs:
            if any([Type in str for str in ["Verb", "Krdanta", "Krdavyaya"]]):
                Vspecf = True
                j = specfs.index(Type)
            specf = True
        stment = True
        for ch in line:
            if ord(ch) >= 127:
                stment = False
                break
        if specf or Vspecf or not stment:
            if dfirst == None:
                dfirst = detail()
                dfirst.type = Type
                if specfs[j] == "Krdanta": dfirst.specf, dfirst.dispSpecf = "Subject", "Subject"
                else: dfirst.specf, dfirst.dispSpecf = specfs[j], specfs[j]
                dfirst.mean_deno = ""
                k = 2 if ":" in sub else 0
                if specfs[j] == "Vocative":
                    if word[1] == "Øá": dfirst.word = word[k+1] + " " + word[k+2]
                    else: dfirst.word = word[k+1]
                else: dfirst.word = word[k]
                dfirst.voice = ["karthari", "karmani"][["ACTIVE", "PASSIVE"].index(senvoice)]
                dfirst.stem, dfirst.linga, dfirst.vibvach, dfirst.mode, dfirst.sub_no, dfirst.no_base, dfirst.no_codes, dfirst.pos, \
                dfirst.matnoun, dfirst.subinsen = "", 0, 0, 0, 0, 0, 0, 0, 0, 0
                trecords.append(dfirst)
            else:
                trecord, temptr = detail(), detail()
                trecord.type = Type
                k = 2 if ":" in sub else 0
                if specfs[j] == "Vocative":
                    if word[1] == "Øá": trecord.word = word[k + 1] + " " + word[k + 2]
                    else: trecord.word = word[k + 1]
                else: trecord.word = word[k + 1]
                trecord.voice = ["karthari", "karmani"][["ACTIVE", "PASSIVE"].index(senvoice)]
                trecord.stem, trecord.linga, trecord.vibvach, trecord.mode, trecord.sub_no, trecord.no_base, trecord.no_codes, trecord.pos, \
                trecord.matnoun, trecord.subinsen = "", 0, 0, 0, 0, 0, 0, 0, 0, 0
                trecords.append(trecord)
    ifp.close()
    afp.close()
    rfp.close()
    sfp.close()
    Efp.close()
    return n

if __name__ == '__main__':
    main()





