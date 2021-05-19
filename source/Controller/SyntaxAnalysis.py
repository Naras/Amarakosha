import json, source.Controller.data1 as data1, source.Controller.disp as dsp, functools as ft #, icecream as ic
from typing import List

class subanta:
    def __init__(self):
        endRemovedBase = None  # type: str
        pratipadikam = None  # type: str
        code = None  # type: string
class split:
    def __init__(self):
        self.firstWord = [None] * 20  # type: list[str]
        self.secondWord = [None] * 20  # type: list[str]
        self.noOfSplits = None  # type: int
    def get(self):
        return {'firstWord:':self.firstWord[:self.noOfSplits], 'secondWord:':self.secondWord[:self.noOfSplits], 'noOfSplits':self.noOfSplits}
    def __str__(self):
        return json.dumps(self.get())
class split1:
    def __init__(self):
        self.word = [None] * 200  # type: list[str]
        self.noOfWords = None  # type: int
    def get(self):
        return {'word':self.word[:self.noOfWords]}
class result:
    def __init__(self):
        word = [None] * 1000  # type: list[str]
        noOfIdens = None  # type: int

def splitTheWord(word: str) -> split:
    fp = ''  # type: str
    sp = ''  # type: str
    splitWords = split()
    count = 0
    for i, c in enumerate(word[::-1][:len(word)-1]): # reverse traversal, ignore first char in word
        if ord(c) in range(ord('¤'), ord('±')):  # 164-177 (swaras)
            sp = word[i:]
            fp = word[:i]
        elif ord(c) in range(ord('³'),ord('Ø')): # 179-216 (vyanjanas + numbers)
            if ord(word[i + 1]) in range(ord('Ú'),ord('æ')): # 218-230 (kagunita endings)
                sp = chr(ord(word[i + 1]) - (ord('Ú') - ord('¥'))) if ord(word[i + 1]) in range(ord('Ú'),ord('ß')) \
                    else chr(ord(word[i + 1]) - (ord('à') - ord('«')))  # either 218-223 or 224-230
                if i+2 < len(word): sp += word[i + 2]
            elif ord(word[i + 1]) <= ord('£') or ord(word[i + 1]) in range(ord('¤'),ord('Ø')): # 164 - 216 | < 163
                sp += '¤' + word[i + 1]
            elif word[i + 1] == 'è': # 232 halanth
                sp = word[i + 2] if i+2 < len(word) else ''
                fp = word[:i - 1] + 'è'
        if ord(c) in range(ord('¤'),ord('Ø')): # 164-216 (all aksharas)
            if not (fp == '' or sp  == ''):
                splitWords.firstWord[count] = fp
                splitWords.secondWord[count] = sp
                count += 1
        # second possible split
        if ord(c) in range(ord('¤'), ord('Ø')): # 164-216 (all aksharas)
            fp = word[:i]
            sp = word[i:]
            if ord(word[i + 1]) in range(ord('¤'), ord('Ø')):
                if not (fp == '' or sp == ''):
                    splitWords.firstWord[count] = fp
                    splitWords.secondWord[count] = sp
                    count += 1

    splitWords.noOfSplits = count
    splitWord = split()
    i, j = -1, 0
    for k in range(splitWords.noOfSplits):
        i += 1
        splitWord.firstWord[i] = splitWords.firstWord[j]
        splitWord.secondWord[i] = splitWords.secondWord[j]
        j += 1
        if splitWords.firstWord[i] == splitWords.firstWord[i + 1] and splitWords.secondWord[i] == splitWords.secondWord[i + 1]: i += 1
    splitWord.noOfSplits = j
    return splitWord

# Syntax.h
karthari, karmani, fullstop = 0, 1, 'è'
class subanta_data:
    def __init__(self):
        self.vibhakti = [None] * 20  # type: list[int]
        self.vacana = [None] * 20  # type: list[int]
        self.linga = [None] * 20  # type: list[int]
        self.purusha = [None] * 20  # type: list[int]
        self.subanta = [None] * 20  # type: list[str]
        self.pratipadika = [None] * 20  # type: list[str]
        self.erb = [None] * 20  # type: list[str]
        self.wordNum = [None] * 20  # type: list[int]
        self.numofNouns = 0  # type: int
    def get(self):
        return {'vibhakti':self.vibhakti[:self.numofNouns], 'vacana':self.vacana[:self.numofNouns], 'linga':self.linga[:self.numofNouns],
        'purusha':self.purusha[:self.numofNouns], 'subanta':self.subanta[:self.numofNouns], 'pratipadika':self.pratipadika[:self.numofNouns],
        'erb':self.erb[:self.numofNouns], 'wordNum':self.wordNum[:self.numofNouns], 'numofNouns':self.numofNouns}
    def __str__(self):
        return json.dumps(self.get())
class tiganta_data:
    def __init__(self):
        self.dhatuVidha = [None] * 10  # type: list[int]
        self.prayoga = [None] * 10  # type: list[int]
        self.lakara = [None] * 10  # type: list[int]
        self.purusha = [None] * 10  # type: list[int]
        self.vacana = [None] * 10  # type: list[int]
        self.gana = [None] * 10  # type: list[int]
        self.padi = [None] * 10  # type: list[int]
        self.it = [None] * 10  # type: list[int]
        self.karma = [None] * 10  # type: list[int]
        self.tiganta = [None] * 10  # type: list[str]
        self.dhatu = [None] * 10  # type: list[str]
        self.nijdhatu = [None] * 10  # type: list[str]
        self.sandhatu = [None] * 10  # type: list[str]
        self.artha = [None] * 10  # type: list[str]
        self.err = [None] * 10  # type: list[str]
        self.wordNum = [None] * 10  # type: list[int]
        self.numofVerbs = 0  # type: int
    def instance(self,i):
        v = VERB()
        v.wordPos, v.vacana, v.purusha, v.prayoga, v.karma, v.dhatu, v.verb = self.wordNum[i], self.vacana[i], self.purusha[i], self.prayoga[i], self.karma[i], self.dhatu[i], self.tiganta[i]
        return v
    def get(self):
        return {'dhatuVidha':self.dhatuVidha[:self.numofVerbs], 'vacana':self.vacana[:self.numofVerbs], 'lakara':self.lakara[:self.numofVerbs],
                'purusha':self.purusha[:self.numofVerbs], 'gana':self.gana[:self.numofVerbs], 'padi':self.padi[:self.numofVerbs],
                'it':self.it[:self.numofVerbs], 'tiganta':self.tiganta[:self.numofVerbs],'dhatu':self.dhatu[:self.numofVerbs],
                'nijdhatu': self.nijdhatu[:self.numofVerbs],'sandhatu':self.sandhatu[:self.numofVerbs], 'artha':self.artha[:self.numofVerbs],
                'err':self.err[:self.numofVerbs], 'wordNum':self.wordNum[:self.numofVerbs], 'numofVerbs':self.numofVerbs}
    def __str__(self):
        return json.dumps(self.get())
class krdanta_data:
    def __init__(self):
        self.vibhakti = [None] * 20  # type: list[int]
        self.vacana = [None] * 20  # type: list[int]
        self.linga = [None] * 20  # type: list[int]
        self.prayoga = [None] * 20  # type: list[int]
        self.dhatuVidha = [None] * 20  # type: list[int]
        self.krdType = [None] * 20  # type: list[int]
        self.purusha = [None] * 20  # type: list[int]
        self.gana = [None] * 20  # type: list[int]
        self.padi = [None] * 20  # type: list[int]
        self.karma = [None] * 20  # type: list[int]
        self.it = [None] * 20  # type: list[int]
        self.krdanta = [None] * 20  # type: list[str]
        self.pratipadika = [None] * 20  # type: list[str]
        self.dhatu = [None] * 20  # type: list[str]
        self.nijdhatu = [None] * 20  # type: list[str]
        self.sandhatu = [None] * 20  # type: list[str]
        self.artha = [None] * 20  # type: list[str]
        self.erb = [None] * 20  # type: list[str]
        self.wordNum = [None] * 20  # type: list[int]
        self.numofKrdantas = 0  # type: int
    def instance(self,i):
        k = PARTICIPLE()
        k.krdanta, k.vibhakti, k.vacana, k.linga, k.prayoga, k.karma, k.krdType = self.krdanta[i], self.vibhakti[i], self.vacana[i], self.linga[i], self.prayoga[i], self.karma[i], self.krdType[i]
        return k
    def get(self):
        return {'vibhakti':self.vibhakti[:self.numofKrdantas], 'vacana':self.vacana[:self.numofKrdantas], 'linga':self.linga[:self.numofKrdantas],
        'purusha':self.purusha[:self.numofKrdantas], 'prayoga':self.prayoga[:self.numofKrdantas], 'dhatuVidha':self.dhatuVidha[:self.numofKrdantas],
        'gana':self.gana[:self.numofKrdantas], 'padi':self.padi[:self.numofKrdantas], 'it':self.it[:self.numofKrdantas],
        'krdanta':self.krdanta[:self.numofKrdantas], 'pratipadika':self.pratipadika[:self.numofKrdantas], 'dhatu':self.dhatu[:self.numofKrdantas],
        'nijdhatu': self.nijdhatu[:self.numofKrdantas], 'sandhatu':self.sandhatu[:self.numofKrdantas], 'artha':self.artha[self.numofKrdantas],
        'erb':self.erb[:self.numofKrdantas], 'wordNum':self.wordNum[:self.numofKrdantas], 'numofKrdantas':self.numofKrdantas}
    def __str__(self):
        return json.dumps(self.get())
class avyaya_data:
    def __init__(self):
        self.avyava = [None] * 30  # type: list[str]
        self.wordNum = [None] * 30 # type: list[int]
        self.numofAvyayas = 0 # type: int
    def get(self):
        return {'avyaya':self.avyava[:self.numofAvyayas], 'wordNum':self.wordNum[:self.numofAvyayas], 'numofAvyayas':self.numofAvyayasnum}
    def __str__(self):
        return json.dumps(self.get())
class krdav_data:
    def __init__(self):
        self.dhatuVidha = [None] * 20  # type: list[int]
        self.krdavType = [None] * 20  # type: list[int]
        self.purusha = [None] * 20  # type: list[int]
        self.gana = [None] * 20  # type: list[int]
        self.padi = [None] * 20  # type: list[int]
        self.karma = [None] * 20  # type: list[int]
        self.it = [None] * 20  # type: list[int]
        self.krdavyaya = [None] * 20  # type: list[str]
        self.dhatu = [None] * 20  # type: list[str]
        self.nijdhatu = [None] * 20  # type: list[str]
        self.sandhatu = [None] * 20  # type: list[str]
        self.artha = [None] * 20  # type: list[str]
        self.wordNum = [None] * 20  # type: list[int]
        self.numofKrdavyayas = 0  # type: int
    def get(self):
        return {'dhatuVidha': self.dhatuVidha[:self.numofKrdavyayas], 'gana':self.gana[:self.numofKrdavyayas], 'padi': self.padi[:self.numofKrdavyayas], 'it': self.it[:self.numofKrdavyayas],
                'dhatu': self.dhatu[:self.numofKrdavyayas], 'nijdhatu': self.nijdhatu[:self.numofKrdavyayas], 'sandhatu': self.sandhatu[:self.numofKrdavyayas],
                'artha': self.artha[self.numofKrdavyayas], 'krdavyaya': self.krdavyaya[:self.numofKrdavyayas], 'wordNum': self.wordNum[:self.numofKrdavyayas], 'numofKrdavyayas': self.numofKrdavyayas}
    def __str__(self):
        return json.dumps(self.get())
class VIBHAKTI:
    def __init__(self):
        self.word = [None] * 20  # type: list[str]
        self.vibhakti = [None] * 20  # type: list[int]
        self.vacana = [None] * 20 # type: list[int]
        self.purusha = [None] * 20 # type: list[int]
        self.linga = [None] * 20 # type: list[int]
        self.wordPos = [None] * 20 # type: list[int]
        self.numofWords = 0 # type: int
    def get(self):
        return {'word': self.word[:self.numofWords], 'vibhakti':self.vibhakti[:self.numofWords], 'vacana': self.vacana[:self.numofWords], 'purusha': self.purusha[:self.numofWords],
               'linga': self.linga[:self.numofWords], 'wordpos': self.wordPos[:self.numofWords], 'numofWords': self.numofWords}
    def __str__(self):
        return json.dumps(self.get())
class VERB:
    def __init__(self):
        self.verb = None  # type: str
        self.dhatu = None  # type: str
        self.prayoga = None # type: int
        self.karma = None # type: int
        self.vacana = None # type: int
        self.purusha = None # type: int
        self.linga = None # type: int
        self.wordPos = None # type: int
    def get(self):
        return {'verb': self.verb, 'dhatu':self.dhatu, 'prayoga':self.prayoga, 'vacana': self.vacana, 'purusha': self.purusha, 'linga': self.linga, 'wordpos': self.wordPos}
    def __str__(self):
        return json.dumps(self.get())
class PARTICIPLE:
    def __init__(self):
        self.krdanta = None  # type: str
        self.vibhakti = None  # type: str
        self.vacana = None # type: int
        self.prayoga = None # type: int
        self.linga = None # type: int
        self.karma = None # type: int
        self.krdType = None # type: int
    def get(self):
        return {'krdanta': self.krdanta, 'vibhakti':self.vibhakti, 'vacana': self.vacana, 'prayoga': self.prayoga, 'linga': self.linga, 'karma': self.karma, 'krdType': self.krdType}
    def __str__(self):
        return json.dumps(self.get())

class record:
    def __init__(self):
        self.sentence = None  #type str
        self.idens = [None] * 100  # type: list[str]
        self.numofIdens = None  #type int
    def get(self):
        return {'sentence':self.sentence, 'idens':self.idens[:self.numofIdens], 'numofIdens':self.numofIdens}
    def __str__(self):
        return json.dumps(self.get())
class word:
    def __init__(self):
        self.iden = [0] * 30  # type: list[str]
        self.numofIdens = None  #type int
    def get(self):
        return {'iden':self.iden[:self.numofIdens], 'numofWords':self.numofIdens}
    def __str__(self):
        return json.dumps(self.get())
class typeWord:
    def __init__(self):
        self.word = [None] * 15  # type: list[str]
        self.numofWords = None  #type int
    def get(self):
        return {'word':self.word[:self.numofWords], 'numofWords':self.numofWords}
    def __str__(self):
        return json.dumps(self.get())
def generateTable(rec: record) -> (List, List):
    wOrd = [None] * 10
    # rEcord = [None] * 100  # type: list[str]
    # field = [None] * 10   # type: list[str]
    wordNum, m, j, fpo = 1, 0, 0, []
    wOrd[m] = word()
    for iden in rec.idens[:rec.numofIdens]:
        # fpo.append[rec.sentence]
        # for iden in reco.idens: fpo.append(iden)
        splitSen = split1()
        splitSen.word = iden.split(' ')
        splitSen.noOfWords = len(splitSen.word)
        num = int(splitSen.word[0][0])
        if num != wordNum:
            wOrd[m].numofIdens = j
            m += 1
            wOrd[m] = word()
            j = 0
            wordNum = num
        wOrd[m].iden[j] = iden[:-1]
        j += 1
    wOrd[m].numofIdens = j
    numOfWords = m + 1

    # wordNum = 0
    # return wOrd[:numOfWords]
    # tempout = []
    # ic.ic(numOfWords, [w.get() for w in wOrd if w != None])
    tempout = temp(numOfWords, wOrd, 0)

    return wOrd[:numOfWords], tempout
def temp(numOfWords: int, wrds: List[word], i: int) -> List:
    tempout = []
    if i < numOfWords:
        for iden in wrds[i].iden[:wrds[i].numofIdens]:
            tempout.append(iden)
            tmp = temp(numOfWords, wrds, i+1)
            if not tmp == []:
                tmp2 = [None]*len(tmp)
                for ii, item in enumerate(tmp):
                    tmp2[ii] = [iden, item]
                tmp = tmp2
            if not tmp == []: tempout = tempout[:-1] + tmp
    # else: tempout = ['--------']
    return tempout
def listdepth(item, depth: int) -> int:
    if isinstance(item, list):
        depth += 1
        depths = []
        for item2 in item:
            depths.append(listdepth(item2, depth))
        depth = max(depths)
    return depth

def checkForSyntacticCompatibility(rec: record) -> List[str]:
    def assign_subanta() -> subanta_data:
        # noun = subanta_data()
        noun.subanta[noun.numofNouns] = splitSen[1]
        noun.pratipadika[noun.numofNouns] = splitSen[4]
        noun.erb[noun.numofNouns] = splitSen[5]
        noun.vibhakti[noun.numofNouns] = (int(splitSen[7]) - 1) // 3 + 1
        noun.vacana[noun.numofNouns] = (int(splitSen[7]) - 1) % 3 + 1
        noun.linga[noun.numofNouns] = ord(splitSen[6][1]) - 48
        noun.purusha[noun.numofNouns] = {'ÍÝÖèÌÄè':2, '¤×èÌÄè':3,}.get(splitSen[3], 1)
        noun.wordNum[noun.numofNouns] = m
        word.word[m] = 'subanta'
        noun.numofNouns += 1
        return noun
    def assign_krdanta() -> krdanta_data:
        # participle = krdanta_data()
        participle.krdanta[participle.numofKrdantas] = splitSen[1]
        participle.pratipadika[participle.numofKrdantas] = splitSen[4]
        participle.erb[participle.numofKrdantas] = splitSen[5]
        participle.dhatu[participle.numofKrdantas] = splitSen[10]
        participle.nijdhatu[participle.numofKrdantas] = splitSen[11]
        participle.sandhatu[participle.numofKrdantas] = splitSen[12]
        listKarmas = splitSen[16].split('/')
        for count, temp in enumerate(listKarmas):
            participle.artha[participle.numofKrdantas] = temp #'Meaning'
            if len(temp) > 1: tmp = temp[len(temp) - 1]
            else: tmp = temp
            karma[count] = ord(tmp) - 48
        karmaflag = True
        for ln in range(len(listKarmas)-1):
            if karma[ln] != karma[ln + 1]:
                karmaflag = False;
                break;
        participle.karma[participle.numofKrdantas] = karma[0] if karmaflag else 0
        participle.gana[participle.numofKrdantas] = ord(splitSen[14][0]) - 48
        participle.padi[participle.numofKrdantas] = ord(splitSen[14][1]) - 48
        participle.it[participle.numofKrdantas] = ord(splitSen[14][2]) - 48
        participle.vibhakti[participle.numofKrdantas] = (int(splitSen[7]) - 1) // 3 + 1
        participle.vacana[participle.numofKrdantas] = (int(splitSen[7]) - 1) % 3 + 1
        participle.linga[participle.numofKrdantas] = ord(splitSen[6][1]) - 48
        participle.krdType[participle.numofKrdantas] = ord(splitSen[8][0]) - 96
        participle.dhatuVidha[participle.numofKrdantas] = ord(splitSen[8][1]) - 47
        participle.purusha[participle.numofKrdantas] = 0
        participle.prayoga[participle.numofKrdantas] = {1:1, 2:1, 3:1, 7:1, 9:1, 4:2, 5:0, 6:0, 8:0}[participle.krdType[participle.numofKrdantas]]
        participle.wordNum[participle.numofKrdantas] = m
        word.word[m] = 'krdanta'
        participle.numofKrdantas += 1
        return participle
    def assign_avyaya() -> avyaya_data:
        # indeclinable = avyaya_data()
        indeclinable.avyava[indeclinable.numofAvyayas] = splitSen[0]
        indeclinable.wordNum[indeclinable.numofAvyayas] = m
        word.word[m] = 'avyaya'
        return indeclinable
    def assign_krdav() -> krdav_data:
        # krdav = krdav_data()
        krdav.krdavyaya[krdav.numofKrdavyayas] = splitSen[0]
        krdav.dhatu[krdav.numofKrdavyayas] = splitSen[5]
        krdav.nijdhatu[krdav.numofKrdavyayas] = splitSen[6]
        krdav.sandhatu[krdav.numofKrdavyayas] = splitSen[7]
        listKarmas = splitSen[8].split('/')
        for count, temp in enumerate(listKarmas):
            krdav.artha[krdav.numofKrdavyayas] = temp #'Meaning'
            krdav.karma[krdav.numofKrdavyayas] = int(temp[:-1]) - 48
        krdav.dhatuVidha[krdav.numofKrdavyayas] = int(splitSen[3][1]) - 48
        krdav.krdavType[krdav.numofKrdavyayas] = int(splitSen[3][0]) - 96
        krdav.gana[krdav.numofKrdavyayas] = int(splitSen[9][0]) - 48
        krdav.padi[krdav.numofKrdavyayas] = int(splitSen[9][1]) - 48
        krdav.it[krdav.numofKrdavyayas] = int(splitSen[9][2]) - 48
        krdav.wordNum[krdav.numofKrdavyayas] = m
        word.word[m] = 'krdav'
        return krdav
    def assign_tiganta() -> tiganta_data:
        # verb = tiganta_data()
        verb.tiganta[verb.numofVerbs] = splitSen[1]
        verb.err[verb.numofVerbs] = splitSen[4]
        verb.dhatu[verb.numofVerbs] = splitSen[6]
        verb.nijdhatu[verb.numofVerbs] = splitSen[7]
        verb.sandhatu[verb.numofVerbs] = splitSen[8]
        listKarmas = splitSen[9].split('/')
        for count, temp in enumerate(listKarmas):
            verb.artha[verb.numofVerbs] = temp  # 'Meaning'
            # if len(temp) > 1: tmp = temp[len(temp) - 1]
            # else: tmp = temp
            # if tmp in range(ord('0'),ord('9')): verb.karma[verb.numofVerbs] = ord(tmp) - 48
            # else: verb.karma[verb.numofVerbs] = karthari
        verb.karma[verb.numofVerbs] = int(splitSen[14]) - 1
        verb.dhatuVidha[verb.numofVerbs] = ord(splitSen[11][0]) - 48
        verb.prayoga[verb.numofVerbs] = (ord(splitSen[11][1]) - 65) % 2
        verb.lakara[verb.numofVerbs] = (ord(splitSen[11][1]) - 65) // 2
        verb.purusha[verb.numofVerbs] = (int(splitSen[12]) - 1) // 3
        verb.vacana[verb.numofVerbs] = int(splitSen[12]) % 3
        verb.gana[verb.numofVerbs] = ord(splitSen[10][0]) - 48
        verb.padi[verb.numofVerbs] = ord(splitSen[10][1]) - 48
        verb.it[verb.numofVerbs] = ord(splitSen[10][2]) - 48
        word.word[m] = 'tiganta'
        verb.wordNum[verb.numofVerbs] = m
        verb.numofVerbs += 1
        return verb
    # i, j, k, l, zz, ii, jj = 0, 0, 0, 0, 0, 0
    karma = [None] * 50  # type: list[int]
    karmaflag = None  # type: bool
    # count = None  # type: int
    noun, adj, pro, verb, participle, krdav, indeclinable, word = subanta_data(), subanta_data(), subanta_data(), tiganta_data(), krdanta_data(), krdav_data(), avyaya_data(), typeWord()
    arg = [None] * 7
    for m in range(rec.numofIdens):
        splitSen = rec.idens[m][:-1].split()
        case = int(splitSen[3])
        if not splitSen[1] == 'Øá':
            func = [assign_subanta, assign_krdanta, assign_avyaya, assign_krdav, assign_tiganta, assign_subanta, assign_subanta][case - 1]
            arg[case - 1] = func()
    noun, participle, indeclinable, krdav, verb, adj, pro = arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6]
    word.numofWords = rec.numofIdens - 1
    if verb != None and verb.numofVerbs > 0:
        result = checkCompatibility1(rec, noun, verb, participle, indeclinable, krdav, adj, pro, word)
    elif participle != None and participle.numofKrdantas > 0:
        qflag, result = checkCompatibility(rec, noun, participle, indeclinable, krdav, adj, pro)
    else: result = dispMesgNoun(rec, noun, indeclinable, krdav, adj, pro)
    return result
def checkCompatibility1(rec: record, noun: subanta_data, verb: tiganta_data, participle: krdanta_data, indeclinable: avyaya_data, krdav: krdav_data, adj: subanta_data, pro: subanta_data, word: typeWord) -> List[str]:
    # krdtemp = krdanta_data()
    # Verb = VERB()
    # subject, object, locative, instrument, third, dative, ablative, vocative, genitive, second = \
    #     VIBHAKTI(), VIBHAKTI(), VIBHAKTI(), VIBHAKTI(), VIBHAKTI(), VIBHAKTI(), VIBHAKTI(), VIBHAKTI(), VIBHAKTI()
    flag = [None] * 9  # type: list[str]
    dvithiya = None # type: str
    def assign_prathama_vibhakti() -> None:
        if verb.prayoga[i] == karthari:
            subject.word[subject.numofWords] = noun.subanta[j]
            subject.vibhakti[subject.numofWords] = noun.vibhakti[j]
            subject.vacana[subject.numofWords] = noun.vacana[j]
            subject.purusha[subject.numofWords] = noun.purusha[j]
            subject.linga[subject.numofWords] = noun.linga[j]
            subject.wordPos[subject.numofWords] = noun.wordNum[j]
            subject.numofWords += 1
        elif verb.prayoga[i] == karmani:
            object.word[object.numofWords] = noun.subanta[j]
            object.vibhakti[object.numofWords] = noun.vibhakti[j]
            object.vacana[object.numofWords] = noun.vacana[j]
            object.purusha[object.numofWords] = noun.purusha[j]
            object.linga[object.numofWords] = noun.linga[j]
            object.wordPos[object.numofWords] = noun.wordNum[j]
            object.numofWords += 1
        return
    def assign_dvithiya_vibhakti() -> None:
        if verb.prayoga[i] == karthari:
            object.word[object.numofWords] = noun.subanta[j]
            object.vibhakti[object.numofWords] = noun.vibhakti[j]
            object.vacana[object.numofWords] = noun.vacana[j]
            object.purusha[object.numofWords] = noun.purusha[j]
            object.linga[object.numofWords] = noun.linga[j]
            object.wordPos[object.numofWords] = noun.wordNum[j]
            object.numofWords += 1
        elif verb.prayoga[i] == karmani:
            second.word[second.numofWords] = noun.subanta[j]
            second.vibhakti[second.numofWords] = noun.vibhakti[j]
            second.vacana[second.numofWords] = noun.vacana[j]
            second.purusha[second.numofWords] = noun.purusha[j]
            second.linga[second.numofWords] = noun.linga[j]
            second.wordPos[second.numofWords] = noun.wordNum[j]
            second.numofWords += 1
        return
    def assign_trithiya_vibhakti() -> None:
        if verb.prayoga[i] == karthari:
            instrument.word[instrument.numofWords] = noun.subanta[j]
            instrument.vibhakti[instrument.numofWords] = noun.vibhakti[j]
            instrument.vacana[instrument.numofWords] = noun.vacana[j]
            instrument.purusha[instrument.numofWords] = noun.purusha[j]
            instrument.linga[instrument.numofWords] = noun.linga[j]
            instrument.wordPos[instrument.numofWords] = noun.wordNum[j]
            instrument.numofWords += 1
        elif verb.prayoga[i] == karmani:
            third.word[third.numofWords] = noun.subanta[j]
            third.vibhakti[third.numofWords] = noun.vibhakti[j]
            third.vacana[third.numofWords] = noun.vacana[j]
            third.purusha[third.numofWords] = noun.purusha[j]
            third.linga[third.numofWords] = noun.linga[j]
            third.wordPos[third.numofWords] = noun.wordNum[j]
            third.numofWords += 1
        return
    def assign_chaturthi_vibhakti() -> None:
        dative.word[dative.numofWords] = noun.subanta[j]
        dative.vibhakti[dative.numofWords] = noun.vibhakti[j]
        dative.vacana[dative.numofWords] = noun.vacana[j]
        dative.purusha[dative.numofWords] = noun.purusha[j]
        dative.linga[dative.numofWords] = noun.linga[j]
        dative.wordPos[dative.numofWords] = noun.wordNum[j]
        dative.numofWords += 1
        return
    def assign_pancami_vibhakti() -> None:
        ablative.word[ablative.numofWords] = noun.subanta[j]
        ablative.vibhakti[ablative.numofWords] = noun.vibhakti[j]
        ablative.vacana[ablative.numofWords] = noun.vacana[j]
        ablative.purusha[ablative.numofWords] = noun.purusha[j]
        ablative.linga[ablative.numofWords] = noun.linga[j]
        ablative.wordPos[ablative.numofWords] = noun.wordNum[j]
        ablative.numofWords += 1
        return
    def assign_shashti_vibhakti() -> None:
        genitive.word[genitive.numofWords] = noun.subanta[j]
        genitive.vibhakti[genitive.numofWords] = noun.vibhakti[j]
        genitive.vacana[genitive.numofWords] = noun.vacana[j]
        genitive.purusha[genitive.numofWords] = noun.purusha[j]
        genitive.linga[genitive.numofWords] = noun.linga[j]
        genitive.wordPos[genitive.numofWords] = noun.wordNum[j]
        genitive.numofWords += 1
        return
    def assign_saptami_vibhakti() -> None:
        locative.word[locative.numofWords] = noun.subanta[j]
        locative.vibhakti[locative.numofWords] = noun.vibhakti[j]
        locative.vacana[locative.numofWords] = noun.vacana[j]
        locative.purusha[locative.numofWords] = noun.purusha[j]
        locative.linga[locative.numofWords] = noun.linga[j]
        locative.wordPos[locative.numofWords] = noun.wordNum[j]
        locative.numofWords += 1
        return
    def assign_ashtami_vibhakti() -> None:
        vocative.word[vocative.numofWords] = noun.subanta[j]
        vocative.vibhakti[vocative.numofWords] = noun.vibhakti[j]
        vocative.vacana[vocative.numofWords] = noun.vacana[j]
        vocative.purusha[vocative.numofWords] = noun.purusha[j]
        vocative.linga[vocative.numofWords] = noun.linga[j]
        vocative.wordPos[vocative.numofWords] = noun.wordNum[j]
        vocative.numofWords += 1
        return
    qflag, result = False, []
    subject, instrument, second, third = None, None, None, None
    object, locative, dative, ablative, vocative, genitive = VIBHAKTI(), VIBHAKTI(), VIBHAKTI(), VIBHAKTI(), VIBHAKTI(), VIBHAKTI()
    for i in range(verb.numofVerbs):
        vrb = verb.instance(i)
        if vrb.prayoga == karthari: subject, instrument = VIBHAKTI(), VIBHAKTI()
        elif vrb.prayoga == karmani: second, third = VIBHAKTI(), VIBHAKTI()
        krdtemp = getKrdantadata(participle, verb.tiganta[i])
        if noun != None:
            for j in range(noun.numofNouns):
                if not verb.tiganta == noun.subanta[j]:
                    func = [assign_prathama_vibhakti, assign_dvithiya_vibhakti, assign_trithiya_vibhakti, assign_chaturthi_vibhakti,
                    assign_pancami_vibhakti, assign_shashti_vibhakti, assign_saptami_vibhakti, assign_ashtami_vibhakti][noun.vibhakti[j] - 1]
                    func()
        counter = ord('a') - 1
        if verb.karma[i] == 0 and object.numofWords > 0:
                karmaFlag = 0
                while verb.karma[i] < 3:
                    verb.karma[i] += 1
                    dvithiya = ''
                    if verb.prayoga[i] == karmani:
                        for aa in range(second.numofWords):
                            dvithiya += second.word[aa] + '/'
                        for aa in range(third.numofWords):
                            subject, instrument = VIBHAKTI(), VIBHAKTI()
                            for bb in range(third.numofWords):
                                subject.word[subject.numofWords] = third.word[bb]
                                subject.vibhakti[subject.numofWords] == third.vibhakti[bb]
                                subject.vacana[subject.numofWords] == third.vacana[bb]
                                subject.purusha[subject.numofWords] == third.purusha[bb]
                                subject.linga[subject.numofWords] == third.linga[bb]
                                subject.wordPos[subject.numofWords] == third.wordPos[bb]
                                subject.numofwords += 1
                            for cc in range(third.numofWords):
                                flagn = False
                                for bb in range(third.numofWords):
                                    if third.word[cc] == subject.word[bb]:
                                        flagn = True
                                        break
                                if not flagn:
                                    instrument.word[instrument.numofWords] = third.word[cc]
                                    instrument.vibhakti[instrument.numofWords] = third.vibhakti[cc]
                                    instrument.vacana[subject.numofWords] == third.vacana[cc]
                                    instrument.purusha[subject.numofWords] == third.purusha[cc]
                                    instrument.linga[subject.numofWords] == third.linga[cc]
                                    instrument.linga[subject.numofWords] == third.linga[cc]
                                    instrument.wordPos[subject.numofWords] == third.wordPos[cc]
                                    instrument.numofwords += 1
                            counter += 1
                            if participle != None: qflag, result = syntacticCheck(rec, adj, pro, krdav, indeclinable, vrb, subject, object, locative, instrument, dative, ablative, vocative,
                                                   genitive, krdtemp, verb, participle.numofKrdantas, counter, dvithiya, karmaFlag, word)
                    else:
                        counter += 1
                        qflag, result = syntacticCheck(adj, pro, krdav, indeclinable, vrb, subject, object, locative,instrument, dative, ablative, vocative,
                                               genitive, krdtemp, verb, verb.numofVerbs, counter, dvithiya, karmaFlag, word)
                verb.karma[i] = 0
        else:
                karmaFlag = verb.karma[i]
                dvithiya = ''
                if verb.prayoga[i] == karmani:
                    for aa in range(second.numofWords):
                        dvithiya += second.word[aa] + '/'
                    for aa in range(third.numofWords):
                        subject, instrument = VIBHAKTI(), VIBHAKTI()
                        for bb in range(third.numofWords):
                            subject.word[subject.numofWords] = third.word[bb]
                            subject.vibhakti[subject.numofWords] == third.vibhakti[bb]
                            subject.vacana[subject.numofWords] == third.vacana[bb]
                            subject.purusha[subject.numofWords] == third.purusha[bb]
                            subject.linga[subject.numofWords] == third.linga[bb]
                            subject.linga[subject.numofWords] == third.linga[bb]
                            subject.wordPos[subject.numofWords] == third.wordPos[bb]
                            subject.numofwords += 1
                        for cc in range(third.numofWords):
                            flagn = False
                            for bb in range(third.numofWords):
                                if third.word[cc] == subject.word[bb]:
                                    flagn = True
                                    break
                            if not flagn:
                                instrument.word[instrument.numofWords] = third.word[cc]
                                instrument.vibhakti[instrument.numofWords] = third.vibhakti[cc]
                                instrument.vacana[subject.numofWords] == third.vacana[cc]
                                instrument.purusha[subject.numofWords] == third.purusha[cc]
                                instrument.linga[subject.numofWords] == third.linga[cc]
                                instrument.linga[subject.numofWords] == third.linga[cc]
                                instrument.wordPos[subject.numofWords] == third.wordPos[cc]
                                instrument.numofwords += 1
                        counter += 1
                        qflag, result = syntacticCheck(rec, adj, pro, krdav, indeclinable, vrb, subject, object, locative,instrument, dative, ablative, vocative,
                                               genitive, krdtemp, verb, verb.numofVerbs, counter, dvithiya, karmaFlag, word)
                else: qflag, result = syntacticCheck(adj, pro, krdav, indeclinable, vrb, subject, object, locative, instrument, dative, ablative, vocative,
                                               genitive, krdtemp, verb, verb.numofVerbs, counter, dvithiya, karmaFlag, word)
        if not qflag: break
    return result
def checkCompatibility(rec: record, noun: subanta_data, participle: krdanta_data, indeclinable: avyaya_data, krdav: krdav_data, adj: subanta_data, pro: subanta_data) -> bool:
    saflag = False
    for i in range(participle.numofKrdantas):
        if participle.krdType[i] == 4:
            saflag = participle.karma[i] == 0
            if participle.karma[i] == 2:
                participle.prayoga[i] = 0
                qflag = checkCompatibility2(rec, noun, participle, indeclinable, i, saflag, krdav, adj, pro)
            elif participle.karma[i] == 1:
                participle.prayoga[i] = 0
                qflag = checkCompatibility2(rec, noun, participle, indeclinable, i, saflag, krdav, adj, pro)
                participle.prayoga[i] = 1
                qflag, result = checkCompatibility2(rec, noun, participle, indeclinable, i, saflag, krdav, adj, pro)
        else:  qflag, result = checkCompatibility2(rec, noun, participle, indeclinable, i, saflag, krdav, adj, pro)
        if not qflag: break
    return qflag, result
def checkCompatibility2(rec: record, noun: subanta_data, participle: krdanta_data, indeclinable: avyaya_data, i: int, saflag: bool, krdav: krdav_data, adj: subanta_data, pro: subanta_data) -> bool:
    def assign_prathama_vibhakti() -> None:
        if krdanta.prayoga == karthari:
            subject.word[subject.numofWords] = noun.subanta[i]
            subject.vibhakti[subject.numofWords] = noun.vibhakti[i]
            subject.vacana[subject.numofWords] = noun.vacana[i]
            subject.purusha[subject.numofWords] = noun.purusha[i]
            subject.linga[subject.numofWords] = noun.linga[i]
            subject.wordPos[subject.numofWords] = noun.wordNum[i]
            subject.numofWords += 1
        elif krdanta.prayoga[i] == karmani:
            object.word[object.numofWords] = noun.subanta[i]
            object.vibhakti[object.numofWords] = noun.vibhakti[i]
            object.vacana[object.numofWords] = noun.vacana[i]
            object.purusha[object.numofWords] = noun.purusha[i]
            object.linga[object.numofWords] = noun.linga[i]
            object.wordPos[object.numofWords] = noun.wordNum[i]
            object.numofWords += 1
        return
    def assign_dvithiya_vibhakti() -> None:
        if krdanta.prayoga == karthari:
            object.word[object.numofWords] = noun.subanta[i]
            object.vibhakti[object.numofWords] = noun.vibhakti[i]
            object.vacana[object.numofWords] = noun.vacana[i]
            object.purusha[object.numofWords] = noun.purusha[i]
            object.linga[object.numofWords] = noun.linga[i]
            object.wordPos[object.numofWords] = noun.wordNum[i]
            object.numofWords += 1
        elif krdanta.prayoga == karmani:
            second.word[second.numofWords] = noun.subanta[i]
            second.vibhakti[second.numofWords] = noun.vibhakti[i]
            second.vacana[second.numofWords] = noun.vacana[i]
            second.purusha[second.numofWords] = noun.purusha[i]
            second.linga[second.numofWords] = noun.linga[i]
            second.wordPos[second.numofWords] = noun.wordNum[i]
            second.numofWords += 1
        return
    def assign_trithiya_vibhakti() -> None:
        if krdanta.prayoga == karthari:
            instrument.word[instrument.numofWords] = noun.subanta[i]
            instrument.vibhakti[instrument.numofWords] = noun.vibhakti[i]
            instrument.vacana[instrument.numofWords] = noun.vacana[i]
            instrument.purusha[instrument.numofWords] = noun.purusha[i]
            instrument.linga[instrument.numofWords] = noun.linga[i]
            instrument.wordPos[instrument.numofWords] = noun.wordNum[i]
            instrument.numofWords += 1
        elif krdanta.prayoga[i] == karmani:
            third.word[third.numofWords] = noun.word[i]
            third.vibhakti[third.numofWords] = noun.vibhakti[i]
            third.vacana[third.numofWords] = noun.vacana[i]
            third.purusha[third.numofWords] = noun.purusha[i]
            third.linga[third.numofWords] = noun.linga[i]
            third.wordPos[third.numofWords] = noun.wordNum[i]
            third.numofWords += 1
        return
    def assign_chaturthi_vibhakti() -> None:
        dative.word[dative.numofWords] = noun.subanta[i]
        dative.vibhakti[dative.numofWords] = noun.vibhakti[i]
        dative.vacana[dative.numofWords] = noun.vacana[i]
        dative.purusha[dative.numofWords] = noun.purusha[i]
        dative.linga[dative.numofWords] = noun.linga[i]
        dative.wordPos[dative.numofWords] = noun.wordNum[i]
        dative.numofWords += 1
        return
    def assign_pancami_vibhakti() -> None:
        ablative.word[ablative.numofWords] = noun.subanta[i]
        ablative.vibhakti[ablative.numofWords] = noun.vibhakti[i]
        ablative.vacana[ablative.numofWords] = noun.vacana[i]
        ablative.purusha[ablative.numofWords] = noun.purusha[i]
        ablative.linga[ablative.numofWords] = noun.linga[i]
        ablative.wordPos[ablative.numofWords] = noun.wordNum[i]
        ablative.numofWords += 1
        return
    def assign_shashti_vibhakti() -> None:
        genitive.word[genitive.numofWords] = noun.subanta[i]
        genitive.vibhakti[genitive.numofWords] = noun.vibhakti[i]
        genitive.vacana[genitive.numofWords] = noun.vacana[i]
        genitive.purusha[genitive.numofWords] = noun.purusha[i]
        genitive.linga[genitive.numofWords] = noun.linga[i]
        genitive.wordPos[genitive.numofWords] = noun.wordNum[i]
        genitive.numofWords += 1
        return
    def assign_saptami_vibhakti() -> None:
        locative.word[locative.numofWords] = noun.subanta[i]
        locative.vibhakti[locative.numofWords] = noun.vibhakti[i]
        locative.vacana[locative.numofWords] = noun.vacana[i]
        locative.purusha[locative.numofWords] = noun.purusha[i]
        locative.linga[locative.numofWords] = noun.linga[i]
        locative.wordPos[locative.numofWords] = noun.wordNum[i]
        locative.numofWords += 1
        return
    def assign_ashtami_vibhakti() -> None:
        vocative.word[vocative.numofWords] = noun.subanta[i]
        vocative.vibhakti[vocative.numofWords] = noun.vibhakti[i]
        vocative.vacana[vocative.numofWords] = noun.vacana[i]
        vocative.purusha[vocative.numofWords] = noun.purusha[i]
        vocative.linga[vocative.numofWords] = noun.linga[i]
        vocative.wordPos[vocative.numofWords] = noun.wordNum[i]
        vocative.numofWords += 1
        return
    if participle.prayoga[i] == karthari: subject, instrument = VIBHAKTI(), VIBHAKTI()
    elif participle.prayoga[i] == karmani: third, second = VIBHAKTI(), VIBHAKTI()
    object, locative, dative, ablative, vocative, genitive = VIBHAKTI(), VIBHAKTI(), VIBHAKTI(), VIBHAKTI(), VIBHAKTI(), VIBHAKTI()
    krdanta = participle.instance(i)
    for i in range(noun.numofNouns):
        if krdanta.krdanta == noun.subanta[i]: continue
        func = [assign_prathama_vibhakti, assign_dvithiya_vibhakti, assign_trithiya_vibhakti, assign_chaturthi_vibhakti,
                assign_pancami_vibhakti, assign_shashti_vibhakti, assign_saptami_vibhakti, assign_ashtami_vibhakti][noun.vibhakti[i] - 1]
        func()
        counter = ord('a') - 1
        if krdanta.karma == 0 and object.numofWords > 0:
            karmaFlag = 0
            while krdanta.karma < 3:
                krdanta.karma += 1
                dvithiya = ''
                if krdanta.prayoga == karmani:
                    for aa in range(second.numofWords):
                        dvithiya += second.word[aa] + '/'
                    for aa in range(third.numofWords):
                        subject, instrument = VIBHAKTI(), VIBHAKTI()
                        for bb in range(third.numofWords):
                            subject.word[subject.numofWords] = third.word[bb]
                            subject.vibhakti[subject.numofWords] == third.vibhakti[bb]
                            subject.vacana[subject.numofWords] == third.vacana[bb]
                            subject.purusha[subject.numofWords] == third.purusha[bb]
                            subject.linga[subject.numofWords] == third.linga[bb]
                            subject.linga[subject.numofWords] == third.linga[bb]
                            subject.wordPos[subject.numofWords] == third.wordPos[bb]
                            subject.numofwords += 1
                        for cc in range(third.numofWords):
                            flagn = False
                            for bb in  range(third.numofWords):
                                if third.word[cc] == subject.word[bb]:
                                    flagn = True
                                    break
                            if flagn:
                                instrument.word[instrument.numofWords] = third.word[cc]
                                instrument.vibhakti[instrument.numofWords] = third.vibhakti[cc]
                                instrument.vacana[subject.numofWords] == third.vacana[cc]
                                instrument.purusha[subject.numofWords] == third.purusha[cc]
                                instrument.linga[subject.numofWords] == third.linga[cc]
                                instrument.linga[subject.numofWords] == third.linga[cc]
                                instrument.wordPos[subject.numofWords] == third.wordPos[cc]
                                instrument.numofwords += 1
                        counter += 1
                        qflag, result = syntacticCheck1(adj, pro, krdav, indeclinable, krdanta, subject, object, locative, instrument, dative, ablative, vocative,
                                               genitive, participle, participle.numofKrdantas, counter, dvithiya, karmaFlag, word)
                else:
                    counter += 1
                    qflag, result = syntacticCheck1(adj, pro, krdav, indeclinable, krdanta, subject, object, locative, instrument, dative, ablative, vocative,
                                               genitive, participle, participle.numofKrdantas, counter, dvithiya, karmaFlag, word)
            krdanta.karma = 0
        else:
            karmaFlag = krdanta.karma
            dvithiya = ''
            if krdanta.prayoga == karmani:
                for aa in range(second.numofWords):
                    dvithiya += second.word[aa] + '/'
                for aa in range(third.numofWords):
                    subject, instrument = VIBHAKTI(), VIBHAKTI()
                    for bb in range(third.numofWords):
                        subject.word[subject.numofWords] = third.word[bb]
                        subject.vibhakti[subject.numofWords] == third.vibhakti[bb]
                        subject.vacana[subject.numofWords] == third.vacana[bb]
                        subject.purusha[subject.numofWords] == third.purusha[bb]
                        subject.linga[subject.numofWords] == third.linga[bb]
                        subject.linga[subject.numofWords] == third.linga[bb]
                        subject.wordPos[subject.numofWords] == third.wordPos[bb]
                        subject.numofwords += 1
                    for cc in range(third.numofWords):
                        flagn = False
                        for bb in range(third.numofWords):
                            if third.word[cc] == subject.word[bb]:
                                flagn = True
                                break
                        if flagn:
                            instrument.word[instrument.numofWords] = third.word[cc]
                            instrument.vibhakti[instrument.numofWords] = third.vibhakti[cc]
                            instrument.vacana[subject.numofWords] == third.vacana[cc]
                            instrument.purusha[subject.numofWords] == third.purusha[cc]
                            instrument.linga[subject.numofWords] == third.linga[cc]
                            instrument.linga[subject.numofWords] == third.linga[cc]
                            instrument.wordPos[subject.numofWords] == third.wordPos[cc]
                            instrument.numofwords += 1
                    counter += 1
                    qflag, result = syntacticCheck1(rec, adj, pro, krdav, indeclinable, krdanta, subject, object, locative,instrument, dative, ablative, vocative,
                                           genitive, participle, participle.numofKrdantas, counter, dvithiya, karmaFlag, saflag)
            else: qflag, result = syntacticCheck1(adj, pro, krdav, indeclinable, krdanta, subject, object, locative, instrument, dative, ablative, vocative,
                                           genitive, participle, participle.numofKrdantas, counter, dvithiya, karmaFlag, saflag)
    return qflag, result
def dispMesgNoun(rec: record, noun: subanta_data, indeclinable: avyaya_data, krdav: krdav_data, adj: subanta_data, pro: subanta_data) -> List[str]:
    result = [rec.sentence]
    for c, cl in enumerate(noun, adj, pro):
        result.append(['Noun(s) are:', 'Adjective(s) are:', 'Pronoun(s) are:'][c])
        for i in range(cl.numofNouns):result.append('%s, '%cl.subanta[i])
    result.append('Avyaya(s) are:')
    for i in range(indeclinable.numofAvyayas): result.append('%s, ' % indeclinable.avyava[i])
    result.append('krdavyaya(s) are:')
    for i in range(krdav.numofKrdavyayas): result.append('%s, ' % krdav.krdavyava[i])
    return result
def getKrdantadata(participle: krdanta_data, tiganta: str) -> krdanta_data():
    krdtemp, m = krdanta_data(), 0
    if participle != None:
        for k in range(participle.numofKrdantas):
           if tiganta != participle.krdanta[k]:
               krdtemp.vibhakti[m] = participle.vibhakti[k]
               krdtemp.vacana[m] = participle.vacana[k]
               krdtemp.linga[m] = participle.linga[k]
               krdtemp.prayoga[m] = participle.prayoga[k]
               krdtemp.dhatuVidha[m] = participle.dhatuVidha[k]
               krdtemp.krdType[m] = participle.krdType[k]
               krdtemp.purusha[m] = participle.purusha[k]
               krdtemp.gana[m] = participle.gana[k]
               krdtemp.padi[m] = participle.padi[k]
               krdtemp.karma[m] = participle.karma[k]
               krdtemp.it[m] = participle.it[k]
               krdtemp.krdanta[m] = participle.krdanta[k]
               krdtemp.pratipadika[m] = participle.pratipadika[k]
               krdtemp.dhatu[m] = participle.dhatu[k]
               krdtemp.nijdhatu[m] = participle.nijdhatu[k]
               krdtemp.sandhatu[m] = participle.sandhatu[k]
               krdtemp.artha[m] = participle.artha[k]
               krdtemp.erb[m] = participle.erb[k]
               m += 1
    krdtemp.numofKrdantas = m
    return krdtemp
def syntacticCheck(adj: subanta_data, pro: subanta_data, krdav: krdav_data, indeclinable: avyaya_data, verb: VERB, subject: VIBHAKTI, object: VIBHAKTI, locative: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI, vocative: VIBHAKTI,
                   genitive: VIBHAKTI, krdtemp: krdanta_data, verbs: tiganta_data, numofVerbs: int, counter: int, dvithiya: str, karmaFlag: bool, word: str) -> (int, List[str]):

    result, qflag = [], 0
    avyayaFlag = checkforAvyaya(indeclinable)
    errorflag = {'subject':subject != None and subject.numofWords > 1 and avyayaFlag > 0 and not checkPosofAvyaya(indeclinable, subject, avyayaFlag),
                  'object':subject != None and object.numofWords > 1 and avyayaFlag > 0 and not checkPosofAvyaya(indeclinable, object, avyayaFlag),
                  'genitive':subject != None and genitive.numofWords > 1 and avyayaFlag > 0 and not checkPosofAvyaya(indeclinable, genitive, avyayaFlag),
                  'dative':subject != None and dative.numofWords > 1 and avyayaFlag > 0 and not checkPosofAvyaya(indeclinable, dative, avyayaFlag),
                 'ablative':subject != None and ablative.numofWords > 1 and avyayaFlag > 0 and not checkPosofAvyaya(indeclinable, ablative, avyayaFlag),
                  'instrument':subject != None and instrument.numofWords > 1 and avyayaFlag > 0 and not checkPosofAvyaya(indeclinable, instrument, avyayaFlag),
                  'locative':subject != None and locative.numofWords > 1 and avyayaFlag > 0 and not checkPosofAvyaya(indeclinable, locative, avyayaFlag)
                  # 'vocative':vocative.numofWords > 1 and avyayaFlag > 0 and checkPosofAvyaya(indeclinable, vocative, avyayaFlag),
                      }
    # if (verb.prayoga == karmani or karmaFlag == 0) and counter != (ord('a') - 1): result.append('%s%s'%(rec.sentence.split('(')[1][0], counter))
    voice = 'ACTIVE VOICE' if verb.prayoga == karthari else 'PASSIVE VOICE'
    result.append('The sentence is in ' + voice); result.append('')
    if karmaFlag == 0 and object.numofWords > 0:
        voice = 'Considering the verb as ' + ['Sakarmaka(transitive)','Akarmaka(intransitive)'][verb.karma-1]
    else: voice = 'Verb is ' + ['Sakarmaka(transitive)','Akarmaka(intransitive)'][verb.karma-1]
    result.append(voice)
    num = False
    # for cla in [subject, object, ablative, instrument, locative, dative]: num = num or (cla != None and cla.numofWords > 1)
    # num = subject.numofWords > 1 or object.numofWords > 1 or ablative.numofWords > 1 or instrument.numofWords > 1 or locative.numofWords > 1 or dative.numofWords > 1
    num = ft.reduce(lambda x, y: x and y.numofWords > 1,[subject, object, ablative, instrument, locative, dative])
    if numofVerbs == 1:
        if avyayaFlag > 0 and not num:
            result.append(displaytheInformation(subject, object, instrument, dative, ablative, locative, vocative, genitive, indeclinable, krdav, adj, pro, krdtemp, verb.prayoga, krdtemp))
            result.append('Verb(s) are' + ', '.join(verb.tiganta[:verb.numOfVerbs])[1:])
            result.append('There is ' + ', '.join(indeclinable.avyava[:indeclinable.numofAvyayas])[1:] + ' present in the sentence, but there are 2 or more words with the same charateristics.')
            result.append('The sentence is syntactically not compatible')
        else: result.append(compatibilityCheck1(krdav, verb, krdtemp, subject, object, instrument, dative, ablative, locative, vocative,  genitive, indeclinable, avyayaFlag,
                                  errorflag, dvithiya, adj, pro, word))
    else:
        qflag = 0
        result.append(displaytheInformation(subject, object, instrument, dative, ablative, locative, vocative, genitive, indeclinable, krdav, adj, pro, krdtemp, 2))
        fmted = [tupl for tupl in zip(verbs.tiganta[:verbs.numofVerbs], verbs.dhatu[:verbs.numofVerbs], verbs.purusha[:verbs.numofVerbs],
                                      verbs.vacana[:verbs.numofVerbs])]
        # fmted = str.format('%s %s %s %s %s'%(fmted))
        res = ''
        for tupl in fmted:
            tiganta, dhatu, purusha, vacana = tupl
            purusha, vacana = dsp.Person[purusha], dsp.Vacana[vacana]
            res += '%s ( %s / %s / %s )\n'%(tiganta, dhatu, purusha, vacana)
        result.append('Verb(s) are : ' + res[:-1])
        flagp = getPurushaofAllVerbs(verbs)
        flagv = getVacanaofAllVerbs(verbs)
        if avyayaFlag:
            aflag = checkPosofAvyayaBetweenVerbs(indeclinable, verb, avyayaFlag)
            if aflag:
                if flagp:
                    if flagv: result.append('The verbs do not agree in purusha and vacana')
                    else: result.append('The verbs agree in vacana but not in pursuha')
                else:
                    if flagv: result.append('The verbs agree in purusha but not in vacana')
                    else:
                        qflag = 2
                        result.append('The verbs agree in purusha and Vacana')
            else:
                result.append('There is more than one verb present in the sentence and' + ', '.join(indeclinable.avyava[:indeclinable.numofAvyayas])[1:] +
                              ' is not in the correct place.\nThe sentence is syntactically not compatible.')
        else:
            if flagp:
                if flagv: result.append('The verbs do not agree in purusha and vacana')
                else: result.append('The verbs agree in vacana but not in pursuha')
            else:
                if flagv: result.append('The verbs do not agree in purusha and vacana')
                else: result.append('There is more than one verb present in the sentence and there is no ¸ or ÔÚ present in the sentence.\nThe sentence is syntactically not compatible.')
        result.append('---------------')
    return qflag, result
def syntacticCheck1(adj: subanta_data, pro: subanta_data, krdav: krdav_data, indeclinable: avyaya_data, krdanta: PARTICIPLE, subject: VIBHAKTI, object: VIBHAKTI, locative: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI, vocative: VIBHAKTI,
                    genitive: VIBHAKTI, participle: krdanta_data, numofKrdantas: int, counter: int, dvithiya: str, karmaFlag: bool, saflag: bool) -> (int, List[str]):

    result = []
    avyayaFlag = checkforAvyaya(indeclinable)
    # if (krdanta.prayoga == karmani or karmaFlag == 0) and counter != (ord('a') - 1): result.append('%s%s'%(rec.sentence.split('(')[1][0], counter))
    if krdanta.krdType == 4:
        if saflag: result.append('The basic root of the krdanta is in both akarmaka/sakarmaka\nHence the sentence is in both active/passive voice')
        elif krdanta.karma == 1: result.append('The basic root of the krdanta is sakarmaka\nThe sentence is in both active/passive voice')
        else: result.append('The basic root of the krdanta is akarmaka')
    voice = 'ACTIVE' if krdanta.prayoga == karthari else 'PASSIVE'
    result.append('The sentence is in ' + voice + ' VOICE'); result.append('')
    if karmaFlag and object.numofWords == 0:
        result.append(['Considering krdanta as  SAKARMAKA (transitive)', 'Considering krdanta as  AKARMAKA (intransitive)'][krdanta.karma - 1])
    qflag = False
    clasName = ['Subject(s):', 'Object(s):', 'Instrument(s):', 'Dative(s):', 'Ablative(s):', 'Genitive(s):', 'Locative(s):', 'Vocative(s):']
    errorflag = {'subject':subject.numofWords > 1 and avyayaFlag and checkPosofAvyaya(indeclinable, subject, avyayaFlag),
                      'object':object.numofWords > 1 and avyayaFlag and checkPosofAvyaya(indeclinable, object, avyayaFlag),
                      'genitive':genitive.numofWords > 1 and avyayaFlag and checkPosofAvyaya(indeclinable, genitive, avyayaFlag),
                      'ablative':ablative.numofWords > 1 and avyayaFlag and checkPosofAvyaya(indeclinable, ablative, avyayaFlag),
                      'instrument':instrument.numofWords > 1 and avyayaFlag and checkPosofAvyaya(indeclinable, instrument, avyayaFlag),
                      'locative':locative.numofWords > 1 and avyayaFlag and checkPosofAvyaya(indeclinable, locative, avyayaFlag),
                      # 'vocative':vocative.numofWords > 1 and avyayaFlag and checkPosofAvyaya(indeclinable, vocative, avyayaFlag),
                      'dative':dative.numofWords > 1 and avyayaFlag and checkPosofAvyaya(indeclinable, dative, avyayaFlag)}
    flag = {'p':False, 'v':False, 'l':False, 't':False}
    num = ft.reduce(lambda x, y: x and y.numofWords > 1, [subject, object, genitive, ablative, instrument, locative, dative])
    avyayaflag = not ((not any(errorflag)) and krdav.numofKrdavyayas == 0 and avyayaFlag)
    flag['t'] = checkPosandTypeofAllKrdantas(participle)
    adjflag, proflag = False, False
    if adj != None and adj.numofNouns > 0:
        adjflag = checkAdjProVibhaktiCompatibility(adj, subject, object, instrument, dative, ablative, locative, vocative, genitive, True)
    if pro != None and pro.numofNouns > 0:
        proflag = checkAdjProVibhaktiCompatibility(pro, subject, object, instrument, dative, ablative, locative, vocative, genitive, True)
    if numofKrdantas == 1:
        if avyayaFlag and num:
            result.append(displaytheInformation1(subject, object, instrument,  dative, ablative, locative, vocative, genitive, indeclinable, krdav, adj, pro, krdanta.prayoga))
            res = ''
            for i in range(numofKrdantas): res += participle.krdanta[i]
            result.append('Krdanta(s) are:' + res)
            result.append('There is ')
            for i in range(indeclinable.numofAvyayas): result.append('%s present in the sentence, but there are no 2 or more words with same charcteristics\n The sentence is syntactically not compatible'%indeclinable.avyaya[i])
        else:
            qflag, res = compatibilityCheck2(participle, krdanta, subject, object, instrument, dative, ablative, locative, vocative,  genitive, indeclinable, avyayaflag, errorflag, dvithiya, krdav, adj, pro)
            result.append(res)
    elif numofKrdantas == 2:
        qflag = True
        result.append(displaytheInformation1(subject, object, instrument, dative, ablative, locative, vocative, genitive,indeclinable, krdav, adj, pro, krdanta.prayoga))
        for i in range(participle.numofKrdantas):
            result.append(clasName[participle.vibhakti[i] - 1])
            result.append('%s %s / %s / %s'%(participle.krdanta[i], data1.Linga(participle.linga[i]), data1.Case(participle.vibhakti[i]), data1.Vacana(participle.vacana[i])))
        if not flag['t'] and participle.krdType[1] in [4,5] and adjflag and proflag:
            if participle.prayoga[1] == 0:
                if subject.numofWords == 0: result.append('Any subanta in %s, %s \nand in %s can be the %s\n%s'%(data1.Case[0], data1.Vacana[krdanta.vacana-1],data1.Linga[krdanta.linga], 'subject', dsp.mesgn))
                elif subject.numofWords == 1:
                    flag['p'] = subject.vibhakti[0] == participle.vibhakti[1] and subject.vacana[0] == participle.vacana[1] and subject.linga[0] == participle.linga[1]
                    if flag['p']:result.append('%s %s'%('subject', dsp.mesgV1))
                    else: result.append('The krdanta does not agree with subject\nThe sentence is syntactically not compatible')
                else:
                    result.append('There is more than one %s in the sentence and '%'subject')
                    if avyayaflag:
                        for i in range(indeclinable.numofAvyayas): result.append('%s '%indeclinable.avyava[i])
                        result.append('in the sentence is not in the correct place')
                    else: result.append("there is no '¸ ' or 'ÔÚ' in the sentence.")
            else:
                if object.numofWords == 0: result.append('Any subanta in %s, %s \nand in %s can be the %s\n%s'%(data1.Case[0], data1.Vacana[krdanta.vacana-1],data1.Linga[krdanta.linga], 'subject', dsp.mesgn))
                elif object.numofWords == 1:
                    flag['p'] = object.vibhakti[0] == participle.vibhakti[1] and object.vacana[0] == participle.vacana[1] and object.linga[0] == participle.linga[1]
                    if flag['p']:result.append('%s %s'%('object', dsp.mesgV1))
                    else: result.append('The krdanta does not agree with object\nThe sentence is syntactically not compatible')
                else:
                    result.append('There is more than one %s in the sentence and '%'object')
                    if avyayaflag:
                        for i in range(indeclinable.numofAvyayas): result.append('%s '%indeclinable.avyava[i])
                        result.append('in the sentence is not in the correct place')
                    else: result.append("there is no '¸ ' or 'ÔÚ' in the sentence.")
        else: result.append('There is no verb. The sentence is syntactically not compatible')
    else:
        qflag = True
        result.append(displaytheInformation1(subject, object, instrument, dative, ablative, locative, vocative,genitive, indeclinable, krdav, adj, pro, 2))

        for i in range(participle.numofKrdantas):
            res = ['Subject(s):', 'Object(s):', 'Instrument(s):', 'Dative(s):', 'Ablative(s):', 'Genitive(s):', 'Locative(s):', 'Vocative(s):'][participle.vibhakti[i] - 1] + \
                  '%s %s / %s / %s' % (participle.krdanta[i], data1.Linga(participle.linga[i]), data1.Case(participle.vibhakti[i]), data1.Vacana(participle.vacana[i]))
            result.append(res)
        k, prayoga = None, 0
        for j in range(participle.numofKrdantas):
            if participle.krdType in [4,5]:
                k, prayoga = j, participle.prayoga[j]
                break
        if not flag['t'] and k != None and adjflag and proflag:
            if prayoga == 0:
                if subject.numofWords == 0:
                    result.append('Any subanta in %s, %s \nand in %s can be the %s\n%s'%(data1.Case[0], data1.Vacana[krdanta.vacana-1],data1.Linga[krdanta.linga], 'subject', dsp.mesgn))
                    for j in range(subject.numofWords):
                        flag['p'] = subject.vibhakti[j] == participle.vibhakti[k] and subject.vacana[j] == participle.vacana[k] and subject.linga[j] == participle.linga[k]
                        if flag['p']: result.append('%s %s' % ('subject', dsp.mesgV1))
                        else: result.append('The krdanta does not agree with subject\nThe sentence is syntactically not compatible')
            else:
                if object.numofWords == 0: result.append('Any subanta in %s, %s \nand in %s can be the %s\n%s'%(data1.Case[0], data1.Vacana[krdanta.vacana-1],data1.Linga[krdanta.linga], 'subject', dsp.mesgn))
                else:
                    for j in range(object.numofWords):
                        flag['p'] = object.vibhakti[j] == participle.vibhakti[k] and object.vacana[j] == participle.vacana[k] and object.linga[j] == participle.linga[k]
                    if flag['p']: result.append('%s %s' % ('object', dsp.mesgV1))
                    else: result.append('The krdanta does not agree with object\nThe sentence is syntactically not compatible')
        else: result.append('There is no verb. The sentence is syntactically not compatible')
    return qflag, result
def checkforAvyaya(indeclinable: avyaya_data) -> int:
    if indeclinable == None: return 0
    for i in range(indeclinable.numofAvyayas):
       result = {'.':1, '¤ÈÛ':1, 'ÔÚ':5, '¤ÃÔÚ':3, '¨Â':3, '¥Øå×èÔÛÂè':3}.get(indeclinable.avyava[i], 0)
    return result
def checkPosofAvyaya(indeclinable: avyaya_data, vibhakti: VIBHAKTI, avyayaFlag: int) -> int:
    if indeclinable == None or vibhakti == None: return 0
    for i in range(indeclinable.numofAvyayas):
        aflag = 0
        if avyayaFlag in [1, 5]:
            for j, vibh in enumerate(vibhakti.numofWords - 1):
                vflag = False
                if vibhakti[j] + 1 == vibhakti[j + 1]: vflag = True
            if vflag:
                if vibhakti.wordPos[vibhakti.numofWords - 1] == indeclinable[indeclinable.wordNum[i]]:
                    aflag = avyayaFlag
        else:
            for j, wordpos in enumerate(vibhakti.wordPos[:vibhakti.numofWords]):
                aflag = 0
                if vibhakti.wordPos[j] + 2 == vibhakti.wordPos[j + 1] and vibhakti.wordPos[j] + 1 == indeclinable[indeclinable.wordNum[i]]:
                    aflag = avyayaFlag
    return aflag
def displaytheInformation(subject: VIBHAKTI, object: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI, locative: VIBHAKTI, vocative: VIBHAKTI, genitive: VIBHAKTI, indeclinable: avyaya_data, krdav: krdav_data,
                          adj: subanta_data, pro: subanta_data,  krdtemp: krdanta_data, prayoga: int) -> List[str]:
    result = []
    some_part_of_speech = 0
    for clas in [subject, object, instrument, dative, ablative, genitive, locative, vocative]:
        if clas != None: some_part_of_speech += clas.numofWords
    if some_part_of_speech > 0:
        result.append('Noun(s)')
        classes = ['Subject(s)', 'Object(s)', 'Instrument(s)', 'Dative(s)', 'Ablative(s)', 'Genitive(s)', 'Locative(s)'] #, 'Vocative(s)']
        for cl, clas in enumerate([subject, object, instrument, dative, ablative, genitive, locative]): #, vocative]):
            if clas != None and clas.numofWords > 0:
                res = classes[cl] + ' '
                for i in range(clas.numofWords): res += ': %s  (  %s / %s /  %s )'%(clas.word[i], data1.Linga[clas.linga[i]], data1.Case[clas.vibhakti[i] - 1], data1.Vacana[clas.vacana[i] - 1])
                result.append(res)
        if vocative != None:
            clas = vocative
            if clas.numofWords > 0:
                res = 'Vocative(s) '
                for i in range(clas.numofWords): res += 'Øá :%s  (  %s / %s /  %s )' % (clas.word[i], data1.Linga[clas.linga[i]], data1.Case[clas.vibhakti[i] - 1], data1.Vacana[clas.vacana[i] - 1])
                result.append(res)
    else: return result
    for adjpro in [adj, pro]:
        if adjpro != None:
            if adjpro.numofNouns > 0:
                classes = [['Subject(s)', 'Object(s)'], ['Object(s)' 'Object(s)'], ['Instrument(s)', 'Subject(s)'],  ['Dative(s)', 'Dative(s)'],
                           ['Ablative(s)', 'Ablative(s)'], ['Genitive(s)', 'Genitive(s)'], ['Locative(s)', 'Locative(s)'], ['Vocative(s)', 'Vocative(s)']]
                result.append(classes[adjpro.vibhakti - 1].get([0, 2].index(prayoga), ': '))
                for i, ad in enumerate(adjpro[:adjpro.numofNouns][1:]):
                    result.append('%s %s %s %s' % (adjpro.subanta[i], data1.Linga[adjpro.linga[i]], data1.Case[adjpro.vibhakti[i]], data1.Vacana[adjpro.vacana[i]]))
    if krdtemp.numofKrdantas > 0:
        result.append('Krdanta(s)')
        role = classes[krdtemp.vibhakti[0] - 1] + ' : '
        res = [role, 'Object(s) : ', role][prayoga] if prayoga < 2 else ''
        result.append('%s  %s ( %s / %s / %s )'%(res, krdtemp.krdanta[0], data1.Linga[krdtemp.linga[0]], data1.Case[krdtemp.vibhakti[0]], data1.Vacana[krdtemp.vacana[0]]))
        for i in range(1, krdtemp.numofKrdantas):
            result.append(' %s' %krdtemp.krdanta[i])
    if indeclinable != None and indeclinable.numofAvyayas > 0:
        result.append('Avyaya(s):')
        for i in range(indeclinable.numofAvyayas):
            result.append('%s'%indeclinable.avyava[i])
    if krdav != None and krdav.numofKrdavyayas > 0:
        res = ''
        for i in range(krdav.numofKrdavyayas):
         res += '%s %s %s '%(krdav.krdavyaya[i], krdav.dhatu[i], data1.Krudavyaya[krdav.krdavType[i]-1])
         result.append('Krdavyaya(s):' + res)
    return result
def displaytheInformation1(subject: VIBHAKTI, object: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI,locative: VIBHAKTI, vocative: VIBHAKTI, genitive: VIBHAKTI, indeclinable: avyaya_data, krdav: krdav_data,
                          adj: subanta_data, pro: subanta_data,  prayoga: int) -> List[str]:
    result = []
    if sum([subject.numofWords, object.numofWords, instrument.numofWords, dative.numofWords, ablative.numofWords, genitive.numofWords,
        locative.numofWords, vocative.numofWords]) > 0:
        result.append('Noun(s)')
        classes = ['Subject(s)', 'Object(s)', 'Instrument(s)', 'Dative(s)', 'Ablative(s)', 'Genitive(s)', 'Locative(s)'] #, 'Vocative(s)']
        for cl, clas in enumerate([subject, object, instrument, dative, ablative, genitive, locative]): #, vocative]):
            if clas.numofWords > 0:
                res = classes[cl] + ' '
                for i in range(clas.numofWords): res += ': %s  (  %s / %s /  %s )'%(clas.word[i], data1.Linga[clas.linga[i]], data1.Case[clas.vibhakti[i] - 1], data1.Vacana[clas.vacana[i] - 1])
                result.append(res)
        clas = vocative
        if clas.numofWords > 0:
            res = 'Vocative(s) '
            for i in range(clas.numofWords): res += 'Øá :%s  (  %s / %s /  %s )' % (clas.word[i], data1.Linga[clas.linga[i]], data1.Case[clas.vibhakti[i] - 1], data1.Vacana[clas.vacana[i] - 1])
            result.append(res)
    for adjpro in [adj, pro]:
        if adjpro != None and adjpro.numofNouns > 0:
            classes = [['Subject(s)', 'Object(s)'], ['Object(s)' 'Object(s)'], ['Instrument(s)', 'Subject(s)'],  ['Dative(s)', 'Dative(s)'],
                       ['Ablative(s)', 'Ablative(s)'], ['Genitive(s)', 'Genitive(s)'], ['Locative(s)', 'Locative(s)'], ['Vocative(s)', 'Vocative(s)']]
            result.append(classes[adjpro.vibhakti - 1].get([0, 2].index(prayoga), ': '))
            for i, ad in enumerate(adjpro[:adjpro.numofNouns][1:]):
                result.append('%s %s %s %s' % (adjpro.subanta[i], data1.Linga[adjpro.linga[i]], data1.Case[adjpro.vibhakti[i]], data1.Vacana[adjpro.vacana[i]]))
    if indeclinable != None and indeclinable.numofAvyayas > 0:
        result.append('Avyaya(s):')
        for i in range(indeclinable.numofAvyayas):
            result.append('%s'%indeclinable.avyava[i])
    if krdav != None and krdav.numofKrdavyayas > 0:
        res = ''
        for i in range(krdav.numofKrdavyayas):
         res += '%s %s %s '%(krdav.krdavyaya[i], krdav.dhatu[i], data1.Krudavyaya[krdav.krdavType[i]-1])
        result.append('Krdavyaya(s):' + res)
    return result
def compatibilityCheck1(krdav: krdav_data, verb: VERB, krdtemp: krdanta_data, subject: VIBHAKTI, object: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI, locative: VIBHAKTI, vocative: VIBHAKTI, genitive: VIBHAKTI, indeclinable: avyaya_data,
                        avyayaFlag: bool, errorflag: dict, dvithiya: str, adj: subanta_data, pro: subanta_data, word: typeWord) -> List[str]:
    def SubjectOrObject(flag, clas, clasName, proFlag, adjFlag, adj, pro):
        mesg_adj = dsp.mesga2 if adj != None and adj.numofNouns == 1 else dsp.mesga2a   #][[1].get(adj.numofNouns, 1)]
        mesg_pro = dsp.mesgp2 if pro != None and pro.numofNouns == 1 else dsp.mesgp2a  #][[1].get(pro.numofNouns, 1)]
        if flag['karma'] != 2: mesg_krd = dsp.mesgk2 if krdtemp.numofKrdantas == 1 else dsp.mesgk2a
        else: mesg_krd = dsp.mesgka1 if krdtemp.numofKrdantas == 1 else dsp.mesgka2
        flag['purusha'] = checkforPurushaCompatibility(verb, clas, pro, avyayaFlag)
        flag['vacana'] = checkforVacanaCompatibility(verb, clas, pro, avyayaFlag)
        mesgV = [[dsp.mesgV1, dsp.mesgV2], [dsp.mesgV3, dsp.mesgV4]][[True, False].index(flag['purusha'])][[True, False].index(flag['vacana'])]
        mesg_y_or_n = [dsp.mesgy, dsp.mesgn][[True, False].index(flag['purusha'] and flag['vacana'])]
        if flag['a'] and flag['karma']:
            if clas.numofWords > 0:
                if krdtemp.numofKrdantas > 0:
                    if pro != None and pro.numofNouns > 0:
                        if proFlag:
                            if adj != None and adj.numofNouns > 0:
                                if adjFlag:
                                    if flag['karma']: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesga1, dsp.mesgk1, dsp.mesgp1, mesg_y_or_n))
                                    else: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesga1, dsp.mesgp1, dsp.mesgn))
                                else:
                                    if flag['karma']: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesgk1, dsp.mesgp1, mesg_adj, dsp.mesgn))
                                    else: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesgp1, mesg_adj, mesg_krd, dsp.mesgn))
                            else:
                                if flag['karma']: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesgk1, dsp.mesgp1, mesg_y_or_n))
                                else: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesgp1, mesg_krd, dsp.mesgn))
                        else:
                            if adj != None and adj.numofNouns > 0:
                                if adjFlag:
                                    if flag['karma']: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesga1, dsp.mesgk1, mesg_pro, dsp.mesgn))
                                    else: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesga1, mesg_pro, mesg_krd, dsp.mesgn))
                                else:
                                    if flag['karma']: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesgk1, mesg_adj, mesg_pro, dsp.mesgn))
                                    else:result.append('The %s %s\n %s %s' % (clasName, mesgV, mesg_adj, mesg_pro, mesg_krd, dsp.mesgn))
                            else:
                                if flag['karma']: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesgk1, dsp.mesga1, mesg_pro, dsp.mesgn))
                                else: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesga1, mesg_pro, mesg_krd, dsp.mesgn))
                    else:
                        if adj != None and adj.numofNouns > 0:
                            if adjFlag:
                                if flag['karma']: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesga1, dsp.mesgk1, dsp.mesgp1, mesg_y_or_n))
                                else: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesga1, dsp.mesgp1, mesg_krd, dsp.mesgn))
                            else:
                                if flag['karma']: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesgk1, dsp.mesgp1, mesg_y_or_n))
                                else: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesgp1, mesg_krd, dsp.mesgn))
                        else:
                                if flag['karma']: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesgk1, dsp.mesgp1, mesg_y_or_n))
                                else: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesgp1, mesg_krd, dsp.mesgn))
                else:
                    if pro != None and pro.numofNouns > 0:
                        if proFlag:
                            if adj != None and adj.numofNouns > 0:
                                if adjFlag: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesga1, dsp.mesgp1, mesg_y_or_n))
                                else: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesgp1, mesg_adj, dsp.mesgn))
                            else: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesgp1, mesg_y_or_n))
                        else:
                            if adj != None and adj.numofNouns > 0:
                                if adjFlag: result.append('The %s %s\n %s %s' % (clasName, mesgV, dsp.mesga1, mesg_pro, dsp.mesgn))
                                else: result.append('The %s %s\n %s %s' % (clasName, mesgV, mesg_pro, mesg_adj, dsp.mesgn))
                            else: result.append('The %s %s\n %s %s' % (clasName, mesgV, mesg_pro, dsp.mesgn))
                    else:
                        if adj != None and adj.numofNouns > 0:
                            if adjFlag: result.append('\nThe %s %s\n %s %s' % (clasName, mesgV, dsp.mesga1, mesg_y_or_n))
                            else: result.append('\nThe %s %s\n %s %s' % (clasName, mesgV,mesg_adj, dsp.mesgn))
                        else: result.append('\nThe %s %s\n %s' % (clasName, mesgV, dsp.mesgy))
            else:
                if pro != None and pro.numofNouns > 0:
                    proFlag = checkPronounVerbCompatibility(verb, subject, object, instrument, dative, ablative, locative, genitive, vocative, pro)
                    if proFlag:
                        if adj != None and adj.numofNouns > 0:
                            if adjFlag:
                                if krdtemp.numofKrdantas > 0:
                                    if flag['karma']:
                                        if proFlag == 2: result.append(dispMesg6(verb.prayoga, verb.purusha, verb.vacana, clasName))
                                        else: result.append('The %s %s\n %s %s' % (dsp.mesgP1, dsp.mesga1, dsp.mesgk1, dsp.mesgy))
                                    else: result.append('The %s %s\n %s %s' % (dsp.mesgP1, dsp.mesga1, mesg_krd, dsp.mesgn))
                                else:
                                    if proFlag == 2: result.append(dispMesg6(verb.prayoga, verb.purusha, verb.vacana, clasName))
                                    else: result.append('The %s %s\n %s %s' % (dsp.mesgP1, dsp.mesga1, dsp.mesgn))
                            else:
                                if krdtemp.numofKrdantas > 0:
                                    if flag['karma']: result.append('The %s %s\n %s %s' % (dsp.mesgP1, dsp.mesgk1, mesg_adj, dsp.mesgn))
                                    else: result.append('The %s %s\n %s %s' % (dsp.mesgP1, mesg_krd, mesg_adj, dsp.mesgn))
                                else: result.append('The %s %s\n %s %s' % (dsp.mesgP1, mesg_adj, dsp.mesgn))
                        else:
                            if krdtemp.numofKrdantas > 0:
                                if flag['karma']: result.append('The %s %s\n %s %s' % (dsp.mesgP1, dsp.mesgk1, mesg_adj, dsp.mesgn))
                                else: result.append('The %s %s\n %s %s' % (dsp.mesgP1, mesg_krd, mesg_adj, dsp.mesgn))
                            else: result.append('The %s %s\n %s %s' % (dsp.mesgP1, mesg_adj, dsp.mesgn))
                    else: result.append('The %s %s\n %s %s' % (clasName, dsp.mesgP2, dsp.mesgn))
                else:
                    if adj != None and adj.numofNouns > 0:
                        if adjFlag:
                            if krdtemp.numofKrdantas > 0:
                                if flag['karma']: result.append(dispMesg6(verb.prayoga, verb.purusha, verb.vacana, clasName))
                                else: result.append('The %s %s\n %s %s' % (dsp.mesga1, mesg_krd, dsp.mesgn))
                            else:
                                if krdtemp.numofKrdantas > 0:
                                    if flag['karma']: result.append('The %s %s\n %s %s' % (dsp.mesgk1, mesg_adj, dsp.mesgn))
                                    else: result.append('The %s %s\n %s %s' % (mesg_adj, mesg_krd, dsp.mesgn))
                                else: result.append('The %s %s\n %s %s' % (mesg_adj, dsp.mesgn))
                        else:
                            if krdtemp.numofKrdantas > 0:
                                if flag['karma']: result.append(dispMesg6f(verb.prayoga, verb.purusha, verb.vacana, krdtemp))
                                else: result.append('The %s %s\n %s %s' % (mesg_krd, dsp.mesgn))
                            else:
                                if krdtemp.numofKrdantas > 0:
                                    if flag['karma']: result.append('The %s %s\n %s %s' % (dsp.mesgk1, mesg_adj, dsp.mesgn))
                                    else: result.append('The %s %s\n %s %s' % (mesg_adj, mesg_krd, dsp.mesgn))
                                else: result.append('The %s %s\n %s %s' % (mesg_adj, dsp.mesgn))
                    else:
                        if krdtemp.numofKrdantas > 0:
                            if flag['karma']:
                                res = dispMesg6f(verb.prayoga, verb.purusha, verb.vacana, clasName, krdtemp)
                                if res != []: result.append(res)
                            else: result.append('The %s %s\n %s %s' % (mesg_krd, dsp.mesgn))
                        else: result.append(dispMesg6(verb.prayoga, verb.purusha, verb.vacana, clasName))
        else:
            if not flag['karma']:
                if object.numofWords > 0:  # dispMesgKarma
                    if verb.karma != 2: result.append('The dhatu of kradavyaya is akarmaka')
                    else: result.append('The dhathu is akaramaka')
                    if object.numofWords == 1: result.append('There is an object in the sentence')
                    else: result.append('There are objects in the sentence')
                else:
                    if flag['a']: result.append(analyseAkarmakaWithoutObjects(clasName, flag['purusha'], flag['vacana'], flag['karma'], adjFlag, proFlag,
                              subject, object, instrument, dative, ablative, locative, genitive, vocative, pro, adj, verb))
                    else:
                        if VinaaSahaFlag > 0: result.append(['ÔÛÆÚ is not handled properly', '×Ø is not handled properly'][VinaaSahaFlag - 1])
                        else:
                            for clas, flag, str in zip(allVibhaktiRoles, errorflag.values(), allVibhaktiLiterals):
                                if clas.numofWords > 0 and flag: result.append('There is more than one %s in the sentence and ' % str)
                                if avyayaFlag:
                                    for j in indeclinable.numofAvyayas: result.append('%s ' % indeclinable.avyava[j])
                                    result.append('in the sentence is not in the correct place. %s' % dsp.mesgn)
                                else: result.append("there is no '¸ ' or 'ÔÚ' in the sentence.\ %s" % dsp.mesgn)
            else:
                if VinaaSahaFlag > 0:
                    result.append(['ÔÛÆÚ is not handled properly', '×Ø is not handled properly'][VinaaSahaFlag - 1])
                else:
                    for clas, flag, str in zip(allVibhaktiRoles, errorflag.values(), allVibhaktiLiterals):
                        if clas.numofWords > 0 and flag: result.append('There is more than one %s in the sentence and ' % str)
                        if avyayaFlag:
                            for j in indeclinable.numofAvyayas: result.append('%s ' % indeclinable.avyava[j])
                            result.append('in the sentence is not in the correct place. %s' % dsp.mesgn)
                        else: result.append("there is no '¸ ' or 'ÔÚ' in the sentence.\ %s" % dsp.mesgn)
    result = []
    allVibhaktiRoles, allVibhaktiLiterals = [subject, object, instrument, dative, ablative, genitive, locative, vocative], ['subject', 'object', 'instrument', 'dative', 'ablative', 'genitive', 'locative', 'vocative']
    flag = {'a': False, 'vacana': False, 'linga': False, 'purusha': False, 'karma': True, 'ak': False, 'ka': False, 'krdanta': 0, 'krdav': 0}
    # flag['karma'] = True
    if adj != None and adj.numofNouns > 0:
        adjFlag = checkAdjorProandVibhaktiCompatibility(adj, subject, object, instrument, dative, ablative, locative, vocative, genitive, True)
    else: adjFlag = False
    if pro != None and pro.numofNouns > 0:
        proFlag = checkAdjorProandVibhaktiCompatibility(adj, subject, object, instrument, dative, ablative, locative, vocative, genitive, False)
    else: proFlag = False
    lastWordPos = 0
    for n in range(word.numofWords):
        if word.word[n] == 'krdanta':
            if n > lastWordPos: lastWordPos = n
            flag['krdanta'] = checkforKrdantaCompatibility(krdtemp, subject, object, instrument, dative, ablative, genitive, locative, vocative, n, avyayaFlag)
        elif word.word[n] == 'krdav':
            if n > lastWordPos: lastWordPos = n
            flag['krdav'] = checkforKrdavyayaCompatibility(krdav, subject, object, instrument, dative, ablative, genitive, locative, vocative, n)
    # if avyayaFlag:
    excludeSubject =  {x: errorflag[x] for x in errorflag if x != 'subject'}
    if any(excludeSubject.values()):
        for literal, clas in zip(allVibhaktiLiterals, allVibhaktiRoles):
            if excludeSubject[literal]: flag['a'] = checkForKrdavayayaAndVibhaktiCompatibility(krdav, clas, indeclinable, avyayaFlag)
    elif errorflag['subject']:
        flag['a'] = flag['krdav'] and krdav.numofKrdavyayas > 0
    else: flag['a'] = True
    numofObjects = 0
    if verb.karma == 2:
        for i in range(object.numofWords):
            if object.wordPos[i] >= lastWordPos:
                numofObjects += 1
                flag['karma'] = False
    if flag['krdav'] == 2: flag['karma'] = False
    VinaaSahaFlag = False
    if flag['a']:
        VinaaSahaFlag = checkVinaaSahaCompatibility(indeclinable, adj, pro, object, instrument, ablative, krdtemp, verb.prayoga, False)
        if VinaaSahaFlag in [1,2]: flag['a'] = False
    result.append(displaytheInformation(subject, object, instrument, dative, ablative, locative, vocative, genitive, indeclinable, krdav, adj, pro, krdtemp, verb.prayoga))
    result.append('Verb : %s ( %s / %s / %s )'%(verb.verb, verb.dhatu, data1.Person[verb.purusha], data1.Vacana[verb.vacana]))
    clas = subject if verb.prayoga == karthari else object
    clasName = 'subject' if verb.prayoga == karthari else 'object'
    SubjectOrObject(flag, clas, clasName, proFlag, adjFlag, adj, pro)
    result.append('---------------')
    return result
def compatibilityCheck2(participle: krdanta_data, krdanta: PARTICIPLE, subject: VIBHAKTI, object: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI,
                        locative: VIBHAKTI, vocative: VIBHAKTI,  genitive: VIBHAKTI, indeclinable: avyaya_data, avyayaflag: bool, errorflag: dict, dvithiya: str, krdav: krdav_data, adj: subanta_data, pro: subanta_data) -> List[str]:
    def SubjectOrObject(flag, clas, clasName, proFlag, adjFlag, adj, pro):
        mesg_adj = dsp.mesga2 if adj != None and adj.numofNouns == 1 else dsp.mesga2a   #][[1].get(adj.numofNouns, 1)]
        mesg_pro = dsp.mesgp2 if pro != None and pro.numofNouns == 1 else dsp.mesgp2a  #][[1].get(pro.numofNouns, 1)]
        flag['case'] = checkForVibhaktiCompatibility(krdanta, clas)
        flag['vacana'] = checkForVacanaCompatibility(krdanta, clas, avyayaflag)
        flag['linga'] = checkForLingaCompatibility(krdanta, clas)
        mesgK15 = [[dsp.mesgK1, dsp.mesgK2], [dsp.mesgK3, dsp.mesgK5]][[True, False].index(flag['vacana'])][[True, False].index(flag['linga'])]
        mesgK48 = [[dsp.mesgK4, dsp.mesgK6], [dsp.mesgK7, dsp.mesgK8]][[True, False].index(flag['vacana'])][[True, False].index(flag['linga'])]
        mesgK = [mesgK15, mesgK48][[True, False].index(flag['case'])]
        mesg_y_or_n = [dsp.mesgy, dsp.mesgn][[True, False].index(flag['vacana'] and flag['linga'])]
        mesg_y_or_n = [mesg_y_or_n, dsp.mesgn][[True, False].index(flag['case'])]
        if flag['a'] and flag['karma']:
            if clas.numofWords > 0:
                if pro != None and pro.numofNouns > 0:
                    if proFlag:
                        if adj != None and adj.numofNouns > 0:
                            if adjFlag: result.append('The %s %s\n %s %s' % (clasName, mesgK, dsp.mesga1, dsp.mesgp1, mesg_y_or_n))
                            else: result.append('The %s %s\n %s %s' % (clasName, mesgK, dsp.mesgp1, mesg_adj, dsp.mesgn))
                        else: result.append('The %s %s\n %s %s' % (clasName, mesgK, dsp.mesgp1, mesg_y_or_n))
                    else:
                        if adj != None and adj.numofNouns > 0:
                            if adjFlag: result.append('The %s %s\n %s %s' % (clasName, mesgK, dsp.mesga1, mesg_pro, dsp.mesgn))
                            else: result.append('The %s %s\n %s %s' % (clasName, mesgK, mesg_pro, mesg_adj, dsp.mesgn))
                        else: result.append('The %s %s\n %s %s' % (clasName, mesgK, mesg_pro, dsp.mesgn))
                else:
                    if adj != None and adj.numofNouns > 0:
                        if adjFlag: result.append('The %s %s\n %s %s' % (clasName, mesgK, dsp.mesga1, mesg_y_or_n))
                        else: result.append('The %s %s\n %s %s' % (clasName, mesgK, mesg_adj, dsp.mesgn))
                    else: result.append('The %s %s\n %s' % (clasName, mesgK, mesg_y_or_n))
            else:
                if pro != None and pro.numofNouns > 0:
                    proFlag = checkPronounKrdantaCompatibility(subject, object, instrument, dative, ablative, genitive, locative, vocative, krdanta, pro)
                    if proFlag:
                        if adj != None and adj.numofNouns > 0:
                            if adjFlag: result.append('The %s %s\n %s %s' % (clasName, dsp.mesgP3, dsp.mesga1, mesg_y_or_n))
                            else: result.append('The %s %s\n %s %s' % (clasName, mesgK, dsp.mesgP3, mesg_adj, dsp.mesgn))
                        else: result.append('The %s %s\n %s %s' % (clasName, mesgK, dsp.mesgp1, mesg_y_or_n))
                    else: result.append('The %s %s\n %s %s' % (clasName, dsp.mesgP4, dsp.mesgn))
                else:
                    if adj != None and adj.numofNouns > 0:
                        if adjFlag: result.append(dispMesg9a(krdanta, clasName))
                        else: result.append('%s %s' % (mesg_adj, dsp.mesgn))
                    else: result.append(dispMesg9(krdanta, clasName))
        else:
            if not flag['karma']:
                if object.numofWords > 0:  # dispMesgKarma
                    if krdanta.karma != 2 and flag['karma']: result.append('The dhatu of kradavyaya is akarmaka')
                    else: result.append('The dhathu is akaramaka')
                    if object.numofWords == 1: result.append('There is an object in the sentence')
                    else: result.append('There are objects in the sentence')
                else:
                    if flag['a']:
                        result.append( analyseAkarmakaWithoutObjects1(clasName, flag['p'], flag['v'], flag['k'], adjFlag, proFlag,
                               subject, object, instrument, dative, ablative, locative, genitive, vocative, pro, adj, krdanta))
                    else:
                        if VinaaSahaFlag > 0:
                            result.append(['ÔÛÆÚ is not handled properly', '×Ø is not handled properly'][VinaaSahaFlag - 1])
                        else:
                            for clas, flag, str in zip(allVibhaktiRoles, errorflag.values(), allVibhaktiLiterals):
                                if clas.numofWords > 0 and flag: result.append('There is more than one %s in the sentence and ' % str)
                                if avyayaflag:
                                    for j in indeclinable.numofAvyayas: result.append('%s ' % indeclinable.avyava[j])
                                    result.append('in the sentence is not in the correct place. %s' % dsp.mesgn)
                                else: result.append("there is no '¸ ' or 'ÔÚ' in the sentence.\ %s" % dsp.mesgn)
            else:
                if flag['a']:
                    result.append(analyseAkarmakaWithoutObjects1(clasName, flag['p'], flag['v'], flag['k'], adjFlag, proFlag,
                                   subject, object, instrument, dative, ablative, locative, genitive, vocative, pro, adj, krdanta))
                else:
                    if VinaaSahaFlag > 0: result.append(['ÔÛÆÚ is not handled properly', '×Ø is not handled properly'][VinaaSahaFlag - 1])
                    else:
                        for clas, flag, str in zip(allVibhaktiRoles, errorflag.values(), allVibhaktiLiterals):
                            if clas.numofWords > 0 and flag: result.append('There is more than one %s in the sentence and ' % str)
                            if avyayaflag:
                                for j in indeclinable.numofAvyayas: result.append('%s ' % indeclinable.avyava[j])
                                result.append('in the sentence is not in the correct place. %s' % dsp.mesgn)
                            else: result.append("there is no '¸ ' or 'ÔÚ' in the sentence.\ %s" % dsp.mesgn)

    result = []
    allVibhaktiRoles, allVibhaktiLiterals = [subject, object, instrument, dative, ablative, genitive, locative, vocative], \
                                            ['subject', 'object', 'instrument', 'dative', 'ablative', 'genitive', 'locative', 'vocative']
    # if avyayaflag:
    flag = {'a':False, 'case':False, 'vacana':False, 'linga':False, 'karma':False}
    if any(errorflag.values()):
        for literal, clas in zip(allVibhaktiLiterals, allVibhaktiRoles):
            if errorflag[literal]: flag['a'] = checkForKrdavayayaAndVibhaktiCompatibility(krdav, clas, indeclinable, avyayaflag)
    else: flag['a'] = True
    flag['karma'] = True
    adjFlag, proFlag  = False, False
    if adj != None and adj.numofNouns:
        adjFlag = checkAdjorProandVibhaktiCompatibility(adj, subject, object, instrument, dative, ablative, locative, vocative, genitive, True)
    if pro != None and pro.numofNouns:
        proFlag = checkAdjorProandVibhaktiCompatibility(adj, subject, object, instrument, dative, ablative, locative, vocative, genitive, False)
    if krdanta.karma == 2: flag['karma'] = False
    elif krdav != None:
        for i in range(krdav.numofKrdavyayas):
            if krdav.karma[i] == 2:
                flag['karma'] = False
                break
    VinaaSahaFlag = False
    if flag['a']:
        VinaaSahaFlag = checkVinaaSahaCompatibility(indeclinable, adj, pro, object, instrument, ablative, participle, krdanta.prayoga, True)
        flag['a'] = False if VinaaSahaFlag else True
    result.append(displaytheInformation1(subject, object, instrument, dative, ablative, locative, vocative, genitive, indeclinable, krdav, adj, pro, krdanta.prayoga))
    result.append('Krdanta(s)  : %s ( %s / %s / %s )\n'%(krdanta.krdanta, data1.Linga[krdanta.linga], data1.Case[krdanta.vibhakti - 1], data1.Vacana[krdanta.vacana - 1]))
    clas = subject if krdanta.prayoga == karthari else object
    clasName = 'subject' if krdanta.prayoga == karthari else 'object'
    if krdanta.prayoga == karthari or (krdanta.prayoga == karmani and dvithiya == ''): SubjectOrObject(flag, clas, clasName, proFlag, adjFlag, adj, pro)
    if krdanta.prayoga == karmani and dvithiya != '':
        result.append('%s is found in accusitive case\n but there cannot be accusitive case in sentences with passive voice. the sentence is syntactically not compatible')
    result.append('---------------')
    return flag, result
def checkForKrdavayayaAndVibhaktiCompatibility(krdav: krdav_data, clas: VIBHAKTI, avyaya: avyaya_data, avyayaflag: bool) -> bool:
    flag = None
    for i in range(krdav.numofKrdavyayas):
        if clas.vibhakti[0] == 1:
            for j in range(clas.numofWords - 1):
                if clas.numofWords > 2: return avyayaflag
                elif clas.numofWords == 1: flag = clas.wordPos[0] == krdav.wordNum[i]
                else: flag = clas.wordPos[j + 1] == clas.wordPos[j] and clas.wordPos[j + 1] == krdav.wordNum[i]
        else:
            if avyayaflag:
                if clas.numofWords == 1: flag = clas.wordPos[0] + 1 == krdav.wordNum[i]
                else:
                    vib1, vib2 = 0, 0
                    for j in range(clas.numofWords):
                        if clas.wordPos[j] < krdav.wordNum[i]: vib1 += 1
                        if clas.wordPos[j] > krdav.wordNum[i]: vib2 += 1
                    flag = vib1 == 1 and vib2 == 1
            else:
                vib1, vib2, before, after = 0, 0, False, False
                for j in range(clas.numofWords):
                    if clas.wordPos[j] < krdav.wordNum[i]: vib1 += 1
                    if clas.wordPos[j] > krdav.wordNum[i]: vib2 += 1
                    if avyaya.wordNum[0] < krdav.wordNum[i]: before = True
                    if avyaya.wordNum[0] > krdav.wordNum[i]: after = True
                if before:
                    if vib1 == 1: return False
                    else:
                        if vib2 > 1: return False
                        for j in range(clas.numofWords - 1):
                            if clas.wordPos[j] + 1 ==   clas.wordPos[j + 1] and clas.wordPos[j + 1] == avyaya.wordNum[0]: flag = True
                elif after:
                    if vib2 == 1: return False
                    else:
                        if vib1 > 1: return False
                        for j in range(clas.numofWords - 1):
                            if clas.wordPos[j] + 1 ==   clas.wordPos[j + 1] and clas.wordPos[j + 1] == avyaya.wordNum[0]: flag = True
    return flag
def checkPosofAvyayaBetweenVerbs(indeclinable: avyaya_data, verb :tiganta_data, avyayaflag :int) -> int:
    for i in range(indeclinable.numofAvyayas):
        aflag = 0
        if avyayaflag in [1,5]:
            for j in range(verb.numofVerbs - 1):
                if verb.wordNum[j] + 1 == verb.wordNum[j + 1]: vflag = True
                break
            aflag = avyayaflag if vflag and verb.wordNum(verb.numofVerbs - 1) + 1 == indeclinable.wordNum[i] else False
        else:
            for j in range(verb.numofVerbs - 1):
                if verb.wordNum[j] + 2 == verb.wordNum[j + 1] and verb.wordNum[j] + 1 == indeclinable.wordNum[j]:
                    aflag = avyayaflag
                    break
    return aflag
def checkAdjProVibhaktiCompatibility(adj: subanta_data, subject: VIBHAKTI, object: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI, locative: VIBHAKTI, vocative: VIBHAKTI, genitive: VIBHAKTI, tflag: bool = False) -> int:
    flag = 2 if subject.numofWords == 0 and not tflag else [True, False].index(tflag)
    flags = {'s':False, 'o':False, 'i':False, 'd':False, 'a':False, 'g':False, 'l':False, 'v':False}
    for clas in [subject, object, instrument, dative, ablative, locative, vocative]:
        for y in range(clas.numofWords):
            for x in range(adj.numofNouns):
                flag = 0
                if subject.wordPos[y] == adj.wordNum[x] and clas.vibhakti[y] == adj.vibhakti[x] and clas.vacana[y] == adj.vacana[x] and clas.linga[y] == adj.linga[x]:
                    flag = 1
                    break
    return flag
def checkforKrdantaCompatibility(krdtemp:krdanta_data, subject: VIBHAKTI, object: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI, genitive: VIBHAKTI, locative: VIBHAKTI, vocative: VIBHAKTI, wordNum: int, avyayaFlag: bool = False) -> bool:
    def all_other_vibhaktis(clas) -> bool:
        def case3() -> bool: return krdtemp.linga[k] in [0, 1]
        def case4() -> bool: return krdtemp.linga[k] in [0, 2]
        def case5() -> bool: return krdtemp.linga[k] in [1, 2]
        def case6() -> bool: return krdtemp.linga[k] in [0, 1, 2]
        if clas.numofWords == 0: flag = True
        elif clas.numofWords == 1:
            if (krdtemp.wordNum[k] + 1 == clas.wordPos[0]) or (krdtemp.wordNum[k] - 1 == clas.wordPos[0]):
                if krdtemp.vacana[k] == clas.vacana[0]:
                    flag = krdtemp.linga[k] == clas.linga[0]
                    if not flag:
                        fun = [case3, case4, case5, case6][clas.linga[0] - 3]
                        flag = fun()
            else: flag = True
        else:
            for j in range(clas.numofWords):
                if krdtemp.wordNum[k] - 1 == clas.wordPos[j]: flag = False
                elif krdtemp.wordNum[k] + 1 == clas.wordPos[j]:
                    if krdtemp.vacana[k] == clas.vacana[j]:
                        flag = krdtemp.linga[k] == clas.linga[j]
                        if not flag:
                            fun = [case3, case4, case5, case6][clas.linga[j] - 3]
                            flag = fun()
                else: flag = True
        return flag
    def assign_prathama_vibhakti(clas) -> bool:
        def case3() -> bool: return krdtemp.linga[k] in [0, 1]
        def case4() -> bool: return krdtemp.linga[k] in [0, 2]
        def case5() -> bool: return krdtemp.linga[k] in [1, 2]
        def case6() -> bool: return krdtemp.linga[k] in [0, 1, 2]
        if not (subject.numofWords > 1 and avyayaFlag):
            for j in range(subject.numofWords):
                flag = krdtemp.vacana[k] == subject.vacana[j] or krdtemp.linga[k] == subject.linga[j]
                if not flag:
                    fun = [case3, case4, case5, case6][subject.linga[j] - 3]
                    flag = fun()
        else: flag = False
        return flag
    kflag, clas = False, [subject, object, instrument, dative, ablative, locative, vocative]
    for cl in clas: kflag = kflag or cl != None and cl.numofWords == 0
    if not kflag:
        for k, krd in enumerate(krdtemp[:krdtemp.numofKrdantas]):
            if krdtemp.wordNum[k] == wordNum:
                func = [assign_prathama_vibhakti, all_other_vibhaktis].get(krdtemp.vibhakti[k] - 1, 1)
                arg = [subject, object, instrument, dative, ablative, locative, vocative][krdtemp.vibhakti[k] - 1]
                kflag = func(arg)
    return kflag
def checkforKrdavyayaCompatibility(krdav:krdav_data, subject: VIBHAKTI, object: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI, genitive: VIBHAKTI, locative: VIBHAKTI, vocative: VIBHAKTI, wordnum: int) -> int:
    if subject.numofWords > 2: kflag = 0
    else:
        for k in range(krdav.numofKrdavyayas):
            if krdav.wordNum[k] == wordnum:
                if subject.numofWords == 1:
                    kflag = 1 if krdav.wordNum[k] - 1 == subject.wordPos[0] else kflag
                elif subject.numofWords == 2:
                    kflag = 2 if (krdav.wordNum[k] - 2 == subject.wordPos[0]) and (krdav.wordNum[k] - 1 == subject.wordPos[1]) else kflag
                for j in range(object.numofWords):
                    if krdav.wordNum[k] - 1 == object.wordPos[j]:
                        kflag = 2 if krdav.karma[k] == 2 else 1
                for clas in [instrument, dative, ablative, genitive, locative, vocative]:
                    if krdav.wordNum[k] - 1 == clas.wordPos[j]: kflag = 1
    return kflag
def checkVinaaSahaCompatibility(indeclinable: avyaya_data, adj: subanta_data, pro: subanta_data, object: VIBHAKTI, instrument: VIBHAKTI,  ablative: VIBHAKTI, krdtemp: krdanta_data, prayoga: bool, kflag: bool) -> int:
    flag = 0
    if indeclinable != None:
        for i in range(indeclinable.numofAvyayas):
            if indeclinable.avyava[i] == 'ÔÛÆÚ':
                flag = 1
                for j in range(object.numofWords):
                    if object.wordPos[j] == indeclinable.wordNum[i]:
                        flag = 0
                        break
                if prayoga == karthari:
                    for adj_or_pro in [adj, pro]:
                        for j in range(adj.numofNouns):
                            if adj_or_pro.vibhakti[j] == 2 and adj_or_pro.wordNum[j] + 1 == indeclinable.wordNum[i]:
                                flag = 0
                                break
                    for j in range(krdtemp.numofKrdantas):
                        if krdtemp.vibhakti[j] == 2 and krdtemp.wordNum[j] + 1 == indeclinable.wordNum[i]:
                            flag = 0
                            break
                for clas in [instrument, ablative]:
                    for j in range(clas.numofWords):
                        if clas.wordPos[j] + 1 == indeclinable.wordNum[i]:
                            flag = 0
                            break
                for adj_or_pro in [adj, pro]:
                    for j in range(adj.numofNouns):
                        if adj_or_pro.vibhakti[j] in [3, 5] and adj_or_pro.wordNum[j] + 1 == indeclinable.wordNum[i]:
                            flag = 0
                            break
                if kflag:
                    for j in range(krdtemp.numofKrdantas):
                        if krdtemp.vibhakti[j] in [3, 5] and krdtemp.wordNum[j] + 1 == indeclinable.wordNum[i]:
                            flag = 0
                            break
            elif indeclinable.avyava[i] == '×Ø':
                flag = 2
                for j in range(instrument.numofWords):
                    if instrument.wordPos[j] + 1 == indeclinable.wordNum[i]:
                        flag = 0
                        break
                for adj_or_pro in [adj, pro]:
                    for j in range(adj.numofNouns):
                        if adj_or_pro.vibhakti[j] == 3 and adj_or_pro.wordNum[j] + 1 == indeclinable.wordNum[i]:
                            flag = 0
                            break
                if kflag:
                    for j in range(krdtemp.numofKrdantas):
                        if krdtemp.vibhakti[j] in [3, 5] and krdtemp.wordNum[j] + 1 == indeclinable.wordNum[i]:
                            flag = 0
                            break
    return flag
def checkforPurushaCompatibility(verb: VERB, vibhakti: VIBHAKTI, pro: subanta_data, avyayaFlag: int) -> bool:
    if vibhakti.numofWords > 0:
        if avyayaFlag == 1 and vibhakti.numofWords >= 2: flagp = verb.purusha == getPurushaofAllVerbs(vibhakti)
        elif avyayaFlag in [3, 5] and vibhakti.numofWords >= 2:
            if verb.purusha == vibhakti.purusha[vibhakti.numofWords - 1]: flagp = True
            else:
                for j in range(vibhakti.numofWords):
                    if verb.purusha == vibhakti.purusha[j]:
                        flagp = True
                        break
        else:
            for j in range(vibhakti.numofWords):
                if verb.purusha != vibhakti.purusha[j]:
                    flagp = False
                    break
            flagp = True
    elif pro != None:
        for j in range(pro.numofNouns):
                if verb.purusha == pro.purusha[j]:
                    flagp = True
                    break
                else: flagp = False
    else: flagp = False
    return flagp
def checkforVacanaCompatibility(verb: VERB, vibhakti: VIBHAKTI, pro: subanta_data, avyayaFlag: int) -> bool:
    if vibhakti.numofWords > 0:
        vacanaAllWords = getVacanaofAllWords(vibhakti)
        if avyayaFlag == 1 and vibhakti.numofWords >= 2:
            if vacanaAllWords == 1:
                if vibhakti.numofWords == 2:
                    if verb.vacana in [1,2]: flagv = True
                else:
                    if verb.vacana == 3: flagv = True
            elif vacanaAllWords == 2:
                if verb.vacana in [1, 2]: flagv = True
            elif vacanaAllWords == 3:
                if verb.vacana == 3: flagv = True
            elif vacanaAllWords == 0:
                if verb.vacana == vibhakti.vacana[vibhakti.numofWords - 1]: flagv = True
            else: flagv = False
        elif avyayaFlag in [3, 5] and vibhakti.numofWords >= 2:
            if vacanaAllWords == 1:
                if verb.vacana == 1: flagv = True
            elif vacanaAllWords in  [2, 3]:
                if verb.vacana == 2: flagv = True
            else:
                flagv = False
        else:
            for j in range(vibhakti.numofWords):
                if verb.vacana == vibhakti.vacana[j]:
                    flagv = True
                    break
            flagv = True
    else:
        if pro != None:
            for j in range(pro.numofNouns):
                if verb.vacana == pro.vacana[j]:
                    flagv = True
                    break
        else: flagv = True
    return flagv
def analyseAkarmakaWithoutObjects(str :str, flagp: bool, flagv: bool, flagk: int, adjFlag: bool, proFlag:bool, subject: VIBHAKTI, object: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI, locative: VIBHAKTI, genitive: VIBHAKTI, vocative: VIBHAKTI, pro: subanta_data, adj: subanta_data, krdtemp: krdanta_data, verb: VERB) -> List[str]:
    result = []
    mesgV = [[dsp.mesgV1, dsp.mesgV2], [dsp.mesgV3, dsp.mesgV4]][[True, False].index(flagp)][[True, False].index(flagv)]
    mesg_y_or_n = [dsp.mesgy, dsp.mesgn][[True, False].index(flagp and flagv)]
    mesg_adj = [dsp.mesga2, dsp.mesga2a][[1].get(adj.numofNouns, 1)]
    mesg_pro = [dsp.mesgp2, dsp.mesgp2a][[1].get(pro.numofNouns, 1)]
    mesg_krd = [[dsp.mesgka1, dsp.mesgka2], [dsp.mesgk2, dsp.msgk2a]][[2].get(flagk, 1)][[1].get(krdtemp.numofKrdantas, 1)]
    if subject.numofWords > 0:
        if krdtemp.numofKrdantas > 0:
            if pro.numofNouns > 0:
                if proFlag:
                    if adj.numofNouns > 0:
                        if adjFlag:
                            if flagk == 1: result.append('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesga1, dsp.mesgk1, dsp.mesgp1, mesg_y_or_n))
                            else: result.append('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesga1, dsp.mesgp1, mesg_krd, dsp.mesgn))
                        else:
                            if flagk == 1: result.append('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesgk1, dsp.mesgp1, mesg_adj, dsp.mesgn))
                            else: result.append('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesgp1, mesg_adj, mesg_krd,dsp.mesgn))
                    else:
                        if flagk == 1: result.append('%s %s\n %s\n %s %s' % (str, mesgV, dsp.mesgk1, dsp.mesgp1, mesg_y_or_n))
                        else: result.append('%s %s\n %s %s\n %s %s' % (str, mesgV, dsp.mesgp1, mesg_krd, dsp.mesgn))
                else:
                    if adj.numofNouns > 0:
                        if adjFlag:
                            if flagk == 1: result.append('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesga1, dsp.mesgk1, mesg_pro,  mesg_y_or_n))
                            else: result.append('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesga1, mesg_pro, mesg_krd, dsp.mesgn))
                        else:
                            if flagk == 1: result.append('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesgk1, dsp.mesga1, dsp.mesgp1, dsp.mesgn))
                            else: result.append('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesga1, mesg_adj, mesg_krd, dsp.mesgn))
                    else:
                        if flagk == 1: result.append(str.format('%s %s\n %s\n %s %s' % (str, mesgV, dsp.mesgk1, mesg_adj, mesg_y_or_n)))
                        else: result.append(str.format('%s %s\n %s %s\n %s %s' % (str, mesgV, mesg_pro, mesg_krd, dsp.mesgn)))
            else:
                if adj.numofNouns > 0:
                    if adjFlag:
                        if flagk == 1: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesga1, dsp.mesgk1, mesg_y_or_n)))
                        else: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesga1, mesg_krd, dsp.mesgn)))
                    else:
                        if flagk == 1: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesgk1, mesg_adj, dsp.mesgn)))
                        else: result.append(str.format('%s %s\n %s %s\n %s %s' % (str, mesgV, dsp.mesg1, mesg_krd, dsp.mesgn)))
                else:
                    if flagk == 1: result.append(str.format('%s %s\n %s\n %s %s' % (str, mesgV, dsp.mesgk1, mesg_y_or_n)))
                    else: result.append(str.format('%s %s\n %s %s\n %s %s' % (str, mesgV, mesg_krd, dsp.mesgn)))
        else:
            if pro.numofNouns > 0:
                if proFlag:
                    if adj.numofNouns > 0:
                        if adjFlag: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesga1, dsp.mesgp1, mesg_y_or_n)))
                        else: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesgp1, mesg_adj, dsp.mesgn)))
                    else: result.append(str.format('%s %s\n %s\n %s %s' % (str, mesgV, dsp.mesgp1, mesg_y_or_n)))
                else:
                    if adj.numofNouns > 0:
                        if adjFlag: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesga1, mesg_pro, dsp.mesgn)))
                        else: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesga1, mesg_pro, mesg_adj, dsp.mesgn)))
                    else:
                        if flagk == 1: result.append(str.format('%s %s\n %s\n %s %s' % (str, mesgV, dsp.mesgk1, mesg_adj, mesg_y_or_n)))
                        else: result.append(str.format('%s %s\n %s %s\n %s %s' % (str, mesgV, mesg_pro, mesg_krd, dsp.mesgn)))
            else:
                if adj.numofNouns > 0:
                    if adjFlag: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesga1, mesg_y_or_n)))
                    else: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesga1, mesg_adj, dsp.mesgn)))
                else: result.append(str.format('%s %s\n %s\n %s %s' % (str, mesgV, mesg_y_or_n)))
    else:
        if pro.numofNouns > 0:
            proFlag = checkPronounVerbCompatibility(verb, subject, object, instrument, dative, ablative, locative, genitive, vocative, pro)
            if proFlag:
                if adj.numofNouns > 0:
                    if adjFlag:
                        if krdtemp.numofKrdantas > 0:
                            if flagk == 1:
                                if proFlag == 2: result.append(dispMesg6(verb.prayoga, verb.purusha, verb. vacana, str))
                                else: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesgy)))
                            else: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesgP1, dsp.mesga1, mesg_krd, dsp.mesgn)))
                        else:
                            if proFlag == 2: result.append(dispMesg6(verb.prayoga, verb.purusha, verb.vacana, str))
                            else: result.append(str.format('%s\n%s\n' % (str, dsp.mesgP1, dsp.mesgy)))
                    else: result.append(str.format('%s\n%s\n' % (str, dsp.mesgP1, dsp.mesgy)))
            else: result.append(str.format('%s\n%s\n' % (str, dsp.mesgP2, dsp.mesgy)))
        else:
            if adj.numofNouns > 0:
                if adjFlag:
                    if krdtemp.numofKrdantas > 0:
                        if flagk == 1: result.append(dispMesg6(verb.prayoga, verb.purusha, verb.vacana, str))
                        else: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgV, dsp.mesga1,
                            [[dsp.mesgk2, dsp.msgk2a], [dsp.mesgka1, dsp.mesgka2]][[2].get(flagk, 1)][[1].get(krdtemp.numofKrdantas, 1)], dsp.mesgn)))
                    else: result.append(dispMesg6(verb.prayoga, verb.purusha, verb.vacana, str))
                else:
                    if krdtemp.numofKrdantas > 0:
                        if flagk == 1: result.append(dispMesg6(verb.prayoga, verb.purusha, verb.vacana, str))
                        else: result.append(str.format('%s %s\n %s %s\n %s %s' % (mesg_krd, dsp.mesgn)))
                    else: result.append(dispMesg6(verb.prayoga, verb.purusha, verb.vacana, str))
            else:
                if krdtemp.numofKrdantas > 0:
                    if flagk == 1: result.append(dispMesg6(verb.prayoga, verb.purusha, verb.vacana, str))
                    else: result.append(str.format('%s %s\n %s %s\n %s %s' % (str, mesgV, dsp.mesga1, mesg_krd, dsp.mesgn)))
                else: result.append(result.append(str.format('%s %s\n %s %s\n %s %s' % (mesg_adj, dsp.mesgn))))
    return result
def analyseAkarmakaWithoutObjects1(str :str, flagc: bool, flagv: bool, flagl: bool, adjFlag: bool, proFlag:bool, subject: VIBHAKTI, object: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI, locative: VIBHAKTI, genitive: VIBHAKTI, vocative: VIBHAKTI, pro: subanta_data, adj: subanta_data, krdanta: PARTICIPLE) -> List[str]:
    result = []
    mesg_y_or_n = [dsp.mesgy, dsp.mesgn][[True, False].index(flagl and flagv)]
    mesg_adj = [dsp.mesga2, dsp.mesga2a][[1].get(adj.numofNouns, 1)]
    mesg_pro = [dsp.mesgp2, dsp.mesgp2a][[1].get(pro.numofNouns, 1)]
    mesgK1_5 = [[dsp.mesgK1, dsp.mesgK2],[dsp.mesgK3, dsp.mesgK5]][[True, False].index(flagv)][[True, False].index(flagl)]
    mesgK4_8 = [[dsp.mesgK4, dsp.mesgK6],[dsp.mesgK7, dsp.mesgK8]][[True, False].index(flagv)][[True, False].index(flagl)]
    mesgK = [mesgK1_5, mesgK4_8][[True, False].index(flagc)]
    if subject.numofWords > 0:
        if pro.numofNouns > 0:
            if proFlag:
                if adj.numofNouns > 0:
                    if adjFlag: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgK, dsp.mesga1, dsp.mesgp1, mesg_y_or_n)))
                    else: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgK, dsp.mesgp1, mesg_adj, dsp.mesgn)))
                else: result.append(str.format('%s %s\n %s\n %s %s' % (str, mesgK, dsp.mesgp1, mesg_y_or_n)))
            else:
                if adj.numofNouns > 0:
                    if adjFlag: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgK, mesg_pro, mesg_adj, dsp.mesgn)))
                    else: result.append(str.format('%s %s\n %s %s\n %s %s'%((str, mesgK, mesg_pro, dsp.mesga2, mesg_adj, dsp.mesgn))))
                else: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgK, mesg_pro, dsp.mesgn)))
        else:
            if adj.numofNouns > 0:
                if adjFlag: result.append(str.format('%s %s\n %s %s\n %s %s'%(str, mesgK, dsp.mesga1, mesg_pro, dsp.mesgn)))
                else:result.append(str.format('%s %s\n %s %s\n %s %s'%((str, mesgK, mesg_pro, dsp.mesga2, mesg_adj, dsp.mesgn))))
            else:
                if adjFlag: result.append(str.format('%s %s\n %s %s\n %s %s' % (str, mesgK, dsp.mesga1, mesg_pro, dsp.mesgn)))
                else:result.append(str.format('%s %s\n %s %s\n %s %s' % ((str, mesgK, mesg_pro, dsp.mesga2, mesg_adj, dsp.mesgn))))
    else:
        if pro.numofNouns > 0:
            if proFlag:
                if adj.numofNouns > 0:
                    if adjFlag: result.append(str.format('%s %s\n %s %s\n %s %s' % (str,  dsp.mesgP3, dsp.mesga1, mesg_y_or_n)))
                    else: result.append(str.format('%s %s\n %s %s\n %s %s' % (str, mesgK, dsp.mesgp1, mesg_adj, dsp.mesgn)))
                else: result.append(str.format('%s %s\n %s\n %s %s' % (dsp.mesgP3, mesg_adj, dsp.mesgn)))
            else: result.append(str.format('%s %s\n %s %s\n %s %s' % (dsp.mesga1P4, dsp.mesgn)))
        else:
            if adj.numofNouns > 0:
                if adjFlag: result.append(str.format('%s %s\n %s %s\n %s %s' % (str, mesgK, dsp.mesga1, mesg_pro, dsp.mesgn)))
                else: result.append(str.format('%s %s\n %s %s\n %s %s' % ((str, mesgK, mesg_pro, dsp.mesga2, mesg_adj, dsp.mesgn))))
            else:
                if adjFlag: result.append(str.format('%s %s\n %s %s\n %s %s' % (str, mesgK, dsp.mesga1, mesg_pro, dsp.mesgn)))
                else: result.append(str.format('%s %s\n %s %s\n %s %s' % ((str, mesgK, mesg_pro, dsp.mesga2, mesg_adj, dsp.mesgn))))
    return result
def checkPronounVerbCompatibility(Verb: VERB, subject: VIBHAKTI, object: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI, locative: VIBHAKTI, genitive: VIBHAKTI, vocative: VIBHAKTI, pro: subanta_data) -> bool:
    flag = 0
    if subject.numofWords == 0:
        for ii in range(pro.numofNouns - 1):
            if pro.vibhakti[ii] == 1:
                flag = 1 if pro.purusha[ii] == Verb.purusha[ii] and pro.vacana[ii] == Verb.vacana[ii] else 0
                if pro.vibhakti[ii] == pro.vibhakti[ii + 1]: return 0
        flag = 1 if pro.purusha[pro.numofNouns] == Verb.purusha[pro.numofNouns] and pro.vacana[pro.numofNouns] == Verb.vacana[pro.numofNouns] else 0
    else: flag = checkAdjorProandVibhaktiCompatibility(pro, subject, object, instrument, dative, ablative, locative, vocative, genitive, False)
    return flag
def checkAdjorProandVibhaktiCompatibility(adj: subanta_data, subject: VIBHAKTI, object: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI, locative: VIBHAKTI, vocative: VIBHAKTI, genitive: VIBHAKTI, tflag) -> bool:
    flag = 1 if tflag else 0
    if tflag and subject.numofWords > 0: flag = 2
    for clas in [subject, object, instrument, dative, ablative, locative, genitive, vocative]:
        for y in range(clas.numofWords):
            for x in range(adj.numofnouns):
                if clas.wordPos[x] == adj.wordNum[x] and clas.vibhakti[y] == adj.vibhakti[x] and clas.vacana[y] == adj.vacana[x] and clas.linga[y] == adj.linga[x]: flag = 1
    return flag
def dispMesg6(prayoga: bool, purusha: int, vacana: int, str: str) -> List[str]:
    # result = []
    # if prayoga:
    result = ['%s in %s and %s can be the %s\n%s'%(dsp.mesg, dsp.Vibhakti[0], data1.Vacana[vacana - 1], str, dsp.mesgy),
                   '\n%s can be assumed to be the %s\n%s' % (dsp.MPurusha[vacana - 1], str, dsp.mesgy),
                   '\n%s can be assumed to be the %s\n%s' % (dsp.UPurusha[vacana - 1], str, dsp.mesgy)
                  ][purusha - 1]
    return result
def dispMesg6f(prayoga: bool, purusha: int, vacana: int, str: str, krdtemp: krdanta_data) -> List[str]:
    result, flag = [], False
    for i in range(krdtemp.numofKrdantas):
        if krdtemp.vibhakti[i] == 1:
            if krdtemp.vacana == vacana:
                flag = True
                result.append(['%s in %s and %s can be the %s\n%s' % (dsp.mesg, data1.Vibhakti[0], data1.Vacana[krdtemp.vacana[i] - 1], data1.Linga[krdtemp.linga[i] - 1], str, dsp.mesgy),
                          '\n%s can be assumed to be the %s\n%s' % (data1.MPurusha[krdtemp.vacana[i] - 1], str, dsp.mesgy),
                          '\n%s can be assumed to be the %s\n%s' % (data1.UPurusha[krdtemp.vacana[i] - 1], str, dsp.mesgy)
                          ][purusha - 1])
            else: result.append(str.format('%s %s'%(dsp.mesg3, dsp.mesgn)))
    if not flag: result.append(dispMesg6(prayoga, purusha, vacana, str))
    return result
def dispMesg9(krdanta: PARTICIPLE, str: str) -> List[str]:
    result = []
    if krdanta.vibhakti == 1: result.append('Any subanta in %s, %s \nand in %s can be the %s\n'%(dsp.Vibhakti[0], dsp.Vacana[krdanta.vacana - 1], dsp.Linga[krdanta.linga - 1], str))
    else: result.append('No matching subject is available')
    result.append('%s %s'%(dsp.mesga1, dsp.mesgy))
    return result
def dispMesg9a(krdanta: PARTICIPLE, str: str):
    result = []
    if krdanta.vibhakti == 1: result.append('Any subanta in %s, %s \nand in %s can be the %s\n'%(dsp.Vibhakti[0], dsp.Vacana[krdanta.vacana - 1], dsp.Linga[krdanta.linga - 1]))
    result.append('%s %s'%(dsp.mesga1, dsp.mesgy))
    return result
def getPurushaofAllVerbs(verb: tiganta_data) -> bool:
    if verb != None:
        for i in range(verb.numofVerbs - 1):
            if verb.purusha[i] != verb.purusha[i + 1]: return True
    return False
def getVacanaofAllVerbs(verb: tiganta_data) -> bool:
    if verb != None:
        for i in range(verb.numofVerbs - 1):
            if verb.vacana[i] != verb.vacana[i + 1]: return True
    return False
def getVacanaofAllWords(clas: VIBHAKTI) -> int:
    allVacanas, vacanaofAllWords = True, 0
    for i in range(clas.numofWords - 1):
        if clas.vacana[i] == clas.vacana[i + 1]: vacanaofAllWords = clas.vacana[i]
        else:
            allVacanas = False
            break
    if not allVacanas: vacanaofAllWords = 3
    return vacanaofAllWords
# SYNDATA1.c
def checkPosandTypeofAllKrdantas(participle: krdanta_data) -> bool:
    if participle.numofKrdantas > 1:
        for i in range(participle.numofKrdantas):
            flag = not (participle.krdType[i - 1] == participle.krdType[i] and participle.wordNum[i - 1] == participle.wordNum[i] and participle.vibhakti[i - 1] == participle.vibhakti[i] \
                   and participle.vacana[i - 1] == participle.vacana[i] and participle.linga[i - 1] == participle.linga[i])
            if not flag: break
    else: flag = False
    return flag
def checkPronounKrdantaCompatibility(subject: VIBHAKTI, object: VIBHAKTI, instrument: VIBHAKTI, dative: VIBHAKTI, ablative: VIBHAKTI, genitive: VIBHAKTI, locative: VIBHAKTI, vocative: VIBHAKTI, krdanta: PARTICIPLE, pro: subanta_data) -> bool:
    flag = False
    if subject.numofWords == 0:
        for ii in range(pro.numofNouns):
            if pro.vibhakti == krdanta.vibhakti and pro.vacana == krdanta.vacana:
                if pro.linga == krdanta.linga:
                    flag = True;
                    break
                else:
                    flag = krdanta.linga in [[0,1], [0,2], [1,2], [0,1,2]][pro.linga - 3]
    else: flag = checkAdjorProandVibhaktiCompatibility(pro, subject, object, instrument, dative, ablative, locative, vocative, genitive, False)
    return flag
def checkPosofAvyayaBetweenKrdantas(indeclinable: avyaya_data, participle :krdanta_data, avyayaflag :int) -> int:
    for i in range(indeclinable.numofAvyayas):
        aflag = 0
        if avyayaflag in [1,5]:
            for j in range(participle.numofKrdantas - 1):
                if participle.wordNum[j] + 1 == participle.wordNum[j + 1]: vflag = True
                break
            aflag = avyayaflag if vflag and participle.wordNum(participle.numofKrdantas - 1) + 1 == indeclinable.wordNum[i] else False
        else:
            for j in range(participle.numofKrdantas - 1):
                if participle.wordNum[j] + 2 == participle.wordNum[j + 1] and participle.wordNum[j] + 1 == indeclinable.wordNum[j]:
                    aflag = avyayaflag
                    break
    return aflag
def getVibhaktiofAllKrdantas(participle: krdanta_data) -> bool:
    for i in range(participle.numofKrdantas - 1):
        if participle.vibhakti[i] != participle.vibhakti[i + 1]: return True
    return False
def getVacanaofAllKrdantas(participle: krdanta_data) -> bool:
    for i in range(participle.numofKrdantas - 1):
        if participle.vacana[i] != participle.vacana[i + 1]: return True
    return False
def getLingaofAllKrdantas(participle: krdanta_data) -> bool:
    for i in range(participle.numofKrdantas - 1):
        if participle.linga[i] != participle.linga[i + 1]: return True
    return False
def checkForVibhaktiCompatibility(krdanta: PARTICIPLE, clas: VIBHAKTI) -> bool:
    for i in range(clas.numofWords):
        flag = krdanta.vibhakti == clas.vibhakti[i]
        if not flag: return flag  # is it one of them matching krdanta or all of them matching krdanta???
    return True
def checkForVacanaCompatibility(krdanta: PARTICIPLE, clas: VIBHAKTI, avyayaflag: bool) -> bool:
    vacanaofAllWords = getVacanaofAllWords(clas)
    if avyayaflag == 1 and clas.numofWords > 1:
        if vacanaofAllWords == 1:
            if clas.numofWords == 2: flag = krdanta.vacana in [1,2]
            else: flag = krdanta.vacana in [1,3]
        elif vacanaofAllWords == 2: flag = krdanta.vacana in [2,3]
        elif vacanaofAllWords == 3: flag = krdanta.vacana == 3
    elif avyayaflag in [3, 5] and clas.numofWords > 1:
        if vacanaofAllWords == krdanta.vacana: return True
    else:
        for i in range(clas.numofWords):
            flag = krdanta.vibhakti == clas.vibhakti[i]
            if flag: return True  # is it one of them matching krdanta or all of them matching krdanta???
    return False
def checkForLingaCompatibility(krdanta: PARTICIPLE, clas: VIBHAKTI) -> bool:
    for i in range(clas.numofWords):
        flag = krdanta.linga == clas.linga[i]
        if not flag: return flag  # is it one of them matching krdanta or all of them matching krdanta???
    return True
def checkPosandTypeofAllKrdantas(participle: krdanta_data) -> bool:
    flag = False
    for i in range(participle.numofKrdantas-1):
        flag = not (participle.krdType[i + 1] == participle.krdType[i] and participle.wordNum[i + 1] == participle.wordNum[i] and participle.vibhakti[i + 1] == participle.vibhakti[i] and participle.vacana[i + 1] == participle.vacana[i] and participle.linga[i + 1] == participle.linga[i])
    return flag
def flatten(item, lst=[]) -> List:
    if isinstance(item, list):
        for item2 in item: flatten(item2, lst)
    else: lst.append(item)
    return lst
def write_out_aci(OSOut, outfile=None):
    # fos = open('../../SenAnal/OSout.aci', 'r')
    if isinstance(OSOut, str): # external file
        fos = open(OSOut, 'r')
        for line in fos:
            if line.split(' ')[0] == "ÔÚ³èÍÌè":
                rec = record()
                rec.sentence, sentend, i = line[:-1], False, 0
            elif line[0] == '-':
                sentend, rec.numofIdens = True, i
            else:
                rec.idens[i] = line
                i += 1
            if sentend:
                wOrd, tempout = generateTable(rec)
                # print('numOfWords %i'%len(wOrd))
                # for item in wOrd:
                #     print('numofIdens %i idens..'%item.numofIdens)
                #     for iden in item.iden[:item.numofIdens]: print(iden)
                # # print('len %i depth %i'%(len(tempout), listdepth(tempout, 0)))
        fos.close()
    else:  # in-memory list
        for line in OSOut:
            if line.split(' ')[0] == "ÔÚ³èÍÌè":
                rec = record()
                rec.sentence, sentend, i = line[:-1], False, 0
            elif line[0] == '-':
                sentend, rec.numofIdens = True, i
            else:
                rec.idens[i] = line + '\n'
                i += 1
            if sentend:
                wOrd, tempout = generateTable(rec)
    tempout, out = flatten(tempout, lst=[]), []
    for i in range(0,len(tempout),len(wOrd)):
        out += [[rec.sentence] + tempout[i:i + len(wOrd)] + ['----------']]
    if outfile != None: foutw = open(outfile, 'w')
    # tot, i, res1 = len(tempout) // 4, 0, []
    tot, i, res1 = len(out), 0, []
    for lst in out:
        i += 1
        if outfile != None: foutw.write('%s  (  %s/ %s )\n' % (lst[0], i, tot))
        res1.append('%s  (  %s/ %s )\n' % (lst[0], i, tot))
        for lin in lst[1:]:
            if outfile != None: foutw.write('%s\n' % lin)
            res1.append('%s\n' % lin)
    if outfile != None: foutw.close()
    return res1
def write_result_aci(out, resultfile=None):
    res = commoncode(out)
    result = flatten(res, lst=[])
    if resultfile != None:
        fresult = open(resultfile, 'w')
        for line in result: fresult.write('%s\n' % line)
        fresult.close
    return result
def write_result_aci_from_out_aci(outfile, resultfile):
    foutr = open(outfile, 'r')
    res = commoncode(foutr)
    foutr.close()
    result = flatten(res)
    fresult = open(resultfile, 'w')
    # fresult = open('../../result2.aci', 'w')
    for line in result: fresult.write('%s\n' % line)
    fresult.close
    return result
def commoncode(out):
    res = []
    for line in out:
        if line.split(' ')[0] == "ÔÚ³èÍÌè":
            rec = record()
            rec.sentence, sentend, i = line[:-1], False, 0
        elif line[0] == '-':
            sentend, rec.numofIdens = True, i
        else:
            rec.idens[i] = line
            i += 1
        if sentend:
            res.append(rec.sentence)
            res.append(checkForSyntacticCompatibility(rec))
    # ic.ic(res)
    return res


if __name__ == '__main__':
    res = write_out_aci('../../OSout.aci', '../../out.aci')
    res1 = write_result_aci(res,'../../result.aci')
    # ic.ic(res1)
    # res2 = write_result_aci_from_out_aci('../../out.aci','../../result2.aci')
    # ic.ic(res2)


