import sys

import pandas
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
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
        self.lblAnta.setText('')
        self.lblLinga.setText('')
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
        self.lblAnta.setText('')
        self.lblLinga.setText('')
        cols, data = Kosha_Subanta_Synonyms_Queries.tblSelect('Amara_Words', maxrows=0)
        self.modelAmara.data = list(map(lambda item: (False,item[2]), data))
        self.modelAmara.dataIscii = list(map(lambda item: (False,item[3]), data))
        # print(self.modelAmara.dataIscii)
        self.listView.setModel(self.modelAmara)
        self.modelAmara.layoutChanged.emit()
    def loadSubanta(self):
        self.menuItemChosen = 'Subanta'
        self.lblAnta.setText('')
        self.lblLinga.setText('')
        cols, data = Kosha_Subanta_Synonyms_Queries.tblSelect('Subanta', maxrows=0)
        self.modelSubanta.data = list(map(lambda item: (False, item[2]), data))
        self.modelSubanta.dataIscii = list(map(lambda item: (False,item[3]), data))
        self.listView.setModel(self.modelSubanta)
        self.modelAmara.layoutChanged.emit()
    def findSynonyms(self):
        if self.menuItemChosen == 'Amara':
            indexes = self.listView.selectedIndexes()
            if indexes:
                index = indexes[0]
                row = index.row()
                status, amaraWord = self.modelAmara.dataIscii[row]
                synonyms = Kosha_Subanta.Amarakosha(amaraWord)
                try:
                    self.modelJanani._data = pandas.DataFrame(synonyms)
                    self.modelJanani.layoutChanged.emit()
                except Exception as e:
                    print(e)
        elif self.menuItemChosen == 'Subanta':
            indexes = self.listView.selectedIndexes()
            if indexes:
                index = indexes[0]
                row = index.row()
                status, base = self.modelSubanta.dataIscii[row]
                try:
                    forms, vacanas, vibhaktis, anta, linga = Kosha_Subanta.Subanta(base)
                    self.lblAnta.setText(Kosha_Subanta_Synonyms_Queries.iscii_unicode(anta))
                    self.lblLinga.setText(Kosha_Subanta_Synonyms_Queries.iscii_unicode(linga))
                    self.modelJanani._data = pandas.DataFrame(forms, columns=vacanas, index=vibhaktis)
                    self.modelJanani.layoutChanged.emit()
                except Exception as e:
                    print(e)
        else: raise NameError('Invalid Category')


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
