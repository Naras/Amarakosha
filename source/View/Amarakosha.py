import sys

import pandas
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics

from source.Controller import Sandhi_Convt, Kosha_Subanta
from source.Model import Kosha_Subanta_Synonyms_Queries

qt_creator_file = "amara_uiComposition.xml"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)
tick = QtGui.QImage('tick.png')

class modelAmara(QtCore.QAbstractListModel):
    def __init__(self, *args, data=None, **kwargs):
        super(modelAmara, self).__init__(*args, **kwargs)
        self.data = data or []
        self.dataIscii= []
    def data(self, index, role):
        if role == Qt.DisplayRole:
            _, text = self.data[index.row()]
            return text
        if role == Qt.DecorationRole:
            status, _ = self.data[index.row()]
            if status:
                return tick
    def rowCount(self, index):
        return len(self.data)
class modelSubanta(QtCore.QAbstractListModel):
    def __init__(self, *args, data=None, **kwargs):
        super(modelSubanta, self).__init__(*args, **kwargs)
        self.data = data or []
        self.dataIscii = []
    def data(self, index, role):
        if role == Qt.DisplayRole:
            _, text = self.data[index.row()]
            return text
        if role == Qt.DecorationRole:
            status, _ = self.data[index.row()]
            if status:
                return tick
    def rowCount(self, index):
        return len(self.data)
class modelJanani_DataFrame(QtCore.QAbstractTableModel):

    def __init__(self, data=pandas.DataFrame([[]], columns=[], index=[])):
        super(modelJanani_DataFrame, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.lbl1.setVisible(False)
        self.lbl2.setVisible(False)
        self.lbl3.setVisible(False)
        self.txt1.setVisible(False)
        self.txt2.setVisible(False)
        self.txt3.setVisible(False)

        self.listView.setUniformItemSizes(True)
        self.listView.setMaximumWidth(self.listView.sizeHintForColumn(0) + 125)
        self.modelAmara = modelAmara()
        self.modelSubanta = modelSubanta()
        self.menuItemChosen = None
        self.modelJanani = modelJanani_DataFrame()
        self.synonymView.setModel(self.modelJanani)
        self.synonymsButton.pressed.connect(self.findSynonyms)
        # self.loadAmara()
        # self.listView.setModel(self.modelAmara)

        # self.amaraMenu = self.Amara.addMenu('&Amara')
        # self.amaraMenu = self.Amara.addMenu('E&xit')

        self.toolbar = self.addToolBar('Amara')
        amaraAction = QtWidgets.QAction('अमरकोश(Amarakosha)', self)
        amaraAction.setShortcut('Ctrl+A')
        amaraAction.triggered.connect(self.loadAmara)
        self.toolbar.addAction(amaraAction)

        self.toolbar = self.addToolBar('Subanta')
        subantaAction = QtWidgets.QAction('सुबंत(Subanta)', self)
        subantaAction.setShortcut('Ctrl+S')
        subantaAction.triggered.connect(self.loadSubanta)
        self.toolbar.addAction(subantaAction)

        self.toolbar = self.addToolBar('Exit')
        exitAction = QtWidgets.QAction('निर्गमनम्(Exit)', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtWidgets.qApp.quit)
        self.toolbar.addAction(exitAction)

        self.statusBar().showMessage('Ready')

    def loadAmara(self):
        self.menuItemChosen = 'Amara'
        self.lbl1.setText('ಕನ್ನಡ')
        self.lbl2.setText('English')
        self.lbl3.setText('हिंदि')
        cols, data = Kosha_Subanta_Synonyms_Queries.tblSelect('Amara_Words', maxrows=0)
        self.modelAmara.data = list(map(lambda item: (False,item[2]), data))
        self.modelAmara.dataIscii = list(map(lambda item: (False,item[3]), data))
        self.listView.setModel(self.modelAmara)
        self.modelAmara.layoutChanged.emit()
    def loadSubanta(self):
        self.menuItemChosen = 'Subanta'
        self.lbl1.setText('अंत')
        self.lbl2.setText('लिंग')
        self.lbl1.setVisible(True)
        self.lbl2.setVisible(True)
        self.lbl3.setVisible(False)
        self.txt1.setVisible(False)
        self.txt2.setVisible(False)
        self.txt3.setVisible(False)
        cols, data = Kosha_Subanta_Synonyms_Queries.tblSelect('Subanta', maxrows=0)
        self.modelSubanta.data = list(map(lambda item: (False, item[2]), data))
        self.modelSubanta.dataIscii = list(map(lambda item: (False,item[3]), data))
        self.listView.setModel(self.modelSubanta)
        self.modelAmara.layoutChanged.emit()
    def findSynonyms(self):
        if self.menuItemChosen == 'Amara':
            self.txt1.setVisible(True)
            self.txt2.setVisible(True)
            self.txt3.setVisible(True)
            self.lbl1.setVisible(True)
            self.lbl2.setVisible(True)
            self.lbl3.setVisible(True)
            indexes = self.listView.selectedIndexes()
            if indexes:
                index = indexes[0]
                row = index.row()
                try:
                    status, amaraWord = self.modelAmara.dataIscii[row]
                    synonyms, KanWord, EngWord, HinWord = Kosha_Subanta.Amarakosha(amaraWord)
                    text = list(map(lambda i : i or '', KanWord))
                    text = [item for item in text if not item=='']
                    self.txt1.setText('\n'.join(text))
                    self.autoResize(self.txt1)
                    text = list(map(lambda i : i or '', EngWord))
                    text = [item for item in text if not item=='']
                    self.txt2.setText('\n'.join(text))
                    self.autoResize(self.txt2)
                    text = list(map(lambda i : i or '', HinWord))
                    text = [item for item in text if not item=='']
                    self.txt3.setText('\n'.join(text))
                    self.autoResize(self.txt3)
                    # self.txt2.resize(400,40)
                    self.modelJanani._data = pandas.DataFrame(synonyms)
                    self.modelJanani.layoutChanged.emit()
                except Exception as e:
                    print(e)
        elif self.menuItemChosen == 'Subanta':
            self.txt1.setVisible(False)
            self.txt2.setVisible(False)
            self.txt3.setVisible(False)
            self.lbl1.setVisible(True)
            self.lbl2.setVisible(True)
            self.lbl3.setVisible(False)
            indexes = self.listView.selectedIndexes()
            if indexes:
                index = indexes[0]
                row = index.row()
                status, base = self.modelSubanta.dataIscii[row]
                try:
                    forms, vacanas, vibhaktis, anta, linga = Kosha_Subanta.Subanta(base)
                    self.lbl1.setText(Kosha_Subanta_Synonyms_Queries.iscii_unicode(anta))
                    self.lbl2.setText(Kosha_Subanta_Synonyms_Queries.iscii_unicode(linga))
                    self.modelJanani._data = pandas.DataFrame(forms, columns=vacanas, index=vibhaktis)
                    self.modelJanani.layoutChanged.emit()
                except Exception as e:
                    print(e)
        else: raise NameError('Invalid Category')

    def autoResize(self, text):
        font = text.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        textSize = fontMetrics.size(0, text.toPlainText())

        w = textSize.width() + 10
        h = textSize.height() + 10
        text.setMinimumSize(w, h)
        text.setMaximumSize(w, h)
        text.resize(w, h)
        text.setReadOnly(True)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
