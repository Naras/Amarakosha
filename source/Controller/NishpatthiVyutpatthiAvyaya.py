from typing import List
from source.Model import AmaraKosha_Database_Queries

def nishpatthi(amaraWord: str) -> List[str]:
    qry = 'select Nishpatti from N_Sanskrit N, Amara_Words A where N.IdNo = A.ID and A.Word = ?'
    # print('amaraword:', amaraWord)
    cols, dbdata = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param=amaraWord, maxrows=0)
    return dbdata
def vyutpatthi(amaraWord:str, language='Sanskrit') -> List[str]:
    table = ['V_Sanskrit', 'V_Hindi', 'V_Odiya'][['Sanskrit', 'Hindi', 'Odiya'].index(language)]
    qry = 'select Vytpatti from '+ table + ' V, Amara_Words A where V.IdNo = A.ID and A.Word = ?'
    # print('amaraword:', amaraWord)
    cols, dbdata = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param=amaraWord, maxrows=0)
    return dbdata
def avyayaAnalysis(word: str, requested_script="devanagari") -> List[str]:
    qry = 'select * from avyaya where field2=?'
    cols, avySuffix = AmaraKosha_Database_Queries.sqlQueryUnicode(qry, param=word, maxrows=0, script=requested_script)
    avyayas =[]
    for avyaya in avySuffix:
        avyaya.inpword = word
        avyaya.Avycode = avySuffix[cols.index('Field1') + 1]
        avyayas.append(avyaya)
    return avyayas