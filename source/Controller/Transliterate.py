__author__ = 'NarasMG'


IndianLanguages = ('devanagari','bengali','gurmukhi','gujarati','oriya','tamizh','telugu','kannada','malayalam')
IndianUnicodeValue = [['devanagari'],['bengali'],['gurmukhi'],['gujarati'],['oriya'],['tamizh'],['telugu'],['kannada'],['malayalam']]
def detectLang(ch):
    start_end = {0:[0x0900,0x097F],1:[0x980, 0x9ff],2:[0xa00, 0xa7f], 3:[0xa80, 0xaff], \
             4:[0x0900,0x097F],5:[0xb00, 0xb7f],6:[0xb80, 0xbff],7:[0xc00, 0xc7f],8:[0xc80, 0xcff]}
    for k,v in start_end.items():
        ch_hex = ord(ch)
        if ch_hex >= v[0] and ch_hex <= v[1]:
            return k
    return None
def transliterate(ch,targetScript):
    ZWJ = u'\u200d'  # Zero Width Joiner
    ZWNJ = u'\u200c'  # Zero Width Non Joiner
    DANDA = u'\u0964'
    DOUBLE_DANDA = u'\u0965'
    if ord(ch) < 128: return ch  # ascii
    elif ch in [DANDA, DOUBLE_DANDA, ZWJ, ZWNJ]: return ch # extra devanagari chars
    else:
        return IndianUnicodeValue[targetScript][ord(ch) - ord(IndianUnicodeValue[detectLang(ch)][1])+1]
def transliterate_lines(source,scriptTarget='devanagari'):
    for i,e in enumerate(IndianLanguages):
        if scriptTarget == e:
            trg = i
            break
    target = ''
    try:
        for s in source:
            t = ''
            for c in s:
                t += transliterate(c,trg)
            target += t
    except Exception as e:
        raise Exception('transliterate - %s char %s(%s) source %s'%(e, s, ord(s), source))
    return target
def init():
    for j in range(9):
        for i in range(0x0900, 0x097F):  # (0x0905,0x093A):
            IndianUnicodeValue[j].append(chr(i + 128 * j))
init()