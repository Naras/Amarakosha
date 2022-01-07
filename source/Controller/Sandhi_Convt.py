__author__ = 'NarasMG'

from source.Controller import blast
from source.Model import AmaraKosha_Database_Queries

global lingas, antas, vibstr, vachstr, Tganas, Tkarmas, Tpadis, Tyit, purstr, mesg, Voices
lingas = ["स्त्रीलिङ्गः", "पुल्लिङ्गः", "नपुंसकलिङ्गः", "स्त्री.पुं", "स्त्री.नपुं", "पुं.नपुं", "स्त्री.पुं.नपुं", "अलिङ्ग"]
antas = ["a,अ", "b,आ", "c,इ", "d,ई", "e,उ", "f,ऊ", "g,ऋ", "h,ॠ", "i,ङ", "j,इ़", "k,ए", "l,ऎ", "m,ओ", "n,औ", "p,च",
         "r,ण", "s,त", "t,थ", "u,द", "v,ध", "w,न", "x,प", "y,भ", "z,म", "A,रेफ", "B,व", "C,श", "D,ष", "E,स", "F,ह"]


vibstr = ["प्रथमा", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी", "षष्ठी", "सप्तमी", "सं प्रथमा"]

vachstr = ["एकवचन", "द्विवचन", "बहुवचन"]

Tganas = ["भ्वादिगणः", "अदादिगणः", "जुहोत्यादिगणः", "दिवादिगणः", "स्वादिगणः", "तुदादिगणः", "रुधादिगणः", "तनादिगणः", "क्रयादिगणः", "चुरादिगणः"]

Tkarmas = ["सकर्मकः", "अकर्मकः", "द्विकर्मकः"]

Tpadis = ["परस्मैपदी", "आत्मनेपदी", "उभयपदी"]

Tyit = ["सेट्","अनिट्", "वेट्"]

purstr = ["प्रथमपुरुषः", "मध्यमपुरुषः", "उत्तमपुरुषः"]

mesg = ["The sentence is syntactically compatible"
        "The sentence is syntactically not compatible",
        "ÒeLeceefJeYeef„",
        "le=leer³eefJeYeef„",
        "lJec/®e/Jee/³egJeec/³et³ec/Denc/DeeJeec/Je³eced",
        "³egJeec",
        "³et³ec",
        "Denc",
        "DeeJeec",
        "Je³eced",
        "Deefmce/YeJeeefce",
        "mJeë/YeJeeJeë",
        "mceë/YeJeeceë",
        "Deefme/YeJeefme",
        "mLeë/YeJeLeë",
        "mLe/YeJeLe",
        "Deefmle/YeJeefle",
        "mleë/YeJeleë",
        "meefvle/YeJeefvle",
        "Any subanta other than ³eg<ceod and Demceod Meyo",
        "Yet³eles",
        "Noun(s)",
        "Pronoun(s)",
        "Adjective(s)",
        "Krdanta(s)",
        "KrdAvyaya(s)",
        "Avyaya(s)",
        "Verb(s)",
        "Verb",
        "Subject(s)",
        "Object(s)",
        "Instrument(s)",
        "Dative(s)",
        "Ablative(s)",
        "Genitive(s)",
        "Locative(s)",
        "Vocative(s)"]

Voices = ["कर्तरि", "कर्मणि"]

Suffix = ["अ"
    , "अः"
    , "अःसु"
    , "अक्"
    , "अक्षु"
    , "अग्भिः"
    , "अग्भ्यः"
    , "अग्भ्याम्"
    , "अङ्"
    , "अङ्क्षु"
    , "अङ्भिः"
    , "अङ्भ्यः"
    , "अङ्भ्याम्"
    , "अङ्षु"
    , "अञ्चः"
    , "अञ्चम्"
    , "अञ्चा"
    , "अञ्चाम्"
    , "अञ्चि"
    , "अञ्चे"
    , "अञ्चोः"
    , "अञ्चौ"
    , "अणः"
    , "अणम्"
    , "अणा"
    , "अणाम्"
    , "अणि"
    , "अणी"
    , "अणे"
    , "अणोः"
    , "अणौ"
    , "अतः"
    , "अता"
    , "अताम्"
    , "अति"
    , "अते"
    , "अतोः"
    , "अत्"
    , "अत्सु"
    , "अदः"
    , "अदा"
    , "अदाम्"
    , "अदि"
    , "अदे"
    , "अदोः"
    , "अद्भिः"
    , "अद्भ्यः"
    , "अद्भ्याम्"
    , "अनः"
    , "अना"
    , "अनाम्"
    , "अनि"
    , "अनी"
    , "अने"
    , "अनोः"
    , "अन्"
    , "अन्तः"
    , "अन्तम्"
    , "अन्तौ"
    , "अभिः"
    , "अभ्यः"
    , "अभ्याम्"
    , "अम्"
    , "अयः"
    , "अयम्"
    , "अया"
    , "अयाम्"
    , "अयि"
    , "अये"
    , "अयोः"
    , "अयौ"
    , "अरः"
    , "अरम्"
    , "अरि"
    , "अरौ"
    , "अलः"
    , "अलम्"
    , "अलि"
    , "अलौ"
    , "अल्"
    , "अवः"
    , "अवा"
    , "अवाट्"
    , "अवाट्सु"
    , "अवाड्"
    , "अवाड्भिः"
    , "अवाड्भ्यः"
    , "अवाड्भ्याम्"
    , "अवाम्"
    , "अवाहः"
    , "अवाहम्"
    , "अवाहौ"
    , "अवि"
    , "अवे"
    , "अवोः"
    , "असः"
    , "असम्"
    , "असा"
    , "असाम्"
    , "असि"
    , "असी"
    , "असु"
    , "असे"
    , "असोः"
    , "असौ"
    , "अस्मात्"
    , "अस्मिन्"
    , "अस्मै"
    , "अस्य"
    , "अस्याः"
    , "अस्याम्"
    , "अस्यै"
    , "अस्सु"
    , "आ"
    , "आंसः"
    , "आंसम्"
    , "आंसि"
    , "आंसौ"
    , "आः"
    , "आःषु"
    , "आणः"
    , "आणम्"
    , "आणाम्"
    , "आणि"
    , "आणौ"
    , "आत्"
    , "आत्सु"
    , "आदः"
    , "आदम्"
    , "आदौ"
    , "आद्"
    , "आद्भिः"
    , "आद्भ्यः"
    , "आद्भ्याम्"
    , "आनः"
    , "आनम्"
    , "आनाम्"
    , "आनि"
    , "आनौ"
    , "आन्"
    , "आभिः"
    , "आभ्यः"
    , "आभ्याम्"
    , "आम्"
    , "आय"
    , "आयः"
    , "आयम्"
    , "आयाः"
    , "आयाम्"
    , "आयै"
    , "आयौ"
    , "आरः"
    , "आरम्"
    , "आरा"
    , "आराम्"
    , "आरि"
    , "आरे"
    , "आरोः"
    , "आरौ"
    , "आर्भिः"
    , "आर्भ्यः"
    , "आर्भ्याम्"
    , "आर्षु"
    , "आवः"
    , "आवम्"
    , "आवा"
    , "आवाम्"
    , "आवि"
    , "आवे"
    , "आवोः"
    , "आवौ"
    , "आसाम्"
    , "आसु"
    , "इ"
    , "इः"
    , "इचः"
    , "इचा"
    , "इचाम्"
    , "इचि"
    , "इची"
    , "इचे"
    , "इचोः"
    , "इणः"
    , "इणम्"
    , "इणा"
    , "इणाम्"
    , "इणि"
    , "इणी"
    , "इणे"
    , "इणोः"
    , "इणौ"
    , "इनः"
    , "इनम्"
    , "इना"
    , "इनाम्"
    , "इनि"
    , "इनी"
    , "इने"
    , "इनोः"
    , "इनौ"
    , "इन्"
    , "इभिः"
    , "इभ्यः"
    , "इभ्याम्"
    , "इम्"
    , "इयः"
    , "इयम्"
    , "इया"
    , "इयाः"
    , "इयाम्"
    , "इयि"
    , "इये"
    , "इयै"
    , "इयोः"
    , "इयौ"
    , "इरः"
    , "इरम्"
    , "इरा"
    , "इराम्"
    , "इरि"
    , "इरे"
    , "इरोः"
    , "इरौ"
    , "इर्भिः"
    , "इर्भ्यः"
    , "इर्भ्याम्"
    , "इवः"
    , "इवत्सु"
    , "इवद्भिः"
    , "इवद्भ्यः"
    , "इवद्भ्याम्"
    , "इवन्"
    , "इवम्"
    , "इवा"
    , "इवांसः"
    , "इवांसम्"
    , "इवांसौ"
    , "इवान्"
    , "इवाम्"
    , "इवि"
    , "इवे"
    , "इवोः"
    , "इवौ"
    , "इषः"
    , "इषम्"
    , "इषा"
    , "इषाम्"
    , "इषि"
    , "इषी"
    , "इषु"
    , "इषे"
    , "इषोः"
    , "इषौ"
    , "इष्षु"
    , "इ़भिः"
    , "इ़भ्यः"
    , "इ़भ्याम्"
    , "इ़षु"
    , "ई"
    , "ईंषि"
    , "ईः"
    , "ईचः"
    , "ईचा"
    , "ईचाम्"
    , "ईचि"
    , "ईचे"
    , "ईचोः"
    , "ईणाम्"
    , "ईणि"
    , "ईनाम्"
    , "ईनि"
    , "ईन्"
    , "ईभिः"
    , "ईभ्यः"
    , "ईभ्याम्"
    , "ईम्"
    , "ईयः"
    , "ईर्भिः"
    , "ईर्भ्यः"
    , "ईर्भ्याम्"
    , "ईर्षु"
    , "ईषु"
    , "उ"
    , "उः"
    , "उणः"
    , "उणा"
    , "उणि"
    , "उणी"
    , "उणे"
    , "उणोः"
    , "उनः"
    , "उना"
    , "उनि"
    , "उनी"
    , "उने"
    , "उनोः"
    , "उभिः"
    , "उभ्यः"
    , "उभ्याम्"
    , "उम्"
    , "उरः"
    , "उरम्"
    , "उरा"
    , "उराम्"
    , "उरि"
    , "उरे"
    , "उरोः"
    , "उरौ"
    , "उर्भिः"
    , "उर्भ्यः"
    , "उर्भ्याम्"
    , "उल्"
    , "उवः"
    , "उवम्"
    , "उवा"
    , "उवाः"
    , "उवाम्"
    , "उवि"
    , "उवे"
    , "उवै"
    , "उवोः"
    , "उवौ"
    , "उषः"
    , "उषम्"
    , "उषा"
    , "उषाम्"
    , "उषि"
    , "उषी"
    , "उषु"
    , "उषे"
    , "उषोः"
    , "उषौ"
    , "उष्षु"
    , "ऊ"
    , "ऊंषि"
    , "ऊः"
    , "ऊणाम्"
    , "ऊणि"
    , "ऊनाम्"
    , "ऊनि"
    , "ऊन्"
    , "ऊभिः"
    , "ऊभ्यः"
    , "ऊभ्याम्"
    , "ऊम्"
    , "ऊर्भिः"
    , "ऊर्भ्यः"
    , "ऊर्भ्याम्"
    , "ऊर्षु"
    , "ऊषु"
    , "ऋ"
    , "ऋणः"
    , "ऋणा"
    , "ऋणि"
    , "ऋणी"
    , "ऋणे"
    , "ऋणोः"
    , "ऋतः"
    , "ऋता"
    , "ऋताम्"
    , "ऋति"
    , "ऋती"
    , "ऋते"
    , "ऋतोः"
    , "ऋत्"
    , "ऋत्सु"
    , "ऋद्"
    , "ऋद्भिः"
    , "ऋद्भ्यः"
    , "ऋद्भ्याम्"
    , "ऋन्ति"
    , "ऋभिः"
    , "ऋभ्यः"
    , "ऋभ्याम्"
    , "ऋषु"
    , "ॠः"
    , "ॠणाम्"
    , "ॠणि"
    , "ॠन्"
    , "ॠभिः"
    , "ॠभ्यः"
    , "ॠभ्याम्"
    , "ॠम्"
    , "ॠषु"
    , "ए"
    , "एः"
    , "एण"
    , "एन"
    , "एभिः"
    , "एभ्यः"
    , "एभ्याम्"
    , "एषाम्"
    , "एषु"
    , "ऐः"
    , "ओ"
    , "ओः"
    , "ओभिः"
    , "ओभ्यः"
    , "ओभ्याम्"
    , "ओषु"
    , "औ"
    , "औः"
    , "औभिः"
    , "औभ्यः"
    , "औभ्याम्"
    , "औषु"
    , "औहः"
    , "औहा"
    , "औहाम्"
    , "औहि"
    , "औहे"
    , "औहोः"
    , "क्"
    , "क्षः"
    , "क्षम्"
    , "क्षा"
    , "क्षाम्"
    , "क्षि"
    , "क्षु"
    , "क्षे"
    , "क्षोः"
    , "क्षौ"
    , "ग्"
    , "ग्भिः"
    , "ग्भ्यः"
    , "ग्भ्याम्"
    , "चः"
    , "चम्"
    , "चा"
    , "चाम्"
    , "चि"
    , "चे"
    , "चोः"
    , "चौ"
    , "जः"
    , "जम्"
    , "जा"
    , "जाम्"
    , "जि"
    , "जे"
    , "जोः"
    , "जौ"
    , "ट्"
    , "ट्त्सु"
    , "ट्सु"
    , "ड्"
    , "ड्भिः"
    , "ड्भ्यः"
    , "ड्भ्याम्"
    , "णः"
    , "णम्"
    , "णा"
    , "णाम्"
    , "णि"
    , "णे"
    , "णोः"
    , "णौ"
    , "ण्"
    , "ण्णाम्"
    , "ण्ण्सु"
    , "ण्त्सु"
    , "ण्भिः"
    , "ण्भ्यः"
    , "ण्भ्याम्"
    , "तः"
    , "तम्"
    , "तव"
    , "ता"
    , "ताम्"
    , "ति"
    , "ती"
    , "तुभ्यम्"
    , "ते"
    , "तोः"
    , "तौ"
    , "त्"
    , "त्रयः"
    , "त्रयाणाम्"
    , "त्रिभ्यः"
    , "त्रिषु"
    , "त्रीन्"
    , "त्वत्"
    , "त्वम्"
    , "त्वया"
    , "त्वयि"
    , "त्वा"
    , "त्वाम्"
    , "त्सु"
    , "थः"
    , "था"
    , "थाम्"
    , "थि"
    , "थिभिः"
    , "थिभ्यः"
    , "थिभ्याम्"
    , "थिषु"
    , "थे"
    , "थोः"
    , "दः"
    , "दम्"
    , "दा"
    , "दाम्"
    , "दि"
    , "दिवः"
    , "दिवा"
    , "दिवाम्"
    , "दिवि"
    , "दिवी"
    , "दिवे"
    , "दिवोः"
    , "दी"
    , "दे"
    , "दोः"
    , "दौ"
    , "द्"
    , "द्भयः"
    , "द्भिः"
    , "द्भ्यः"
    , "द्भ्याम्"
    , "द्यु"
    , "द्युभिः"
    , "द्युभ्यः"
    , "द्युभ्याम्"
    , "द्युषु"
    , "धः"
    , "धम्"
    , "धा"
    , "धाम्"
    , "धि"
    , "धे"
    , "धोः"
    , "धौ"
    , "न"
    , "नः"
    , "नम्"
    , "नयोः"
    , "नस्य"
    , "ना"
    , "नाः"
    , "नात्"
    , "नानाम्"
    , "नान्"
    , "नाभ्याम्"
    , "नाम्"
    , "नाय"
    , "नि"
    , "नी"
    , "ने"
    , "नेन"
    , "नेभ्यः"
    , "नेषु"
    , "नैः"
    , "नोः"
    , "नौ"
    , "न्"
    , "न्तः"
    , "न्तम्"
    , "न्ति"
    , "न्ती"
    , "न्तौ"
    , "न्थाः"
    , "न्थानः"
    , "न्थानम्"
    , "न्थानौ"
    , "न्भिः"
    , "न्भ्यः"
    , "न्भ्याम्"
    , "न्सु"
    , "प्"
    , "प्सु"
    , "ब्भिः"
    , "ब्भ्यः"
    , "ब्भ्याम्"
    , "भः"
    , "भम्"
    , "भा"
    , "भाम्"
    , "भि"
    , "भिः"
    , "भे"
    , "भोः"
    , "भौ"
    , "भ्यः"
    , "भ्याम्"
    , "म्शि"
    , "म्षि"
    , "म्सः"
    , "म्सम्"
    , "म्सा"
    , "म्साम्"
    , "म्सि"
    , "म्सी"
    , "म्से"
    , "म्सोः"
    , "म्सौ"
    , "यः"
    , "यक्षु"
    , "यग्भिः"
    , "यग्भ्यः"
    , "यग्भ्याम्"
    , "यङ्"
    , "यञ्चः"
    , "यञ्चम्"
    , "यञ्चौ"
    , "यम्"
    , "या"
    , "याः"
    , "याम्"
    , "यि"
    , "युः"
    , "युभिः"
    , "युभ्यः"
    , "युभ्याम्"
    , "युवयोः"
    , "युवाभ्याम्"
    , "युवाम्"
    , "युषु"
    , "युष्मत्"
    , "युष्मभ्यम्"
    , "युष्माकम्"
    , "युष्मान्"
    , "युष्माभिः"
    , "युष्मासु"
    , "यूयम्"
    , "ये"
    , "यै"
    , "योः"
    , "यौ"
    , "यौः"
    , "रः"
    , "रा"
    , "राम्"
    , "रि"
    , "रे"
    , "रोः"
    , "रौ"
    , "ला"
    , "ले"
    , "लोः"
    , "वः"
    , "वत्सु"
    , "वद्भिः"
    , "वद्भ्यः"
    , "वद्भ्याम्"
    , "वन्"
    , "वम्"
    , "वा"
    , "वांसः"
    , "वांसम्"
    , "वांसौ"
    , "वाः"
    , "वान्"
    , "वाम्"
    , "वि"
    , "वे"
    , "वै"
    , "वोः"
    , "वौ"
    , "शः"
    , "शम्"
    , "शा"
    , "शाम्"
    , "शि"
    , "शी"
    , "शे"
    , "शोः"
    , "शौ"
    , "षः"
    , "षम्"
    , "षा"
    , "षाम्"
    , "षि"
    , "षी"
    , "षे"
    , "षोः"
    , "षौ"
    , "सः"
    , "सम्"
    , "सा"
    , "साम्"
    , "सि"
    , "सी"
    , "सु"
    , "से"
    , "सोः"
    , "सौ"
    , "हः"
    , "हम्"
    , "हा"
    , "हाम्"
    , "हि"
    , "हे"
    , "होः"]

def Convt(sufcode):   # copied from old VB code and changed to get the suffix, rather than index to the suffix in
    No = []
    for ch in sufcode:
        nr = ord(ch)
        if nr in range(48,58):
            No.append(nr - 48)
        elif nr in range(96,123):
            No.append(nr - 87)
    res = 36 * No[0] + No[1] if No != [] else -1
    if res in range(len(Suffix)): return Suffix[res]
    else: return ''
def Sandhi(inword):
    # print('iscii %s devanagari %s'%(inword, Amarakosha_Database_Queries.iscii_unicode(inword)))
    halanth = chr(232)
    # inword = inword.split()
    outword = ''
    if inword == '': return ''
    inword = AmaraKosha_Database_Queries.unicode_iscii(inword)
    i = 0
    while i < len(inword):
        ch = inword[i]
        if ch != halanth:
            outword += ch
            if (i < len(inword) - 1) and ch != '/':
                ch = inword[i + 1]
                if ord(ch) in range(164, 178):
                    i += 1
                    ch1 = inword[i]
                    if i > 1:
                        if inword[i-2] != " ":
                            if ord(ch1) == 164: pass
                            elif ord(ch1) in range(165, 178):
                                outword += chr(218 - 165 + ord(ch1))
                            else: outword += ch + ch1
                        else: outword += ch1
                    else: outword += ch1
        else:  # halanth
          i += 1
          if i <= len(inword) - 1:
              ch1 = inword[i]
              if ord(ch1) == 164: pass
              elif ord(ch1) in range(165, 178):
                  outword += chr(218 - 165 + ord(ch1))
              else: outword += ch + ch1
          else: outword += ch
        i += 1
    # print('%s after %s %s %s'%(inword, outword, cli_browse.iscii_unicode(inword), cli_browse.iscii_unicode(outword)))
    return AmaraKosha_Database_Queries.iscii_unicode(outword)
def doSandhi1(tigantaForm: str, upasarga: str) -> str:
    aDict1 = {"अ":"आ", "आ":"आ", "इ":"ए", "ई":"ए", "उ":"ओ", "ऊ":"ओ", "ऋ":"आर्", "ए":"ऐ", "ऐ":"ऐ", "ओ":"औ", "औ":"औ"}
    bDict = {"अ": aDict1, "आ": aDict1,
             "इ":{"इ":"ई", "ई":"ई",
                  "अ":"य्", "आ":"य्", "उ":"य्", "ऊ":"य्", "ऋ":"य्", "ए":"य्", "ऐ":"य्", "ओ":"य्", "औ":"य्"},
             "उ":{"उ":"ऊ", "ऊ":"ऊ", "अ":"व्", "आ":"व्", "इ":"व्", "ई":"व्", "ऋ":"व्", "ए":"व्", "ऐ":"व्", "ओ":"व्", "औ":"व्"}    }
    c = bDict.get(upasarga[0], '')
    if c != '': c = c.get(tigantaForm[0], '')
    flag = 1 if upasarga[0] in bDict else 0
    if upasarga[0] == "इ" and tigantaForm[0] in ["अ", "आ", "उ", "ऊ", "ऋ", "ए", "ऐ", "ओ", "औ"]: flag = 2
    if upasarga[0] == "उ" and tigantaForm[0] in ["अ", "आ", "इ", "ई", "ऋ", "ए", "ऐ", "ओ", "औ"]: flag = 1
    if flag > 0:
        sandhiForm = upasarga[:-1] + c
        if flag == 2: sandhiForm += tigantaForm
        else: sandhiForm += tigantaForm[1:]
    else: sandhiForm = upasarga + tigantaForm
    return sandhiForm
def doSandhi2(tigantaForm: str, upasarga: str) -> str:
    sandhiForm = upasarga
    upasargaDict = {"सम्":{"क":"ङ", "ख":"ङ", "ग":"ङ", "घ":"ङ", "ङ":"ङ"},
                    "निर्":{"क":"ष", "ख":"ष", "ट":"ष", "ठ":"ष", "प":"ष", "फ":"ष", "ष":"ष",
                            "च":"श", "छ":"श", "श":"श",
                            "त":"स", "थ":"स", "स":"स"},
                    "दुर्":{"क":"ष", "ख":"ष", "ट":"ष", "ठ":"ष", "प":"ष", "फ":"ष", "ष":"ष",
                            "च":"श", "छ":"श", "श":"श",
                            "त":"स", "थ":"स", "स":"स"},
                    "उत्":{"अ":"द", "आ":"द", "इ":"द", "ई":"द", "उ":"द", "ऊ":"द", "ऋ":"द", "ए":"द", "ऐ":"द", "ओ":"द", "औ":"द",
                           "ग":"द", "घ":"द", "द":"द", "ध":"द", "ब":"द", "भ":"द", "य":"द", "र":"द", "व":"द",
                           "च":"च", "छ":"च",
                           "ज":"ज", "झ":"ज",
                           "ठ":"ट",
                           "न":"न", "म":"न",
                           "ल":"ल",
                           "श":"च",
                           "ह":"द"}
                   }
    sandhiForm[0] = upasargaDict[tigantaForm[0]][upasarga[0]]
    if tigantaForm == "र": sandhiForm = {"निर्":"नी", "दुर्":"दू"}[upasarga]
    flag = 2 if upasarga == "उत्" and tigantaForm[0] == "ह" else 0
    if flag == 1: sandhiForm += "छ"
    elif flag == 2: sandhiForm += tigantaForm[:-1]
    else: sandhiForm += tigantaForm
def doSandhiofUpasargaAndTigantaForm(tigantaForm: str, upasarga: str) -> str:
    if upasarga in ["सम्", "निर्", "दुर्", "उत्"]: sandhiForm = doSandhi2(tigantaForm, upasarga)
    else: sandhiForm = doSandhi1(blast.performBlast(tigantaForm), blast.performBlast(upasarga) )
    return blast.phoneticallyJoin(sandhiForm)
def visandhi(inword: str) -> str:
    # print('iscii %s devanagari %s'%(inword, cli_browse.iscii_unicode(inword)))
    halanth = chr(232)
    # inword = inword.split()
    outword = ''
    i = 0
    inword = AmaraKosha_Database_Queries.unicode_iscii(inword)
    while i < len(inword):
        ch = inword[i]
        if ord(ch) in range(164,178): outword+= ch
        elif ord(ch) in range(179,217):
            if (i < len(inword) - 1):
                ch1 = inword[i + 1]
                outword += ch + halanth
                if ord(ch1) == halanth: i += 1
                else:
                    if ord(ch1) in range(218,231):
                        i += 1
                        outword += chr(ord(ch1) - (218 - 165))
                    else: outword += chr(164)
            else: i += 1
        else: outword+= ch
        i += 1
    return AmaraKosha_Database_Queries.iscii_unicode(outword)
def decode(code: int) -> str:
    if code in range(10): return '0' + str(code)
    elif code in range(10,36): return '0' + chr(code + 87)
    else:
        code, rem = code // 36, code % 36
        if code in range(10): res = str(code)
        elif code in range(10, 36): res = chr(code + 87)
        if rem in range(10): res += str(rem)
        elif rem in range(10, 36): res += chr(rem + 87)
        return res

if __name__ == '__main__':
     print(Suffix[0:5], Suffix[234:245])