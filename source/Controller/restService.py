__author__ = 'naras_mg'

# libraries
import os
from flask import Flask, jsonify, abort, request  # make_response,
import networkx as nx, logging  # json,
from networkx.readwrite import json_graph
from flask_cors import CORS, cross_origin

import sys
sys.path.insert(1, os.getcwd())
from source.Controller import Kosha_Subanta_Krdanta_Tiganta, SyntaxAnalysis
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
def loadBandarkar(script='devanagari'):
    filename = os.path.join('Bandarkar.txt')
    with open(filename, "r", encoding="iso-8859-1") as f:
        dataIscii = [line[:-1] for line in f]
    data = [Kosha_Subanta_Krdanta_Tiganta.transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(item), script) for item in dataIscii]
    return data
def analysis(base, script):
    try:
        subforms, tigforms, krdforms = [], [], []
        Subantas, Krdantas, Tigantas = [], [], []
        syntaxInputFile, bas = [], transliterate_lines(base, 'devanagari').strip()
        numpages, wanted_script = 0, IndianLanguages.index(script)
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
        syntaxInput = [AmaraKosha_Database_Queries.unicode_iscii('वाक्यम्') + ' -- %s' % AmaraKosha_Database_Queries.unicode_iscii(bas)]
        for line in syntaxInputFile:
            syntaxInput.append('%d) ' % line[0] + ' '.join([str(x) for x in line[1:]]))
        syntaxInput.append('----------')
        synt = syntaxAnalysis(syntaxInput)
    except Exception as e:
        logging.debug(e)
    subDatas = []
    for vals in Subantas:
        keys = [transliterate_lines(key, script) for key in ['रूपं', 'प्रातिपदिकं', 'अंतः', 'लिंगः', 'विभक्तिः', 'वचनः']]
        subDat = {}
        for key, val in zip(keys, vals): subDat[key] = val
        subDatas.append(subDat)
    krdDatas = []
    for krdData in Krdantas:
        keys = [transliterate_lines(key, script) for key in ['धातुः','धात्वर्य:','णिजि धातु:','सनि धातु:','गण:','पदिः','कर्मः','इट्','धातुविधः','कृदंतविधः','प्रत्ययः','अंतः','लिंगः','प्रातिपदिकं','रूपं']]
        vals = [krdData.verb, krdData.meaning, krdData.nijverb, krdData.sanverb, krdData.gana, krdData.padi, krdData.karma, krdData.it,  krdData.dhatuVidhah, krdData.krdantaVidhah, krdData.pratyayaVidhah, krdData.anta, krdData.linga, krdData.sabda, krdforms[0][0]]
        krdDat = {}
        for key, val in zip(keys, vals): krdDat[key] = val
        krdDatas.append(krdDat)
    tigDatas = []
    for tigData in Tigantas:
        keys = [transliterate_lines(key, script) for key in ['धातुः','धात्वर्य:','णिजि धातु:','सनि धातु:','गण:','पदिः','कर्मः','इट्','धातुविधः','प्रयोगः','लकारः']]
        vals = [tigData.verb, tigData.base,tigData.nijverb, tigData.sanverb, tigData.gana,tigData.padi, tigData.karma, tigData.it, tigData.dhatuVidah, tigData.voice, tigData.lakara]
        tigDat = {}
        for key, val in zip(keys, vals): tigDat[key] = transliterate_lines(val, script)
        tigDatas.append(tigDat)
    morph = {'सुबंतः': subDatas, 'सुबंतःForms': subforms, 'कृदंतःForms': krdforms, 'तिगंतःForms': tigforms, 'कृदंतः':krdDatas, 'तिगंतः': tigDatas}
    interpretations, graphs = interpret(synt, script)
    # for i, graph in enumerate(graphs): json.dump(json_graph.node_link_data(graph), open('jsondata/amarakosha-force-' + str(i) + '.json', 'w'))
    return {'morphological': morph, 'syntactic': {'interpretations': interpretations, 'graphs': [json_graph.node_link_data(graph) for graph in graphs]}}
def syntaxAnalysis(SyntaxInputFile):
    out = SyntaxAnalysis.write_out_aci(SyntaxInputFile)
    result = SyntaxAnalysis.write_result_aci(out)
    return result
def interpret(result, script='davanagari'):
    typeList = ['Noun(s)', 'Pronoun(s)', 'Adjective(s)', 'Krdanta(s)', 'KrdAvyaya(s)', 'Avyaya(s)']
    subtypeList = ['Subject(s)', 'Object(s)', 'Instrument(s)', 'Dative(s)', 'Ablative(s)', 'Genitive(s)', 'Locative(s)',
                   'Vocative(s)', 'Verb(s)', 'Verb']
    edges, set_edge_labels = {}, []
    conclusions, sentence_no = [{'cells': [], 'conclusions': []}], 0
    graphs = []
    for line_no, line in enumerate(result):
        line = line.replace('\t', '').replace('\n', '').strip()
        words = line.split(' ')
        word = words[0]
        if word == AmaraKosha_Database_Queries.unicode_iscii( 'वाक्यम्'): sentence = AmaraKosha_Database_Queries.iscii_unicode(line[line.index(' -- ') + 4:line.index(' (')])
        if word in [AmaraKosha_Database_Queries.unicode_iscii('वाक्यम्'), ""] or ( len(words) == 1 and word == "subject"): pass
        elif word == "The" or "VOICE" in words or "Considering the verb" in line: conclusions[sentence_no]['conclusions'].append(line)
        elif any([phrase in line for phrase in ["can be assumed to be the", "Any subanta"]]):
            cell = transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(line), script)
            edges['Subject(s)'] = [cell.split()[0], '', '', '']
            conclusions[sentence_no]['conclusions'].append(cell)
        elif 'Noun(s) are:' in line:
            conclusions[sentence_no]['cells'].append(['Noun(s)'] + [''] * 4)
            conclusions[sentence_no]['conclusions'].append('Blah')
        elif 'Noun(s) are:' in result[line_no - 1]:
            parts = line.split(',')
            cell = [transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(w), script)
                    for w in ['word', word, parts[0][:-1], parts[1].strip(), parts[2].strip()]]
            conclusions[sentence_no]['cells'].append(cell)
            # conclusions[sentence_no]['cells'].append(['?'] + ['']*4)
        elif any([phrase in line for phrase in ["Verb is", "No matching subject is available", "Considering krdanta", "There is an object"]]):
            conclusions[sentence_no]['conclusions'].append(line)
        elif word in typeList:
            if len(words) <= 1: parts = ''
            else: parts = line[line.index(' ( ') + 2:].split(' / ')
            if parts == '': conclusions[sentence_no]['cells'].append([transliterate_lines(word, script), '', '', '', ''])
            else:
                cell = [transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(w), script)
                        for w in [word, words[2], parts[0], parts[1], parts[2][:-2]]]
                cellDevanagari = [AmaraKosha_Database_Queries.iscii_unicode(w) for w in
                                  [word, words[2], parts[0], parts[1], parts[2][:-2]]]
                conclusions[sentence_no]['cells'].append(cell)
                w = line[:line.index(' ( ')].split(' : ')[1]
                edges[word] = transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(w), IndianLanguages[0])
                edges[word] = [edges[word]] + [transliterate_lines(word, IndianLanguages[0]) for word in
                                               cellDevanagari[1:]]
        elif word in subtypeList or 'Verb(s) are : ' in result[line_no - 1]:
            parts = line[line.index(' ( ') + 2:].split(' / ')
            if 'Verb(s) are : ' in result[line_no - 1]: word = 'Verb(s)'
            cell = [transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(w), script) for w in
                    [word, words[2], parts[0], parts[1], parts[2][:-2]]]
            cellDevanagari = [AmaraKosha_Database_Queries.iscii_unicode(w) for w in
                              [word, words[2], parts[0], parts[1], parts[2][:-2]]]
            w = line[line.index(' '):line.index(' ( ')]
            if w[0] == ':': w = w[1:]
            edges[word] = transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(w), script)
            edges[word] = [edges[word]] + [transliterate_lines(word, IndianLanguages[0]) for word in cellDevanagari[1:]]
            conclusions[sentence_no]['cells'].append(cell)
        elif word[0] == '-':
            conclusions.append({'cells': [], 'conclusions': []})
            sentence_no += 1
            if 'Verb' in edges.keys():
                graph, edge_labels = karakaGraph(edges)
                if edge_labels not in set_edge_labels:
                    set_edge_labels.append(edge_labels)
                    graphs.append(graph)
            edges = {}
        else: raise NameError(line + '-' + word + ' -> Invalid Category')
    conclusions = [item for item in conclusions if not (item['cells'] == [] and item['conclusions'] == [])]
    return conclusions, graphs
def karakaGraph(interpretation):
    g = nx.Graph()
    edge_labels = {}
    for k, v in interpretation.items():
        if v[0] != '':
            g.add_node(v[0])
            if k != 'Verb': g.nodes[v[0]]['role'], g.nodes[v[0]]['linga'], g.nodes[v[0]]['vibhakti'], g.nodes[v[0]]['vacana'] = k, v[2], v[3], v[-1]
            else:  g.nodes[v[0]]['role'], g.nodes[v[0]]['purusha'], g.nodes[v[0]]['vacana'] = k, v[3], v[4]
    for k, v in interpretation.items():
        if k != 'Verb':
            g.add_edge(interpretation['Verb'][0], interpretation[k][0])
            g[interpretation['Verb'][0]][interpretation[k][0]]['key'] = k
            edge_labels[(interpretation['Verb'][0], interpretation[k][0])] = k
    return g, edge_labels

app = Flask(__name__)
endpoint_prefix = '/Amarakosha/api/v1.0/'
@app.route(endpoint_prefix + 'hello')
def hello_world():
  return 'Hello from Amarakosha Rest Service!'
@app.route(endpoint_prefix + 'Dhatus', methods=['GET'])
@cross_origin()
def get_Amara():
    logging.debug('servicing Amarakosha Synonyms')
    script = request.args.get('script', 'devanagari')
    cols, data = AmaraKosha_Database_Queries.tblSelectUnicode('Amara_Words', maxrows=0)
    data = [transliterate_lines(item[1], script) for item in data]
    return jsonify({'Amarakosha Dhatus': data})
@app.route(endpoint_prefix + 'Subantas', methods=['GET'])
@cross_origin()
def get_Subantas():
    logging.debug('servicing Amarakosha Subanta')
    script = request.args.get('script', 'devanagari')
    cols, data = AmaraKosha_Database_Queries.tblSelectUnicode('Subanta', maxrows=0)
    data = [transliterate_lines(item[cols.index('Erb')], script) for item in data]
    return jsonify({'Subanta Dhatus': data})
@app.route(endpoint_prefix + 'KrdantaTigantaDhatus', methods=['GET'])
def get_KrdantasTigantas():
    logging.debug('servicing Amarakosha Krdanta Tiganta dhatus')
    script = request.args.get('script', 'devanagari')
    scriptIndex = IndianLanguages.index(script) + 1
    cols, data = AmaraKosha_Database_Queries.tblSelectUnicode('Sdhatu', maxrows=0)
    data = [transliterate_lines(item[cols.index('Field2')], script) for item in data]
    return jsonify({'KrdantaTigantaDhatus': data})
@app.route(endpoint_prefix + 'SentencesBandarkar', methods=['GET'])
@cross_origin()
def get_SentencesBandarkar():
    logging.debug('servicing get Sentences from Bandarkar')
    script = request.args.get('script', 'devanagari')
    return jsonify({'Sentences': loadBandarkar(script)})
@app.route(endpoint_prefix + 'SentenceAnalysis', methods=['GET'])
@cross_origin()
def get_SentenceAnalysis():
    logging.debug('servicing analyse Sentence ' + request.args.get('sentence'))
    sentence, script = request.args.get('sentence'), request.args.get('script', 'devanagari')
    return jsonify({'sentenceAnalysis': analysis(sentence, script)})

@app.route(endpoint_prefix + 'Dhatu/<string:dhatu>', methods=['GET'])
@cross_origin()
def get_Synonym(dhatu):
    logging.debug('servicing Amarakosha Synonyms for %s'%dhatu)
    script = request.args.get('script', 'devanagari')
    Amarasynonyms, KanWord, EngWord, HinWord = Kosha_Subanta_Krdanta_Tiganta.Amarakosha(transliterate_lines(dhatu, 'devanagari'), requested_script=IndianLanguages.index(script) + 1)
    return jsonify({'Amarakosha Dhatus': {'Synonyms':Amarasynonyms, 'Kannada': KanWord, 'English': EngWord, 'Hindi': HinWord}})  # , 'Kannada': KanWord
@app.route(endpoint_prefix + 'Subanta/<string:dhatu>', methods=['GET'])
@cross_origin()
def get_Subanta_forms(dhatu):
    logging.debug('servicing Amarakosha Subanta for %s' % dhatu)
    try:
        dhatu = transliterate_lines(dhatu, IndianLanguages[0])
        script = request.args.get('script', 'devanagari')
        scriptIndex = IndianLanguages.index(script) + 1
        forms, anta, linga = Kosha_Subanta_Krdanta_Tiganta.subanta_Generation(dhatu, scriptIndex)
        displayForms = {}
        vbhaktis = []
        for i, vibhakti in enumerate(Kosha_Subanta_Krdanta_Tiganta.vibhaktis):
            vbhaktis.append(format('%d.%s'%(i + 1, transliterate_lines(vibhakti, script))))
        for triplet, vibhakti in zip(forms, vbhaktis):
            displayForms[vibhakti] = triplet
        return jsonify({'Subantas': {'forms': displayForms, transliterate_lines("अंत", script): anta, transliterate_lines("लिंग", script): linga}})
    except Exception as e:
        return jsonify({'Subantas': {'Error': str(e)[1:-1]}})
@app.route(endpoint_prefix + 'KrdantaTigantaDhatu/<string:dhatu>', methods=['GET'])
@cross_origin()
def get_Krdanta_Tiganta_forms(dhatu):
    logging.debug('servicing Amarakosha Krdanta/Tiganta forms for %s' % dhatu)
    try:
        dhatu = transliterate_lines(dhatu, IndianLanguages[0])
        script = request.args.get('script', 'devanagari')
        scriptIndex = IndianLanguages.index(script) + 1
        arthas, karmas, dhatuNo, data, cols = Kosha_Subanta_Krdanta_Tiganta.tiganta_krdanta_arthas_karmas(dhatu, scriptIndex)
        return jsonify({'Arthas Karmas': {'arthas': arthas, 'karmas': karmas, 'dhatu no': dhatuNo, 'dhatus': data}})
    except Exception as e:
        return jsonify({'Krdantas_Tigantas': {'Error': str(e)[1:-1]}})
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
def get_DhatuKrdantaVidhaModeSortedList():
    dhatu, DhatuVidha, KrdantaVidha, KrdMode, script = request.args.get('dhatu'), request.args.get('DhatuVidha'),\
        request.args.get('KrdantaVidha'), request.args.get('KrdMode'), request.args.get('script', 'devanagari')
    logging.debug('servicing Amarakosha Krdanta sorted list for dhatu %s DhatuVidha %s KrdantaVidha %s KrdMode %s'%(dhatu, DhatuVidha, KrdantaVidha, KrdMode))
    try:
        dhatu = transliterate_lines(dhatu, 'devanagari')
        scriptIndex = IndianLanguages.index(script) + 1
        dhatu, DhatuVidha, KrdantaVidha, KrdMode = transliterate_lines(dhatu, 'devanagari'), transliterate_lines(DhatuVidha, 'devanagari'), transliterate_lines(KrdantaVidha, 'devanagari'), transliterate_lines(KrdMode, 'devanagari'),
        arthas, karmas, dhatuNo, dataDhatu, cols = Kosha_Subanta_Krdanta_Tiganta.tiganta_krdanta_arthas_karmas(dhatu, requested_script=scriptIndex)
        forms, krd = Kosha_Subanta_Krdanta_Tiganta.krdanta_Generation(dhatuNo, DhatuVidha, KrdantaVidha, KrdMode, requested_script=scriptIndex)
        krd = [krdI.get() for krdI in krd]
        results = {"forms": forms[:8], transliterate_lines("धात्वार्य", script): ','.join(arthas)}
        labels = {"anta":"अंत", "sabda":"शब्द", "linga":"लिंग", "dhatuVidhah":"धातुविदा", "karma":"कर्म", "krdantaVidhah":"कृदंतविधा", "meaning":"अर्थ",
                  "nijverb":"निजिधातु", "pratyayaVidhah":"प्रत्ययविधा", "sanverb":"शनिधातु", "verb":"धातु", "erb":"रूप", "gana":"गण", "padi":"पदि", "it":"इट्"}
        for k, v in krd[0].items():
            if k in ["anta", "sabda" "linga", "dhatuVidhah", "krdantaVidhah", "meaning", "nijverb", "pratyayaVidhah", "sanverb", "verb", "erb", "padi", "gana", "karma", "it"]:
                results[transliterate_lines(labels[k], script)] = v
        for k in labels.keys(): krd[0].pop(k)
        return jsonify({"Krdantas": results})
    except KeyError as e:
        return abort(400, description=e)
@app.route(endpoint_prefix + 'KrdantaOptionGanaPadiKarmaIt', methods=['GET'])
@cross_origin()
def get_DhatuKrdantaOptionGanaPadiKarmaIt():
    dhatu, option, parameter, DhatuVidha, KrdantaVidha, KrdMode, script = request.args.get('dhatu'),  request.args.get('option'), request.args.get('parameter'), \
        request.args.get('DhatuVidha'), request.args.get('KrdantaVidha'), request.args.get('KrdMode'), request.args.get('script', 'devanagari')
    logging.debug('servicing Amarakosha Krdanta options गण/पदि/कर्म/इट् for dhatu %s option %s parameter %s DhatuVidha %s KrdantaVidha %s KrdMode %s'%(dhatu, option, parameter, DhatuVidha, KrdantaVidha, KrdMode))
    try:
        scriptIndex = IndianLanguages.index(script) + 1
        options = ['गण', 'पदि', 'कर्म', 'इट्']
        dhatu, option, parameter, DhatuVidha, KrdantaVidha, KrdMode = transliterate_lines(dhatu, 'devanagari'), transliterate_lines(option, 'devanagari'), transliterate_lines(parameter, 'devanagari'), transliterate_lines(DhatuVidha, 'devanagari'), transliterate_lines(KrdantaVidha, 'devanagari'), transliterate_lines(KrdMode, 'devanagari'),
        validParameters = [Kosha_Subanta_Krdanta_Tiganta.Tganas, Kosha_Subanta_Krdanta_Tiganta.Tpadis,
                           Kosha_Subanta_Krdanta_Tiganta.Tkarmas, Kosha_Subanta_Krdanta_Tiganta.Tyits][options.index(option)]
        if option not in options: raise SyntaxError("invalid option - has to be one of गण, पदि, कर्म, or इट्")
        if parameter not in validParameters: raise SyntaxError('invalid parameter - must be one of ' + ' / '.join(validParameters))
        func = [Kosha_Subanta_Krdanta_Tiganta.krdanta_Gana, Kosha_Subanta_Krdanta_Tiganta.krdanta_Padi,
                Kosha_Subanta_Krdanta_Tiganta.krdanta_Karma, Kosha_Subanta_Krdanta_Tiganta.krdanta_It][options.index(option)]
        arthas, karmas, dhatuNo, dataDhatu, cols = func(parameter, requested_script=scriptIndex)
        forms, krdData = Kosha_Subanta_Krdanta_Tiganta.krdanta_Generation(dhatuNo, DhatuVidha, KrdantaVidha, KrdMode, requested_script=scriptIndex)
        if option == 'गण': gana = transliterate_lines(parameter, script)
        else: gana = transliterate_lines(Kosha_Subanta_Krdanta_Tiganta.Tganas[dataDhatu[0][cols.index('Field9')] // 100 - 1], script)
        if option == 'पदि': padi = transliterate_lines(parameter, script)
        else: padi = transliterate_lines(Kosha_Subanta_Krdanta_Tiganta.Tpadis[(dataDhatu[0][cols.index('Field9')] % 100) // 10 - 1], script)
        if option == 'इट्': it = transliterate_lines(parameter, script)
        else: it = transliterate_lines(Kosha_Subanta_Krdanta_Tiganta.Tyits[dataDhatu[0][cols.index('Field9')] % 10 - 1], script)
        karma = ','.join(karmas)
        # if option == 'कर्म': karma = parameter
        return jsonify({"Krdantas": {"forms": forms[:8], transliterate_lines("धात्वर्य", script): ','.join(arthas),
                        transliterate_lines("निजिधातु", script): krdData[0].nijverb,
                        transliterate_lines("शनिधातु", script): krdData[0].sanverb, transliterate_lines("कर्म", script): karma,
                         transliterate_lines("गण", script): gana, transliterate_lines("पदि", script): padi,
                         transliterate_lines("इट्", script): it, transliterate_lines("धातुविदा", script): krdData[0].dhatuVidhah,
                         transliterate_lines("कृदंतविधा", script): krdData[0].krdantaVidhah, transliterate_lines("प्रत्यय", script): krdData[0].pratyayaVidhah,
                         transliterate_lines("शब्द", script): krdData[0].sabda, transliterate_lines("अंत", script): krdData[0].anta,
                         transliterate_lines("लिंग", script): krdData[0].linga, transliterate_lines("रूप", script): forms[0][0]
                        }})
    except KeyError as e:
        return abort(400, description=e)
    except SyntaxError as e:
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
@app.route(endpoint_prefix + 'TigantaArthasSortedList', methods=['GET'])
@cross_origin()
def get_DhatuTigantaArthasSortedList():
    word, script = request.args.get('word'), request.args.get('script', 'devanagari')
    logging.debug('servicing Amarakosha Tiganta arthas Sorted List(अकारादि) for word %s'%word)
    try:
        arthas, _, _, _, _ = Kosha_Subanta_Krdanta_Tiganta.tiganta_krdanta_arthas_karmas(transliterate_lines(word, 'devanagari'), requested_script=IndianLanguages.index(script)+1)
        return jsonify({"Tigantas": {"arthas": arthas}})
    except KeyError as e:
        return abort(400, description=e)
@app.route(endpoint_prefix + 'TigantaOptionGanaPadiKarmaIt', methods=['GET'])
@cross_origin()
def get_DhatuTigantaArthasOptionGanaPadiKarmaIt():
    dhatu, option, parameter, DhatuVidha, voice, lakara, script = request.args.get('dhatu'), request.args.get('option'), request.args.get('parameter'),\
        request.args.get('DhatuVidha'), request.args.get('voice'), request.args.get('lakara'), request.args.get('script', 'devanagari')
    logging.debug('servicing Amarakosha Tiganta arthas गण/पदि/कर्म/इट् for dhatu %s option %s parameter %s DhatuVidha %s voice %s lakara %s'%(dhatu, option, parameter, DhatuVidha, voice, lakara))
    try:
        options = ['गण', 'पदि', 'कर्म', 'इट्']
        dhatu, option, parameter, DhatuVidha, voice, lakara = transliterate_lines(dhatu, 'devanagari'), transliterate_lines(option, 'devanagari'), transliterate_lines(parameter, 'devanagari'), transliterate_lines(DhatuVidha, 'devanagari'), transliterate_lines(voice, 'devanagari'), transliterate_lines(lakara, 'devanagari'),
        if option not in options: raise SyntaxError("invalid option - has to be one of गण, पदि, कर्म, or इट्")
        validParameters = [Kosha_Subanta_Krdanta_Tiganta.Tganas, Kosha_Subanta_Krdanta_Tiganta.Tpadis,
                           Kosha_Subanta_Krdanta_Tiganta.Tkarmas, Kosha_Subanta_Krdanta_Tiganta.Tyits][options.index(option)]
        if parameter not in validParameters: raise SyntaxError('invalid parameter - must be one of ' + ' / '.join(validParameters))
        func = [Kosha_Subanta_Krdanta_Tiganta.krdanta_Gana, Kosha_Subanta_Krdanta_Tiganta.krdanta_Padi,
                Kosha_Subanta_Krdanta_Tiganta.krdanta_Karma, Kosha_Subanta_Krdanta_Tiganta.krdanta_It][options.index(option)]
        arthas, karmas, dhatuNo, dataDhatu, cols = func(parameter, requested_script=IndianLanguages.index(script)+1)
        forms, _ = Kosha_Subanta_Krdanta_Tiganta.tiganta_Generation(dhatuNo, DhatuVidha, voice, lakara, requested_script=IndianLanguages.index(script)+1)  # tigData always empty
        if option == 'गण': gana = transliterate_lines(parameter, script)
        else: gana = transliterate_lines(Kosha_Subanta_Krdanta_Tiganta.Tganas[dataDhatu[0][cols.index('Field9')] // 100 - 1], script)
        if option == 'पदि': padi = transliterate_lines(parameter, script)
        else: padi = transliterate_lines(Kosha_Subanta_Krdanta_Tiganta.Tpadis[(dataDhatu[0][cols.index('Field9')] % 100) // 10 - 1], script)
        if option == 'इट्': it = transliterate_lines(parameter, script)
        else: it = transliterate_lines(Kosha_Subanta_Krdanta_Tiganta.Tyits[dataDhatu[0][cols.index('Field9')] % 10 - 1], script)
        # if option == 'कर्म': karma = parameter
        karma = ','.join(karmas)
        return jsonify({"Tigantas": {"forms": forms, transliterate_lines("धात्वार्य", script): ','.join(arthas),
                         transliterate_lines("णिजिधातु", script): transliterate_lines(dataDhatu[0][cols.index("Field3")], script),
                         transliterate_lines("शनिधातु", script): transliterate_lines(dataDhatu[0][cols.index("Field4")], script),
                         transliterate_lines("कर्म", script): karma, transliterate_lines("गण", script): gana,
                         transliterate_lines("पदि", script): padi, transliterate_lines("इट्", script): it,
                         transliterate_lines("धातुविदा", script): transliterate_lines(DhatuVidha, script),
                         transliterate_lines("प्रयोग", script): transliterate_lines(voice, script),
                         transliterate_lines("लकारा", script): transliterate_lines(lakara, script)
                        }})
    except KeyError as e:
        return abort(400, description=e)
    except SyntaxError as e:
        return abort(400, description=e)
@app.route(endpoint_prefix + 'TigantaDhatuVoiceLakara', methods=['GET'])
@cross_origin()
def get_DhatuTigantaVoiceLakara():
    dhatu, DhatuVidha, voice, lakara, script = request.args.get('dhatu'), request.args.get('DhatuVidha'), request.args.get('voice'), request.args.get('lakara'), request.args.get('script', "devanagari")
    logging.debug('servicing Amarakosha Tiganta generation for word %s DhatuVidha %s voice %s lakara %s'%(dhatu, DhatuVidha, voice, lakara))
    try:
        scriptIndex = IndianLanguages.index(script) + 1
        dhatu = transliterate_lines(dhatu, "devanagari")
        arthas, karmas, dhatuNo, dataDhatu, cols = Kosha_Subanta_Krdanta_Tiganta.tiganta_krdanta_arthas_karmas(dhatu, scriptIndex)
        forms, _ = Kosha_Subanta_Krdanta_Tiganta.tiganta_Generation(dhatuNo, DhatuVidha, voice, lakara, requested_script=scriptIndex)  # tigData always empty
        gana = Kosha_Subanta_Krdanta_Tiganta.Tganas[dataDhatu[0][cols.index('Field9')] // 100 - 1]
        padi = Kosha_Subanta_Krdanta_Tiganta.Tpadis[(dataDhatu[0][cols.index('Field9')] % 100) // 10 - 1]
        it = Kosha_Subanta_Krdanta_Tiganta.Tyits[dataDhatu[0][cols.index('Field9')] % 10 - 1]
        return jsonify({"Tigantas": {"forms": forms, transliterate_lines("धात्वार्य", script): ','.join(arthas),
                         transliterate_lines("णिजिधातु", script): transliterate_lines(dataDhatu[0][cols.index("Field3")], script),
                         transliterate_lines("शनिधातु", script): transliterate_lines(dataDhatu[0][cols.index("Field4")], script),
                         transliterate_lines("कर्म", script): ','.join(karmas),
                         transliterate_lines("गण", script): transliterate_lines(gana, script),
                         transliterate_lines("पदि", script): transliterate_lines(padi, script),
                         transliterate_lines("इट्", script): transliterate_lines(it, script),
                        transliterate_lines("धातुविदा", script): transliterate_lines(DhatuVidha, script),
                         transliterate_lines("प्रयोग", script): transliterate_lines(voice, script),
                         transliterate_lines("लकारा", script): transliterate_lines(lakara, script)
                        }})
    except KeyError as e:
        return abort(400, description=e)
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)