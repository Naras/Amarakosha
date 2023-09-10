__author__ = 'naras_mg'

import os

# libraries
from flask import Flask, jsonify, abort, make_response, request
import json, networkx as nx, logging

# from icecream import ic
from networkx.readwrite import json_graph
from datetime import datetime
from flask_cors import CORS, cross_origin

import sys
# print('Include import path %s'%os.getcwd())
sys.path.insert(1, os.getcwd())
from source.Controller import Kosha_Subanta_Krdanta_Tiganta
from source.Controller.Transliterate import transliterate_lines, IndianLanguages
from source.Model import AmaraKosha_Database_Queries

logging.basicConfig(filename='AmarakoshaRestService.log', format='%(asctime)s %(message)s', level=logging.DEBUG)


def krdantaGeneration(dhatuNo):
    f, k = {}, {}
    allForms, emptyForms, dupFormKeys = [], [], []
    allKrds, emptyKrd, dupKrdKeys = [], [], []
    for dhatuVidah in ['केवलकृदन्तः', 'णिजन्तः', 'सन्नन्तः']:
        f[dhatuVidah], k[dhatuVidah] = {}, {}
        for krdantaVidah in ['विध्यर्थः', 'भूतः', 'वर्तमानः', 'भविष्यत्', 'कृदव्ययम्']:
            f[dhatuVidah][krdantaVidah], k[dhatuVidah][krdantaVidah] = {}, {}
            for krdMode in ['तव्य', 'अनीयर्', 'य', 'क्त', 'क्तवतु', 'शतृ', 'शानच्', 'स्यशतृ', 'स्यशानच्', 'क्त्वा']:
                forms, krdData = Kosha_Subanta_Krdanta_Tiganta.krdanta_Generation(dhatuNo, dhatuVidah, krdantaVidah, krdMode)
                if forms != []:
                    if forms not in allForms:
                        f[dhatuVidah][krdantaVidah][krdMode] = forms
                        allForms.append(forms)
                    else: dupFormKeys.append([dhatuVidah, krdantaVidah, krdMode])
                else: emptyForms.append([dhatuVidah, krdantaVidah, krdMode])
                if krdData not in [None, []]:
                    if krdData not in allKrds:
                        k[dhatuVidah][krdantaVidah][krdMode] = krdData
                        allKrds.append(krdData)
                    else: dupKrdKeys.append([dhatuVidah, krdantaVidah, krdMode])
                else: emptyKrd.append([dhatuVidah, krdantaVidah, krdMode])
    return f, k, emptyForms, emptyKrd, dupFormKeys, dupKrdKeys
def tigantaGeneration(dhatuNo):
        f, k = {}, {}
        allForms, emptyForms, dupFormKeys = [], [], []
        allTigs, emptyTig, dupTigKeys = [], [], []
        for dhatuVidah in ['केवलतिगंतः', 'णिजन्तः', 'सन्नन्तः']:
            f[dhatuVidah], k[dhatuVidah] = {}, {}
            for voice in ["कर्तरि", "कर्मणि"]:
                f[dhatuVidah][voice], k[dhatuVidah][voice] = {}, {}
                for lakara in ["लट्", "लिट्", "लुट्", "लृट्", "लोट्", "लङ्", "विधिलिङ्", "अशीर्लिङ्", "लुङ्", "लृङ्"]:
                    forms, tigData = Kosha_Subanta_Krdanta_Tiganta.tiganta_Generation(dhatuNo, dhatuVidah, voice, lakara)
                    if forms != []:
                        if forms not in allForms:
                            f[dhatuVidah][voice][lakara] = forms
                            allForms.append(forms)
                        else:
                            dupFormKeys.append([dhatuVidah, voice, lakara])
                    else:
                        emptyForms.append([dhatuVidah, voice, lakara])
                    if tigData not in [None, []]:
                        if tigData not in allTigs:
                            k[dhatuVidah][voice][lakara] = tigData
                            allTigs.append(tigData)
                        else:
                            dupTigKeys.append([dhatuVidah, voice, lakara])
                    else:
                        emptyTig.append([dhatuVidah, voice, lakara])
        return f, k, emptyForms, emptyTig, dupFormKeys, dupTigKeys
def loadBandarkar():
    filename = os.path.join('Bandarkar.txt')
    with open(filename, "r", encoding="iso-8859-1") as f:
        dataIscii = [line[:-1] for line in f]
    data = [Kosha_Subanta_Krdanta_Tiganta.transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(item), IndianLanguages[0]) for item in dataIscii]
    return data
def analysis_1(base):
    try:
        subforms, tigforms, krdforms = [], [], []
        Subantas, Krdantas, Tigantas = [], [], []
        syntaxInputFile, bas = [], base.strip()
        numpages, wanted_script = 0, 0
        for i, word in enumerate(bas.split(' ')):
            if word.strip() == '': continue
            wids = 1
            try:
                forms, subDetails = Kosha_Subanta_Krdanta_Tiganta.subanta_Analysis(word, wanted_script + 1)
                if not forms == []: subforms += forms
                for item in subDetails:
                    numpages += 1
                    Subantas.append([item.rupam, transliterate_lines(item.base, IndianLanguages[wanted_script]), item.anta, item.linga, item.vib, item.vach, item.vibvach])
                    syntaxInputFile.append([i + 1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 1, AmaraKosha_Database_Queries.unicode_iscii(item.base),
                                            AmaraKosha_Database_Queries.unicode_iscii(item.erb), item.det, item.vibvach + 1])
                    wids += 1
            except Exception as e:
                logging.debug(e)
            try:
                forms, krdData = Kosha_Subanta_Krdanta_Tiganta.krdanta_Analysis(word, wanted_script + 1)
                if not forms == []: krdforms += forms
                if not krdData == []:
                    Krdantas += krdData
                    numpages += len(krdData)
                    for krdDetail in krdData:
                        syntaxInputFile.append(
                            [i + 1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 2,
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.erb),
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.sabda),
                             krdDetail.det,
                             krdDetail.vibvach + 1, krdDetail.ddet, krdDetail.Dno,
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.verb),
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.nijverb),
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.sanverb),
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.meaning), ('%03d' % krdDetail.GPICode),
                             krdDetail.CombinedM, krdDetail.karmaCode])
                        wids += 1
            except Exception as e:
                logging.debug(e)
            try:
                forms, tigDatas = Kosha_Subanta_Krdanta_Tiganta.tiganta_Analysis(word, wanted_script + 1)
                if not forms == []: tigforms += forms
                if not tigDatas == []:
                    Tigantas += tigDatas
                    numpages += len(tigDatas)
                    for tigData in tigDatas:
                        syntaxInputFile.append([i + 1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 5,
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.base), tigData.Dno,
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.verb),
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.nijverb),
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.sanverb),
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.meaning),
                                                ('%03d' % tigData.GPICode), tigData.pralak, tigData.purvach,
                                                tigData.CombinedM, tigData.karmaCode])
                        wids += 1
            except Exception as e:
                logging.debug(e)
        syntaxInputFile = [AmaraKosha_Database_Queries.unicode_iscii('वाक्यम्') + ' -- %s' % AmaraKosha_Database_Queries.unicode_iscii(bas)]
        for line in syntaxInputFile:
            syntaxInputFile.append('%d) ' % line[0] + ' '.join([str(x) for x in line[1:]]))
        syntaxInputFile.append('----------')
    except Exception as e:
        logging.debug(e)
    subDatas = []
    for vals in Subantas:
        keys = ['रूपं', 'प्रातिपदिकं', 'अंतः', 'लिंगः', 'विभक्तिः', 'वचनः']
        subDat = {}
        for key, val in zip(keys, vals): subDat[key] = val
        subDatas.append(subDat)
    krdDatas = []
    for krdData in Krdantas:
        keys = ['धातुः','धात्वर्य:','णिजि धातु:','सनि धातु:','गण:','पदिः','कर्मः','इट्','धातुविधः','कृदंतविधः','प्रत्ययः','अंतः','लिंगः','प्रातिपदिकं','रूपं']
        vals = [krdData.verb, krdData.meaning, krdData.nijverb, krdData.sanverb, krdData.gana, krdData.padi, krdData.karma, krdData.it,  krdData.dhatuVidhah, krdData.krdantaVidhah, krdData.pratyayaVidhah, krdData.anta, krdData.linga, krdData.sabda, krdforms[0][0]]
        krdDat = {}
        for key, val in zip(keys, vals): krdDat[key] = val
        krdDatas.append(krdDat)
    tigDatas = []
    for tigData in Tigantas:
        keys = ['धातुः','धात्वर्य:','णिजि धातु:','सनि धातु:','गण:','पदिः','कर्मः','इट्','धातुविधः','प्रयोगः','लकारः']
        vals = [tigData.verb, tigData.base,tigData.nijverb, tigData.sanverb, tigData.gana,tigData.padi, tigData.karma, tigData.it, tigData.dhatuVidah, tigData.voice, tigData.lakara]
        tigDat = {}
        for key, val in zip(keys, vals): tigDat[key] = val
        tigDatas.append(tigDat)
    return {'सुबंतः': subDatas, 'सुबंतःForms': subforms, 'कृदंतःForms': krdforms, 'तिगंतःForms': tigforms, 'कृदंतः':krdDatas, 'तिगंतः': tigDatas}
'''def analysis_2(base):
    try:
        Subantas, Subantas2, Krdantas, Tigantas = [], [], [], []
        syntaxInputFile, bas = [], base.strip()
        numpages, wanted_script = 0, 0
        for i, word in enumerate(bas.split(' ')):
            if word.strip() == '': continue
            wids = 1
            try:
                forms, subDetails = Kosha_Subanta_Krdanta_Tiganta.subanta_Analysis(word, wanted_script + 1)
                subDat = {}
                for item in subDetails:
                  for key, val in zip(['रूपं', 'प्रातिपदिकं', 'अंतः', 'लिंगः', 'विभक्तिः', 'वचनः'],
                    [item.rupam, transliterate_lines(item.base, IndianLanguages[wanted_script]), item.anta, item.linga, item.vib, item.vach, item.vibvach]): subDat[key] = val
                subanta = {'सुबंतः': subDat, 'forms':forms}
                Subantas2.append(subanta)
                for item in subDetails:
                    numpages += 1
                    Subantas.append([item.rupam, transliterate_lines(item.base, IndianLanguages[wanted_script]), item.anta, item.linga, item.vib, item.vach, item.vibvach])
                    syntaxInputFile.append([i + 1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 1, AmaraKosha_Database_Queries.unicode_iscii(item.base),
                                            AmaraKosha_Database_Queries.unicode_iscii(item.erb), item.det, item.vibvach + 1])
                    wids += 1
            except Exception as e:
                logging.debug(e)
            try:
                forms, krdDatas = Kosha_Subanta_Krdanta_Tiganta.krdanta_Analysis(word, wanted_script + 1)
                krdDat = {}
                for krdData in krdDatas:
                  for key, val in zip(['धातुः','धात्वर्य:','णिजि धातु:','सनि धातु:','गण:','पदिः','कर्मः','इट्','धातुविधः','कृदंतविधः','प्रत्ययः','अंतः','लिंगः','प्रातिपदिकं'],
                    [krdData.verb, krdData.meaning, krdData.nijverb, krdData.sanverb, krdData.gana, krdData.padi, krdData.karma, krdData.it,  krdData.dhatuVidhah,
                     krdData.krdantaVidhah, krdData.pratyayaVidhah, krdData.anta, krdData.linga, krdData.sabda]): krdDat[key] = val
                  # ,'रूपं', krdforms[0][0]
                krdanta = {'कृदंतः': krdDat, 'forms': forms[:8]}
                # krdanta = {'krdantas': [krd.get() for krd in krdData], 'forms': forms}
                Krdantas.append(krdanta)
                if not krdData == []:
                    numpages += len(krdData)
                    for krdDetail in krdData:
                        syntaxInputFile.append(
                            [i + 1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 2,
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.erb),
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.sabda),
                             krdDetail.det,
                             krdDetail.vibvach + 1, krdDetail.ddet, krdDetail.Dno,
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.verb),
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.nijverb),
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.sanverb),
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.meaning), ('%03d' % krdDetail.GPICode),
                             krdDetail.CombinedM, krdDetail.karmaCode])
                        wids += 1
            except Exception as e:
                logging.debug(e)
            try:
                forms, tigDatas = Kosha_Subanta_Krdanta_Tiganta.tiganta_Analysis(word, wanted_script + 1)
                tigDat = {}
                for tigData in tigDatas:
                  for key, val in zip(['धातुः','धात्वर्य:','णिजि धातु:','सनि धातु:','गण:','पदिः','कर्मः','इट्','धातुविधः','प्रयोगः','लकारः'],
                      [tigData.verb, tigData.base, tigData.nijverb, tigData.sanverb, tigData.gana, tigData.padi, tigData.karma, tigData.it, tigData.dhatuVidah, tigData.voice, tigData.lakara]): tigDat[key] = val
                tiganta = {'तिगंतः': tigDat, 'forms': forms}
                # tiganta = {'tiganta': [tig.get() for tig in tigDatas], 'forms': forms}
                Tigantas.append(tiganta)
                if not tigDatas == []:
                    numpages += len(tigDatas)
                    for tigData in tigDatas:
                        syntaxInputFile.append([i + 1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 5,
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.base), tigData.Dno,
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.verb),
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.nijverb),
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.sanverb),
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.meaning),
                                                ('%03d' % tigData.GPICode), tigData.pralak, tigData.purvach,
                                                tigData.CombinedM, tigData.karmaCode])
                        wids += 1
            except Exception as e:
                logging.debug(e)
        syntaxInputFile = [AmaraKosha_Database_Queries.unicode_iscii('वाक्यम्') + ' -- %s' % AmaraKosha_Database_Queries.unicode_iscii(bas)]
        for line in syntaxInputFile:
            syntaxInputFile.append('%d) ' % line[0] + ' '.join([str(x) for x in line[1:]]))
        syntaxInputFile.append('----------')
    except Exception as e:
        logging.debug(e)
    return {'सुबंतः': Subantas2, 'कृदंतः': Krdantas, 'तिगंतः': Tigantas}
def analysis_3(base):
    try:
        subforms, tigforms, krdforms = [], [], []
        Subantas, Krdantas, Tigantas = [], [], []
        syntaxInputFile, bas = [], base.strip()
        numpages, wanted_script = 0, 0
        analysisResults = []
        for i, word in enumerate(bas.split(' ')):
            if word.strip() == '': continue
            wids = 1
            analysisResult = {word:{}}
            try:
                forms, subDetails = Kosha_Subanta_Krdanta_Tiganta.subanta_Analysis(word, wanted_script + 1)
                if not forms == []: subforms += forms
                analysisResult[word]['सुबंतः'] = []
                for item in subDetails:
                    numpages += 1
                    Subantas.append([item.rupam, transliterate_lines(item.base, IndianLanguages[wanted_script]), item.anta, item.linga, item.vib, item.vach, item.vibvach])
                    syntaxInputFile.append([i + 1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 1, AmaraKosha_Database_Queries.unicode_iscii(item.base),
                                            AmaraKosha_Database_Queries.unicode_iscii(item.erb), item.det, item.vibvach + 1])
                    wids += 1
                    dic = {}
                    for key, val in zip(['रूपं', 'प्रातिपदिकं', 'अंतः', 'लिंगः', 'विभक्तिः', 'वचनः'], [item.rupam, item.base, item.anta, item.linga, item.vib, item.vach, item.vibvach]): dic[key] = val
                    analysisResult[word]['सुबंतः'].append({'keyvaluepairs': dic, 'forms':forms})
            except Exception as e:
                logging.debug(e)
            try:
                forms, krdData = Kosha_Subanta_Krdanta_Tiganta.krdanta_Analysis(word, wanted_script + 1)
                # ic(word, [krd.get() for krd in krdData])
                if not forms == []: krdforms += forms
                if not krdData == []:
                    Krdantas += krdData
                    numpages += len(krdData)
                    analysisResult[word]['कृदंतः'] = []
                    for krdDetail in krdData:
                        syntaxInputFile.append(
                            [i + 1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 2,
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.erb),
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.sabda),
                             krdDetail.det,
                             krdDetail.vibvach + 1, krdDetail.ddet, krdDetail.Dno,
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.verb),
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.nijverb),
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.sanverb),
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.meaning), ('%03d' % krdDetail.GPICode),
                             krdDetail.CombinedM, krdDetail.karmaCode])
                        wids += 1
                        dic = {}
                        for key, val in zip(['धातुः','धात्वर्य:','णिजि धातु:','सनि धातु:','गण:','पदिः','कर्मः','इट्','धातुविधः','कृदंतविधः','प्रत्ययः','अंतः','लिंगः','प्रातिपदिकं','रूपं'],
                                [krdDetail.verb, krdDetail.meaning, krdDetail.nijverb, krdDetail.sanverb, krdDetail.gana, krdDetail.padi, krdDetail.karma, krdDetail.it,
                                krdDetail.dhatuVidhah, krdDetail.krdantaVidhah, krdDetail.pratyayaVidhah, krdDetail.anta, krdDetail.linga, krdDetail.sabda, krdforms[0][0]],): dic[key] = val
                        analysisResult[word]['कृदंतः'].append({'keyvaluepairs': dic, 'forms':forms})
            except Exception as e:
                logging.debug(e)
            try:
                forms, tigDatas = Kosha_Subanta_Krdanta_Tiganta.tiganta_Analysis(word, wanted_script + 1)
                if not forms == []: tigforms += forms
                if not tigDatas == []:
                    Tigantas += tigDatas
                    numpages += len(tigDatas)
                    analysisResult[word]['तिगंतः'] = []
                    for tigData in tigDatas:
                        syntaxInputFile.append([i + 1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 5,
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.base), tigData.Dno,
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.verb),
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.nijverb),
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.sanverb),
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.meaning),
                                                ('%03d' % tigData.GPICode), tigData.pralak, tigData.purvach,
                                                tigData.CombinedM, tigData.karmaCode])
                        wids += 1
                        dic = {}
                        for key, val in zip(['धातुः','धात्वर्य:','णिजि धातु:','सनि धातु:','गण:','पदिः','कर्मः','इट्','धातुविधः','प्रयोगः','लकारः'], [tigData.verb, tigData.base, tigData.nijverb, tigData.sanverb, tigData.gana, tigData.padi, tigData.karma, tigData.it,
                                        tigData.dhatuVidah, tigData.voice, tigData.lakara]): dic[key] = val
                        analysisResult[word]['तिगंतः'].append({'keyvaluepairs': dic, 'forms':forms})
            except Exception as e:
                logging.debug(e)
            analysisResults.append(analysisResult)
        syntaxInputFile = [AmaraKosha_Database_Queries.unicode_iscii('वाक्यम्') + ' -- %s' % AmaraKosha_Database_Queries.unicode_iscii(bas)]
        for line in syntaxInputFile:
            syntaxInputFile.append('%d) ' % line[0] + ' '.join([str(x) for x in line[1:]]))
        syntaxInputFile.append('----------')
    except Exception as e:
        logging.debug(e)
    return analysisResults'''
app = Flask(__name__)
endpoint_prefix = '/Amarakosha/api/v1.0/'
@app.route(endpoint_prefix + 'hello')
def hello_world():
  return 'Hello from Amarakosha Rest Service!'
@app.route(endpoint_prefix + 'Dhatus', methods=['GET'])
@cross_origin()
def get_Amara():
    logging.debug('servicing Amarakosha Synonyms')
    cols, data = AmaraKosha_Database_Queries.tblSelectUnicode('Amara_Words', maxrows=0)
    data = [transliterate_lines(item[1], IndianLanguages[0]) for item in data]
    return jsonify({'Amarakosha Dhatus': data})
@app.route(endpoint_prefix + 'Subantas', methods=['GET'])
@cross_origin()
def get_Subantas():
    logging.debug('servicing Amarakosha Subanta')
    cols, data = AmaraKosha_Database_Queries.tblSelectUnicode('Subanta', maxrows=0)
    data = [transliterate_lines(item[cols.index('Erb')], IndianLanguages[0]) for item in data]
    return jsonify({'Subanta Dhatus': data})
@app.route(endpoint_prefix + 'KrdantaTigantaDhatus', methods=['GET'])
def get_Krdantas():
    logging.debug('servicing Amarakosha Krdanta Tiganta dhatus')
    cols, data = AmaraKosha_Database_Queries.tblSelectUnicode('Sdhatu', maxrows=0)
    data = [transliterate_lines(item[cols.index('Field2')], IndianLanguages[0]) for item in data]
    return jsonify({'KrdantaTigantaDhatus': data})
@app.route(endpoint_prefix + 'SentencesBandarkar', methods=['GET'])
@cross_origin()
def get_SentencesBandarkar():
    logging.debug('servicing get Sentences from Bandarkar')
    return jsonify({'Sentences': loadBandarkar()})
@app.route(endpoint_prefix + 'SentenceAnalysis', methods=['GET'])
@cross_origin()
def get_SentenceAnalysis_1():
    logging.debug('servicing analyse Sentence(1) ' + request.args.get('sentence'))
    return jsonify({'morphologyAnalysis': analysis_1(request.args.get('sentence'))})
'''@app.route(endpoint_prefix + 'SentenceAnalysis2', methods=['GET'])
@cross_origin()
def get_SentenceAnalysis_2():
    logging.debug('servicing analyse Sentence(2) ' + request.args.get('sentence'))
    return jsonify({'morphologyAnalysis': analysis_2(request.args.get('sentence'))})
@app.route(endpoint_prefix + 'SentenceAnalysis3', methods=['GET'])
@cross_origin()
def get_SentenceAnalysis_3():
    logging.debug('servicing analyse Sentence(3) ' + request.args.get('sentence'))
    return jsonify({'morphologyAnalysis': analysis_3(request.args.get('sentence'))}'''
@app.route(endpoint_prefix + 'Dhatu/<string:dhatu>', methods=['GET'])
@cross_origin()
def get_Synonym(dhatu):
    logging.debug('servicing Amarakosha Synonyms for %s'%dhatu)
    Amarasynonyms, KanWord, EngWord, HinWord = Kosha_Subanta_Krdanta_Tiganta.Amarakosha(dhatu)
    return jsonify({'Amarakosha Dhatus': {'Synonyms':Amarasynonyms, 'Kannada': KanWord, 'English': EngWord, 'Hindi': HinWord}})  # , 'Kannada': KanWord
@app.route(endpoint_prefix + 'Subanta/<string:base>', methods=['GET'])
@cross_origin()
def get_Subanta_forms(base):
    logging.debug('servicing Amarakosha Subanta for %s'%base)
    try:
        forms, anta, linga = Kosha_Subanta_Krdanta_Tiganta.subanta_Generation(base, 1)
        displayForms = {}
        vbhaktis = []
        for i, vibhakti in enumerate(Kosha_Subanta_Krdanta_Tiganta.vibhaktis): vbhaktis.append(format('%d.%s'%(i + 1, vibhakti)))
        for triplet, vibhakti in zip(forms, vbhaktis):
            displayForms[vibhakti] = triplet
        return jsonify({'Subantas': {'forms': displayForms, 'anta': anta, 'linga': linga}})
    except Exception as e:
        return jsonify({'Subantas': {'Error': str(e)[1:-1]}})
@app.route(endpoint_prefix + 'KrdantaTigantaDhatu/<string:word>', methods=['GET'])
@cross_origin()
def get_Krdanta_Tiganta_forms(word):
    logging.debug('servicing Amarakosha Krdanta/Tiganta forms for %s'%word)
    arthas, karmas, dhatuNo, data, cols = Kosha_Subanta_Krdanta_Tiganta.tiganta_krdanta_arthas_karmas(word)
    return jsonify({'Arthas Karmas': {'arthas': arthas, 'karmas': karmas, 'dhatu no': dhatuNo, 'dhatus': data}})
@app.route(endpoint_prefix + 'Krdanta/<string:dhatuNo>', methods=['GET'])
@cross_origin()
def get_Krdanta(dhatuNo):
    logging.debug('servicing Amarakosha Krdanta generation for %s'%dhatuNo)
    forms, krd, emptyForms, emptyKrd, dupFormKeys, dupKrdKeys = krdantaGeneration(dhatuNo)
    krdData = {}
    # for dhatuVidah in forms.keys():
    #     for krdantaVidah in f[dhatuVidah].keys():
    #         for krdMode, form in forms[dhatuVidah][krdantaVidah].items():
    #             form = forms[dhatuVidah][krdantaVidah][krdMode]
    for dhatuVidah in krd.keys():
        krdData[dhatuVidah] = {}
        for krdantaVidah in krd[dhatuVidah].keys():
            for krdMode, krdgen in krd[dhatuVidah][krdantaVidah].items():
                krdData[dhatuVidah][krdantaVidah] = [krd.get() for krd in krdgen]
    # logging.debug("forms %s\nkrdData %s\nemptyForms %s\nemptyKrd %s\ndupFormsKrd %s\ndupKeyKrd %s"%(forms, krdData, emptyForms, emptyKrd, dupFormKeys, dupKrdKeys))
    return jsonify({"forms": forms, "krdData": krdData, "emptyForms": emptyForms, "emptyKrd": emptyKrd, "dupFormKeys": dupFormKeys, "dupKrdKeys": dupKrdKeys})
@app.route(endpoint_prefix + 'KrdantaDhatuKrdantaMode', methods=['GET'])
@cross_origin()
def get_DhatuKrdantaVidhaMode():
    word, DhatuVidha, KrdantaVidha, KrdMode = request.args.get('word'), request.args.get('DhatuVidha'), request.args.get('KrdantaVidha'), request.args.get('KrdMode')
    logging.debug('servicing Amarakosha Krdanta generation for word %s DhatuVidha %s KrdantaVidha %s KrdMode %s'%(word, DhatuVidha, KrdantaVidha, KrdMode))
    try:
        arthas, karmas, dhatuNo, dataDhatu, cols = Kosha_Subanta_Krdanta_Tiganta.tiganta_krdanta_arthas_karmas(word)
        forms, krd = Kosha_Subanta_Krdanta_Tiganta.krdanta_Generation(dhatuNo, DhatuVidha, KrdantaVidha, KrdMode)
        krd = [krdI.get() for krdI in krd]
        # logging.debug("forms %s\nkrdData %s" % (forms, krd))
        results = {"forms": forms[:8], "dhatvarya": arthas[0]}
        for k, v in krd[0].items():
            if k in ["anta", "sabda" "linga", "dhatuVidhah", "gana", "karma", "krdantaVidhah", "meaning", "nijverb", "pratyayaVidhah", "sanverb", "verb", "erb", "padi", "gana", "it"]: results[k] = v
        return jsonify({"Krdantas": results})
    except KeyError as e:
        return abort(400, description=e)
@app.route(endpoint_prefix + 'Tiganta/<string:dhatuNo>', methods=['GET'])
@cross_origin()
def get_Tiganta(dhatuNo):
    logging.debug('servicing Amarakosha Tiganta generation for %s'%dhatuNo)
    forms, tig, emptyForms, emptyTig, dupFormKeys, dupTigKeys = tigantaGeneration(dhatuNo)
    tigData = {}
    # for dhatuVidah in forms.keys():
    #     tigData[dhatuVidah] = {}
    #     for voice in forms[dhatuVidah].keys():
    #         for lakara, form in forms[dhatuVidah][voice].items():
    #             tigData[dhatuVidah][voice] = form
    for dhatuVidah in tig.keys():
        tigData[dhatuVidah] = {}
        for voice in tig[dhatuVidah].keys():
            for lakara, tiggen in tig[dhatuVidah][voice].items():
                tigData[dhatuVidah][voice] = [tig.get() for tig in tiggen]
    # logging.debug("forms %s\ntigData %s\nemptyForms %s\nemptyTig %s\ndupFormsTig %s\ndupKeyTig %s"%(forms, tigData, emptyForms, emptyTig, dupFormKeys, dupTigKeys))
    return jsonify({"forms": forms, "tigData": tigData, "emptyForms": emptyForms, "emptyTig": emptyTig, "dupFormKeys": dupFormKeys, "dupTigKeys": dupTigKeys})
@app.route(endpoint_prefix + 'TigantaDhatuVoiceLakara', methods=['GET'])
@cross_origin()
def get_DhatuTigantaVoiceLakara():
    word, DhatuVidha, voice, lakara = request.args.get('word'), request.args.get('DhatuVidha'), request.args.get('voice'), request.args.get('lakara')
    logging.debug('servicing Amarakosha Tiganta generation for word %s DhatuVidha %s voice %s lakara %s'%(word, DhatuVidha, voice, lakara))
    try:
        arthas, karmas, dhatuNo, dataDhatu, cols = Kosha_Subanta_Krdanta_Tiganta.tiganta_krdanta_arthas_karmas(word)
        forms, _ = Kosha_Subanta_Krdanta_Tiganta.tiganta_Generation(dhatuNo, DhatuVidha, voice, lakara)  # tigData always empty
        gana = Kosha_Subanta_Krdanta_Tiganta.Tganas[dataDhatu[0][cols.index('Field9')] // 100 - 1]
        padi = Kosha_Subanta_Krdanta_Tiganta.Tpadis[(dataDhatu[0][cols.index('Field9')] % 100) // 10 - 1]
        it = Kosha_Subanta_Krdanta_Tiganta.Tyits[dataDhatu[0][cols.index('Field9')] % 10 - 1]
        return jsonify({"Tigantas": {"forms": forms, "Dhatvarya": arthas[0], "Nijidhatu": dataDhatu[0][cols.index("Field3")],
                        "Sanidhatu": dataDhatu[0][cols.index("Field4")], "karma": karmas[0], "gana": gana, "padi": padi, "it": it,
                        "dhatuVidha": DhatuVidha, "voice": voice, "lakara": lakara
                        }})
    except KeyError as e:
        return abort(400, description=e)
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)