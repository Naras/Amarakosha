__author__ = 'NarasMG'

anusvara, visarga, halanth, nukta, virama = 162, 163, 232, 233, 234

def vowelModifierOf(anIndLangVowel):
    if ord(anIndLangVowel) in range(164,179):
        return {164:"¤", 165:"Ú", 166:"Û", 167:"Ü", 168:"Ý", 169:"Þ", 170:"ß", 171:"à", 172:"á", 173:"â", 174:"ã", 175:"ä", 176:"å", 177:"æ", 178:"ç"}[ord(anIndLangVowel)]
    else: return anIndLangVowel
def vowelFor(s):
    if s == '': return "¤"
    elif ord(s) in [anusvara, visarga, nukta, virama]: return s
    elif ord(s) in range(218,232):
        return {218 :"¥", 219 :"¦", 220 :"§", 221 :"¨", 222 :"©", 223 :"ª", 224 :"«", 225 :"¬", 226 :"­", 227 :"®", 228 :"¯", 229 :"°", 230 :"±", 231 :"²"}[ord(s)]
def consonantAsString(s1, s2):
    answer = ''
    c = 0 if s1 == '' else ord(s1)
    d = 0 if s2 == '' else ord(s2)
    if c in range(179, 217):  # consonant
        if d in [anusvara, visarga]:  answer += s1 + "è¤" + s2
        elif d == 0: answer = s1 + "è¤"
        else: answer = s1 + "è" + vowelFor(s2)
    return answer
def transform(c1, c2):
    c = 0 if c1 == '' else ord(c1)
    d = 0 if c2 == '' else ord(c2)
    if c <= 160: # not Devanagari char
        return c1
    elif c in range(164,179): # is vowel
        if d in [anusvara, visarga]: return c1 + c2
        else: return c1
    elif c in [anusvara, visarga, nukta, virama]: return c1
    elif d in [0] + list(range(164, 217)): return consonantAsString(c1, '') # empty, vowel or consonant
    elif d == halanth: return c1 + c2
    elif d in [anusvara, visarga] + list(range(218, 232)): # vowel modifier
        return consonantAsString(c1, c2)
    else: return ''
def performBlast(s):
    if s == None or s == '' or (ord(s[0]) == visarga and len(s) == 1): #empty or visarga
        return s
    if ord(s[0]) in [halanth, anusvara, visarga] + list(range(218,232)):  # halanth, visarga or vowel modifier
        raise ValueError('blast function: invalid string ' + s)
    answer, i = '', 0
    while i < len(s) - 1:
        answer += transform(s[i], s[i+1])
        # print('pB answer %s'%answer)
        i += 1
        if ord(s[i]) in [halanth, anusvara, visarga] + list(range(218,232)): i += 1
    return answer
def phoneticallyJoin(phoneticallySplitWord):
    output, i = '', 0
    while i <= len(phoneticallySplitWord) - 1:
        c1, c2 = phoneticallySplitWord[i], phoneticallySplitWord[i+1] if i < len(phoneticallySplitWord)-1 else ''
        c = 0 if c1 == '' else ord(c1)
        d = 0 if c2 == '' else ord(c2)
        if c == halanth and d in range(164,179): # halath and vowel
            output += vowelModifierOf(c2) if d != 164 else ''
            i += 2
        else:
            if c1 != '': output += c1
            i += 1
    return output