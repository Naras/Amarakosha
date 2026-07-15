# -*- coding: utf-8 -*-

# Sanskrit Grammatical Categories and Mappings
LINGAS = ["स्त्रीलिङ्गः", "पुल्लिङ्गः", "नपुंसकलिङ्गः", "स्त्री.पुं", "स्त्री.नपुं", "पुं.नपुं", "स्त्री.पुं.नपुं", "अलिङ्ग"]
ANTAS = {
    "a": "अ", "b": "आ", "c": "इ", "d": "ई", "e": "उ", "f": "ऊ", "g": "ऋ", "h": "ॠ", "i": "ङ", "j": "इ़", "k": "ए",
    "l": "ऎ", "m": "ओ", "n": "औ", "p": "च", "r": "ण", "s": "त", "t": "थ", "u": "द", "v": "ध", "w": "न", "x": "प",
    "y": "भ", "z": "म", "A": "रेफ", "B": "व", "C": "श", "D": "ष", "E": "स", "F": "ह"
}
VIBHAKTIS = ["प्रथमा", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी", "षष्ठी", "सप्तमी", "सं प्रथमा"]
VACANAS = ["एकवचन", "द्विवचन", "बहुवचन"]
TGANAS = ["भ्वादिगणः", "अदादिगणः", "जुहोत्यादिगणः", "दिवादिगणः", "स्वादिगणः", "तुदादिगणः", "रुधादिगणः", "तनादिगणः", "क्रयादिगणः", "चुरादिगणः"]
TKARMAS = ["सकर्मकः", "अकर्मकः", "द्विकर्मकः"]
TPADIS = ["परस्मैपदी", "आत्मनेपदी", "उभयपदी"]
TYITS = ["सेट्", "अनिट्", "वेट्"]
PURUSHAS = ["प्रथमपुरुषः", "मध्यमपुरुषः", "उत्तमपुरुषः"]
LAKARAS = ["लट्", "लिट्", "लुट्", "लृट्", "लोट्", "लङ्", "विधिलिङ्", "अशीर्लिङ्", "लुङ्", "लृङ्"]
VOICES = ["कर्तरि", "कर्मणि"]
DHATU_VIDHAS = ["केवलकृदन्तः", "णिजन्तः", "सन्नन्तः"]
DHATU_VIDHAS_TIGANTA = ["केवलतिगंतः", "णिजन्तः", "सन्नन्तः"]
PRATYAYA_VIDHAHS = ["तव्य", "अनीयर्", "य", "क्त", "क्तवतु", "शतृ", "शानच्", "स्यशतृ", "स्यशानच्", "तुमुन्", "क्त्वा"]
KRDANTA_VIDHAHS = ["विध्यर्थः", "भूतः", "वर्तमानः", "भविष्यत्", "कृदव्ययम्"]

# Legacy validation messages used by Syntax Analysis
SYNTAX_MESG = [
    "The sentence is syntactically compatible"
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
    "Vocative(s)"
]
