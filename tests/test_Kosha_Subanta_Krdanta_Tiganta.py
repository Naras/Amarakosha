import codecs
from unittest import TestCase
# import os, sys
# sys.path.append(os.getcwd())
from source.Model import AmaraKosha_Database_Queries

class Test(TestCase):
    def common(self, tbl, parameterName):
        colsAmara, dataAmara = AmaraKosha_Database_Queries.tblSelect(tbl, maxrows=5, duplicate=False)
        # print('%s\n%s'%(colsAmara, dataAmara))
        for field in dataAmara:
            parameter = field[colsAmara.index(parameterName)]
            cols, data = AmaraKosha_Database_Queries.sqlQuery('Select * from ' + tbl + ' where ' + parameterName + ' = ?',
                                                               AmaraKosha_Database_Queries.unicode_iscii(parameter))
            for line in data:
                self.assertEqual(line[cols.index(parameterName)], parameter)
    def common_with_duplicates(self, tbl, parameterName):
        colsAmara, dataAmara = AmaraKosha_Database_Queries.tblSelect(tbl, maxrows=5)
        # print('%s\n%s'%(colsAmara, dataAmara))
        for field in dataAmara:
            parameter = field[colsAmara.index(parameterName)]
            cols, data = AmaraKosha_Database_Queries.sqlQuery('Select * from ' + tbl + ' where ' + parameterName + ' = ?',
                                                               AmaraKosha_Database_Queries.unicode_iscii(parameter))
            for line in data:
                self.assertEqual(line[cols.index(parameterName) + 1], AmaraKosha_Database_Queries.unicode_iscii(parameter))

    def test_amara(self):
        self.common('Amara_Words', 'Word')
        self.common_with_duplicates('Amara_Words', 'Word')
    def test_janani(self):
        self.common('Janani1', 'Words')
        self.common_with_duplicates('Janani1', 'Words')
    def test_subanta(self):
        self.common('Subanta', 'Base')  # "¤¢ÕÝÌÂÜ")
        self.common_with_duplicates('Subanta', 'Base')
    def test_krdanta_tiganta(self):
        self.common('Sdhatu', 'Field2')
        self.common_with_duplicates('Sdhatu', 'Field8')
        self.common('Sdhatu', 'Field2')
        self.common_with_duplicates('Sdhatu', 'Field8')
        self.common('Sdhatu', 'Field3')
        self.common_with_duplicates('Sdhatu', 'Field3')
        self.common('Sdhatu', 'Field4')
        self.common_with_duplicates('Sdhatu', 'Field4')
    def test_krud(self):
        self.common('KRUD', 'Field1')
        self.common_with_duplicates('KRUD', 'Field1')
    def test_stinfin(self):
        self.common('Stinfin', 'Field1')
        self.common_with_duplicates('Stinfin', 'Field1')
    def test_schema(self):
        tbls = AmaraKosha_Database_Queries.schemaParse()
        self.assertEqual(tbls, ['Amara_Words', 'Avyaya', 'Conversion_Errors', 'Conversion_Errors1', 'FINCODE', 'Janani1', 'Janani2', 'KRUD', 'KRUDAV', 'N_Sanskrit', 'STINNEW', 'SUFCODE', 'Sdhatu', 'Stinfin', 'Stinsuf', 'SubFin', 'Subanta', 'UpaCode', 'Upasarga', 'V_Hindi', 'V_Odiya', 'V_Sanskrit', 'Words_list'])
    def test_largetext(self):
        inp = codecs.open('iscii_source.txt',encoding='utf-8')
        src = inp.readlines()
        for line in src:
            print(AmaraKosha_Database_Queries.iscii_unicode(line[:-2]))
            self.assertEqual(line[:-2], AmaraKosha_Database_Queries.unicode_iscii(AmaraKosha_Database_Queries.iscii_unicode(line[:-2])))
        inp.close()
