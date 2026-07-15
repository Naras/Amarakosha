#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest, random

from source.Controller import MorphologicalAnalysis as Kosha_Subanta_Krdanta_Tiganta, SyntaxAnalysis
from source.Controller.Transliterate import transliterate_lines, IndianLanguages
from source.Model import AmaraKosha_Database_Queries
import os, sys
sys.path.append(os.getcwd())


def morphological_syntactic_analysis_exception_givers(sentence):
    numpages, subforms, krdforms, tigforms, Subantas, Krdantas, Tigantas = 0, [], [], [], [], [], []
    syntaxInputFile = []
    for i, word in enumerate(sentence.split(' ')):
        wids = 1
        try:
            forms, subDetails = Kosha_Subanta_Krdanta_Tiganta.subanta_Analysis(word)
            if not forms == []: subforms += forms
            for item in subDetails:
                numpages += 1
                Subantas.append([item.rupam, transliterate_lines(item.base,"devanagari"),
                                 item.anta, item.linga, item.vib, item.vach, item.vibvach])
                syntaxInputFile.append([i + 1, word, wids, 1, AmaraKosha_Database_Queries.unicode_iscii(item.base),
                                        AmaraKosha_Database_Queries.unicode_iscii(item.erb), item.det,
                                        item.vibvach + 1])
                wids += 1
        except Exception as e:
            pass  # Word is not a subanta
        try:
            forms, krdData = Kosha_Subanta_Krdanta_Tiganta.krdanta_Analysis(word)
            if not forms == []: krdforms += forms
            if not krdData == []:
                Krdantas += krdData
                numpages += len(krdData)
                for krdDetail in krdData:
                    syntaxInputFile.append(
                        [i + 1, word, wids, 2, AmaraKosha_Database_Queries.unicode_iscii(krdDetail.erb),
                         AmaraKosha_Database_Queries.unicode_iscii(krdDetail.sabda), krdDetail.det,
                         krdDetail.vibvach + 1, krdDetail.ddet, krdDetail.Dno,
                         AmaraKosha_Database_Queries.unicode_iscii(krdDetail.verb),
                         AmaraKosha_Database_Queries.unicode_iscii(krdDetail.nijverb),
                         AmaraKosha_Database_Queries.unicode_iscii(krdDetail.sanverb),
                         AmaraKosha_Database_Queries.unicode_iscii(krdDetail.meaning), krdDetail.GPICode,
                         krdDetail.CombinedM,
                         krdDetail.karmaCode])
                    wids += 1
        except Exception as e:
            pass  # Word is not a krdanta
        try:
            forms, tigDatas = Kosha_Subanta_Krdanta_Tiganta.tiganta_Analysis(word)
            if not forms == []: tigforms += forms
            if not tigDatas == []:
                Tigantas += tigDatas
                numpages += len(tigDatas)
                for tigData in tigDatas:
                    syntaxInputFile.append(
                        [i + 1, word, wids, 5, AmaraKosha_Database_Queries.unicode_iscii(tigData.base), tigData.Dno,
                         AmaraKosha_Database_Queries.unicode_iscii(tigData.verb),
                         AmaraKosha_Database_Queries.unicode_iscii(tigData.nijverb),
                         AmaraKosha_Database_Queries.unicode_iscii(tigData.sanverb),
                         AmaraKosha_Database_Queries.unicode_iscii(tigData.meaning), tigData.GPICode,
                         tigData.pralak, tigData.purvach, tigData.CombinedM, tigData.karmaCode])
                    wids += 1
        except Exception as e:
            pass  # Word is not a tiganta
    morphologicalOutput = [AmaraKosha_Database_Queries.unicode_iscii('वाक्यम्') + ' -- %s' % AmaraKosha_Database_Queries.unicode_iscii(sentence)]
    for line in syntaxInputFile: morphologicalOutput.append('%d) ' % line[0] + ' '.join([str(x) for x in line[1:]]))
    morphologicalOutput.append('----------')
    out = SyntaxAnalysis.write_out_aci(morphologicalOutput)
    result = SyntaxAnalysis.write_result_aci(out)
    return out, result

class Test(unittest.TestCase):
    def test_morphological_syntactic_analysis_exception_giving_sentences(self):
        sentences = ['कमलानि पश्यति', 'रामः पूजयति', 'व्याधयः नश्यन्ति', 'अरिः पीडयति', 'नृपः जयति', 'धनं नश्यति', 'वारीणि शुष्यन्ति ','नाविकाः नदेन समुद्रं प्रविशन्ति', 'बुधः मोक्षं इच्छति',
                     'रामः कपिभिः जयति रावणम्', 'वारिणा हस्तौ क्षालयति', 'कमले नृत्यत', 'नृपः जयति', 'जनाः वदन्ति', 'स्तेनः धान्यं चॊरयति', 'मनुष्यः ग्रामाय गच्छति', 'सुन्दरः रामः पश्यति']
        for sentence in sentences:
            self.morphological_syntactic_analysis_exception_givers_assert(sentence.strip())

    def morphological_syntactic_analysis_exception_givers_print(self, sentence):
        outExpected, resultExpected = {}, {}
        try:
            out, result = morphological_syntactic_analysis_exception_givers(sentence)
            outExpected[sentence.strip()]  = [AmaraKosha_Database_Queries.iscii_unicode(str(l)) for l in out]
            resultExpected[sentence.strip()] = [AmaraKosha_Database_Queries.iscii_unicode(str(l)) for l in result]
        except Exception as e:
            print(f'morphological_syntactic_analysis_exception_giving_sentence-print: sentence {sentence}\nout={out}\nresult = {result} Exception {e}')

        print(f'test_morphological_syntactic_analysis_exception_giving_sentences: outExpected = {outExpected}')
        print(f'test_morphological_syntactic_analysis_exception_giving_sentences: resultExpected = {resultExpected}')

    def morphological_syntactic_analysis_exception_givers_assert(self, sentence):
        out, result = morphological_syntactic_analysis_exception_givers(sentence)
        self.assertIsNotNone(result, f"Null result for sentence: {sentence}")

    def test_morphological_syntactic_analysis_more_sentences(self):
        filename = os.path.join('Bandarkar.txt')
        with open(filename, "r", encoding="iso-8859-1") as f:
            dataIscii = [line for line in f]
            data = [AmaraKosha_Database_Queries.iscii_unicode(item) for item in dataIscii]
        self.morphological_analysis(random.choice(data))
    def morphological_analysis(self, sentence):
        numpages, subforms, krdforms, tigforms, Subantas, Krdantas, Tigantas, syntaxInputFile = 0, [], [], [], [], [], [], []
        for i, word in enumerate(sentence.split(' ')):
            word = AmaraKosha_Database_Queries.unicode_iscii(word)
            try:
                wids = 1
                forms, subDetails = Kosha_Subanta_Krdanta_Tiganta.subanta_Analysis(word)
                if not forms == []: subforms += forms
                for item in subDetails:
                    numpages += 1
                    Subantas.append([item.rupam, item.base, item.anta, item.linga, item.vib, item.vach, item.vibvach])
                    syntaxInputFile.append([i + 1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 1, AmaraKosha_Database_Queries.unicode_iscii(item.base), AmaraKosha_Database_Queries.unicode_iscii(item.erb), item.det, item.vibvach + 1])
                    wids += 1
            except Exception as e:
                print(e)
            try:
                forms, krdData = Kosha_Subanta_Krdanta_Tiganta.krdanta_Analysis(word)
                if not forms == []: krdforms += forms
                if not krdData == []:
                    Krdantas += krdData
                    numpages += len(krdData)
                    for krdDetail in krdData:
                        syntaxInputFile.append(  [i + 1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 2, AmaraKosha_Database_Queries.unicode_iscii(krdDetail.erb), AmaraKosha_Database_Queries.unicode_iscii(krdDetail.sabda), krdDetail.det,
                             krdDetail.vibvach + 1, krdDetail.ddet, krdDetail.Dno, AmaraKosha_Database_Queries.unicode_iscii(krdDetail.verb), AmaraKosha_Database_Queries.unicode_iscii(krdDetail.nijverb),
                             AmaraKosha_Database_Queries.unicode_iscii(krdDetail.sanverb), AmaraKosha_Database_Queries.unicode_iscii(krdDetail.meaning), krdDetail.GPICode, krdDetail.CombinedM, krdDetail.karmaCode])
                        wids += 1
            except Exception as e:
                print(e)
            try:
                forms, tigDatas = Kosha_Subanta_Krdanta_Tiganta.tiganta_Analysis(word)
                if not forms == []: tigforms += forms
                if not tigDatas == []:
                    Tigantas += tigDatas
                    numpages += len(tigDatas)
                    for tigData in tigDatas:
                        # ic.ic('tiganta', i+1, word, wids)
                        syntaxInputFile.append( [i + 1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 5, AmaraKosha_Database_Queries.unicode_iscii(tigData.base), tigData.Dno, AmaraKosha_Database_Queries.unicode_iscii(tigData.verb),
                                                AmaraKosha_Database_Queries.unicode_iscii(tigData.nijverb), AmaraKosha_Database_Queries.unicode_iscii(tigData.sanverb), AmaraKosha_Database_Queries.unicode_iscii(tigData.meaning), tigData.GPICode,
                                                tigData.pralak, tigData.purvach, tigData.CombinedM, tigData.karmaCode])
                        wids += 1
            except Exception as e:
                print(e)
        morphologicalOutput = [AmaraKosha_Database_Queries.unicode_iscii('वाक्यम्') + ' -- %s' % AmaraKosha_Database_Queries.unicode_iscii(sentence)]
        for line in syntaxInputFile:
            morphologicalOutput.append('%d) ' % line[0] + ' '.join([str(x) for x in line[1:]]))
        morphologicalOutput.append('----------')
        print(f'sentence = {sentence}\nnumpages = {numpages}\nsubforms = {subforms}\nkrdforms = {krdforms}\ntigforms = {tigforms}\nSubantas = {Subantas}\nKrdantas = {[item.get() for item in Krdantas]}\nTigantas = {[item.get() for item in Tigantas]}\nmorphologicalOutput = {morphologicalOutput}')
            # [AmaraKosha_Database_Queries.iscii_unicode(line) for line in morphologicalOutput])

        try:
            out = SyntaxAnalysis.write_out_aci(morphologicalOutput)
            result = SyntaxAnalysis.write_result_aci(out)
            print(f'{sentence}  ಸರಿಯಾಗಿದೆ!\nout = {[AmaraKosha_Database_Queries.iscii_unicode(line) for line in out]}\nresult = {[AmaraKosha_Database_Queries.iscii_unicode(line) for line in result]}')
        except Exception as e:
            print(f'sentence {sentence} Exception {e}')