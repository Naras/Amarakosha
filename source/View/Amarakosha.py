import inspect
import sys

import pandas
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QRadioButton, QGridLayout, QGroupBox, QHBoxLayout, QListView

from source.Controller import Kosha_Subanta_Krdanta
from source.Model import AmaraKosha_Subanta_Krdanta_Queries

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
class modelKrdanta(QtCore.QAbstractListModel):
    def __init__(self, *args, data=None, **kwargs):
        super(modelKrdanta, self).__init__(*args, **kwargs)
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
class modelKrdanta_meanings(QtCore.QAbstractListModel):
    def __init__(self, *args, data=None, **kwargs):
        super(modelKrdanta, self).__init__(*args, **kwargs)
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
class modelFinalResults_DataFrame(QtCore.QAbstractTableModel):
    def __init__(self, data=pandas.DataFrame([[]], columns=[], index=[])):
        super(modelFinalResults_DataFrame, self).__init__()
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

class modalDialog_Krdanta(QDialog):
    def __init__(self, parent, krdantaWord):
     super(modalDialog_Krdanta, self).__init__(parent)
     self.listView_meanings = QListView(self)
     self.modelKrdanta_meanings = modelKrdanta_meanings()
     self.listView_meanings.setModel(self.modelKrdanta_meanings)
     self.listView_meanings.setUniformItemSizes(True)
     self.listView_meanings.setMaximumWidth(self.listView_meanings.sizeHintForColumn(0) + 125)
     self.listView_meanings.setMaximumHeight(self.listView_meanings.sizeHintForRow(0) + 35)

     arthas, karmas, dhatuNo = Kosha_Subanta_Krdanta.krdanta_arthas_karmas(krdantaWord)
     self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), arthas))
     # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))

     self.mainLayout = QVBoxLayout(self)
     self.mainLayout.addWidget(self.listView_meanings)
     self.initialGrid()
     self.ok = False
     self.KrdMode = "तव्य"
     self.setLayout(self.mainLayout)
     self.setWindowTitle('कृदंत')
     self.setGeometry(500, 550, 550, 150)
     self.setModal(True)
     self.modelKrdanta_meanings.layoutChanged.emit()
     self.exec_()
    def initialGrid(self):
        self.grid = None
        self.groupBoxDhatuVidha, self.groupBoxKrdantaVidha, self.groupBoxKrdMode, self.groupBoxGanas, \
        self.groupBoxPadis, self.groupBoxKarmas, self.groupBoxIts = None, None, None, None, None, None, None
        self.OptionChosen = None
        self.optSorted = QPushButton('Sorted List', self)
        self.optSorted.setText('Sorted List')
        self.optSorted.setCheckable(True)
        self.optSorted.clicked.connect(self.subOptions)
        self.optGanas = QPushButton('Ganas', self)
        self.optGanas.setText('Ganas')
        self.optGanas.setCheckable(True)
        self.optGanas.clicked.connect(self.subOptions)
        self.optPadis = QPushButton('Padis', self)
        self.optPadis.setText('Padis')
        self.optPadis.setCheckable(True)
        self.optPadis.clicked.connect(self.subOptions)
        self.optKarmas = QPushButton('Karmas', self)
        self.optKarmas.setText('Karmas')
        self.optKarmas.setCheckable(True)
        self.optKarmas.clicked.connect(self.subOptions)
        self.optIts = QPushButton('Its', self)
        self.optIts.setText('Its')
        self.optIts.setCheckable(True)
        self.optIts.clicked.connect(self.subOptions)

        self.buttonLayout = QHBoxLayout(self)
        self.buttonLayout.addWidget(self.optSorted)
        self.buttonLayout.addWidget(self.optGanas)
        self.buttonLayout.addWidget(self.optPadis)
        self.buttonLayout.addWidget(self.optKarmas)
        self.buttonLayout.addWidget(self.optIts)
        self.mainLayout.addLayout(self.buttonLayout)
        # self.mainLayout.addLayout(self.grid)
        okBtn = QPushButton(self)
        okBtn.setText('Ok')
        okBtn.clicked.connect(self.okClicked)
        self.mainLayout.addWidget(okBtn)
    def okClicked(self):
     self.ok = True
     self.close()
    def createOptionGroup(self, group, name, optionCatcher, default=True):
        option = {}
        groupBox = QGroupBox(name)
        grplayout = QVBoxLayout(self)
        for opt in group:
            option[opt] = QRadioButton(self)
            option[opt].setText(opt)
            option[opt].text = opt
            option[opt].toggled.connect(optionCatcher)
            grplayout.addWidget(option[opt])
        if default: option[group[0]].setChecked(True)
        groupBox.setLayout(grplayout)
        return groupBox
    def subOptions(self):
        self.mainOption = self.sender().text()
        try:
            if not self.grid == None:
                for item in [self.groupBoxDhatuVidha, self.groupBoxKrdantaVidha, self.groupBoxKrdMode, self.groupBoxGanas, self.groupBoxPadis, self.groupBoxKarmas, self.groupBoxIts]:
                    if (not item == None) and item.isWidgetType():
                        self.grid.removeWidget(item)
                self.grid.update()
                self.mainLayout.removeItem(self.grid)
                self.groupBoxDhatuVidha, self.groupBoxKrdantaVidha, self.groupBoxKrdMode, self.groupBoxGanas, \
                self.groupBoxPadis, self.groupBoxKarmas, self.groupBoxIts = None, None, None, None, None, None, None
                self.grid == None
            self.grid = QGridLayout(self)
            DhatuVidha = ["केवलकृदन्तः", "णिजन्तः", "सन्नन्तः"]
            self.groupBoxDhatuVidha = self.createOptionGroup(DhatuVidha, 'धातुविदाः', self.optionDhatuVidha)

            KrdVidha = ["विध्यर्थः", "भूतः", "वर्तमानः", "भविष्यत्", "कृदव्ययम्"]
            self.groupBoxKrdantaVidha = self.createOptionGroup(KrdVidha, 'कृदंतविधाः', self.optionKrdantaVidha)

            pratvidha = ["तव्य", "अनीयर्", "य", "क्त", "क्तवतु", "शतृ", "शानच्", "स्यशतृ", "स्यशानच्", "तुमुन्", "क्त्वा"]
            self.groupBoxKrdMode = self.createOptionGroup(pratvidha, 'Krdanta Mode', self.optionKrdMode)
            self.KrdMode = "तव्य"
            self.grid.addWidget(self.groupBoxKrdantaVidha, 2, 1)
            self.grid.addWidget(self.groupBoxDhatuVidha, 2, 2)
            self.grid.addWidget(self.groupBoxKrdMode, 2, 3)

            if self.mainOption == 'Ganas':
                Ganas = ["भ्वादिगणः", "अदादिगणः", "जुहोत्यादिगणः", "दिवादिगणः", "स्वादिगणः", "तुदादिगणः", "रुधादिगणः",
                         "तनादिगणः", "क्रयादिगणः", "चुरादिगणः"]
                self.groupBoxGanas = self.createOptionGroup(Ganas, 'गनाः', self.optionGanas)
                self.grid.addWidget(self.groupBoxGanas, 2, 0)
            elif self.mainOption == 'Padis':
                Padis = ["परस्मैपदी", "आत्मनेपदी", "उभयपदी"]
                self.groupBoxPadis = self.createOptionGroup(Padis, 'पदिः', self.optionPadis)
                self.grid.addWidget(self.groupBoxPadis, 2, 0)
            elif self.mainOption == 'Its':
                Karmas = ["सकर्मकः", "अकर्मकः", "द्विकर्मकः"]
                self.groupBoxKarmas = self.createOptionGroup(Karmas, 'कर्माः', self.optionKarmas)
                self.grid.addWidget(self.groupBoxKarmas, 2, 0)
            elif self.mainOption == 'Its':
                Its = ["सेट्‌", "अनिट्‌", "वेट्‌"]
                self.groupBoxIts = self.createOptionGroup(Its, 'कर्माः', self.optionIts)
                self.grid.addWidget(self.groupBoxIts, 2, 0)
            self.mainLayout.addLayout(self.grid)
            self.grid.update()

        except Exception as e:
            print('Exception subOptions: ' % e)
    def optionDhatuVidha(self):
     if self.sender().isChecked():
        self.DhatuVidah = self.sender().text
    def optionKrdantaVidha(self):
     if self.sender().isChecked():
        self.KrdantaVidah = self.sender().text
    def optionKrdMode(self):
     if self.sender().isChecked():
        self.KrdMode = self.sender().text
    def optionGanas(self):
     if self.sender().isChecked():
        self.Ganas = self.sender().text
    def optionPadis(self):
     if self.sender().isChecked():
        self.Padis = self.sender().text
    def optionKarmas(self):
     if self.sender().isChecked():
        self.Karmas = self.sender().text
    def optionIts(self):
     if self.sender().isChecked():
        self.Its = self.sender().text

class modelKrdanta_meanings(QtCore.QAbstractListModel):
    def __init__(self, *args, data=None, **kwargs):
        super(modelKrdanta_meanings, self).__init__(*args, **kwargs)
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

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.listView.setUniformItemSizes(True)
        self.listView.setMaximumWidth(self.listView.sizeHintForColumn(0) + 125)
        self.modelAmara = modelAmara()
        self.modelSubanta = modelSubanta()
        self.modelKrdanta = modelKrdanta()
        self.menuItemChosen = None
        self.modelFinalResults = modelFinalResults_DataFrame()
        self.synonymView.setModel(self.modelFinalResults)
        self.synonymsButton.pressed.connect(self.findSynonyms)

        self.formWidget_2.setVisible(False)
        self.formWidget_4.setVisible(False)
        self.formWidget_5.setVisible(False)
        self.synonymView.setVisible(False)

        self.page1Button.pressed.connect(self.displayPage)
        self.page2Button.pressed.connect(self.displayPage)
        self.page3Button.pressed.connect(self.displayPage)

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

        self.toolbar = self.addToolBar('Krdanta')
        krdantaAction = QtWidgets.QAction('कृदंत(Krdanta)', self)
        krdantaAction.setShortcut('Ctrl+ಖ')
        krdantaAction.triggered.connect(self.loadKrdanta)
        self.toolbar.addAction(krdantaAction)

        self.toolbar = self.addToolBar('Exit')
        exitAction = QtWidgets.QAction('निर्गमनम्(Exit)', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtWidgets.qApp.quit)
        self.toolbar.addAction(exitAction)

        self.statusBar().showMessage('Ready')

    def loadAmara(self):
        self.menuItemChosen = 'Amara'
        cols, data = AmaraKosha_Subanta_Krdanta_Queries.tblSelect('Amara_Words', maxrows=0)
        self.modelAmara.data = list(map(lambda item: (False,item[2]), data))
        self.modelAmara.dataIscii = list(map(lambda item: (False,item[3]), data))
        self.listView.setModel(self.modelAmara)
        self.modelAmara.layoutChanged.emit()
        self.listView.clicked.connect(self.enableSynonymsButton)
        self.synonymsButton.setText('पर्यायशब्द(Synonyms)')
        self.synonymsButton.setEnabled(False)
    def enableSynonymsButton(self):
        self.synonymsButton.setEnabled(True)
    def loadSubanta(self):
        self.menuItemChosen = 'Subanta'
        cols, data = AmaraKosha_Subanta_Krdanta_Queries.tblSelect('Subanta', maxrows=0)
        self.modelSubanta.data = list(map(lambda item: (False, item[2]), data))
        self.modelSubanta.dataIscii = list(map(lambda item: (False,item[3]), data))
        self.listView.setModel(self.modelSubanta)
        self.modelAmara.layoutChanged.emit()
        self.listView.clicked.connect(self.enableSynonymsButton)
        self.synonymsButton.setText('Subanta Generation')
        self.synonymsButton.setEnabled(False)
    def loadKrdanta(self):
        self.menuItemChosen = 'Krdanta'
        # qry = 'select * from Sdhatu where field9 like ?'
        param = '_2_'
        qry = 'select * from Sdhatu'
        param = None
        try:
            cols, data = AmaraKosha_Subanta_Krdanta_Queries.sqlQuery(qry, param, maxrows=0)
            # print('%s\n%s'%(cols, data))
            self.modelKrdanta.data = list(map(lambda item: (False, item[4]), data))
            self.modelKrdanta.dataIscii = list(map(lambda item: (False,item[5]), data))
            self.listView.setModel(self.modelKrdanta)
            self.modelAmara.layoutChanged.emit()
            self.listView.clicked.connect(self.enableSynonymsButton)
            self.synonymsButton.setText('Krdanta Generation')
            self.synonymsButton.setEnabled(False)
        except Exception as e:
            print(e)
    def findSynonyms(self):
        # global krdData
        if self.menuItemChosen == 'Amara':
            self.formWidget_2.setVisible(False)
            self.formWidget_4.setVisible(False)
            self.formWidget_5.setVisible(True)
            self.synonymView.setVisible(True)
            indexes = self.listView.selectedIndexes()
            if indexes:
                index = indexes[0]
                row = index.row()
                try:
                    status, amaraWord = self.modelAmara.dataIscii[row]
                    synonyms, KanWord, EngWord, HinWord = Kosha_Subanta_Krdanta.Amarakosha(amaraWord)
                    text = list(map(lambda i : i or '', KanWord))
                    text = [item for item in text if not item=='']
                    self.kannadaEdit.setText('\n'.join(text))
                    self.autoResize(self.kannadaEdit)
                    text = list(map(lambda i : i or '', EngWord))
                    text = [item for item in text if not item=='']
                    self.englishEdit.setText('\n'.join(text))
                    self.autoResize(self.englishEdit)
                    text = list(map(lambda i : i or '', HinWord))
                    text = [item for item in text if not item=='']
                    self.hindiEdit.setText('\n'.join(text))
                    self.autoResize(self.hindiEdit)
                    self.modelFinalResults._data = pandas.DataFrame(synonyms)
                    self.modelFinalResults.layoutChanged.emit()
                except Exception as e:
                    print(e)
        elif self.menuItemChosen == 'Subanta':
            self.formWidget_2.setVisible(False)
            self.formWidget_4.setVisible(True)
            self.formWidget_5.setVisible(False)
            self.synonymView.setVisible(True)
            indexes = self.listView.selectedIndexes()
            if indexes:
                index = indexes[0]
                row = index.row()
                status, base = self.modelSubanta.dataIscii[row]
                try:
                    forms, vacanas, vibhaktis, anta, linga = Kosha_Subanta_Krdanta.Subanta(base)
                    self.antaLineEdit.setText(AmaraKosha_Subanta_Krdanta_Queries.iscii_unicode(anta))
                    self.lingaLineEdit.setText(AmaraKosha_Subanta_Krdanta_Queries.iscii_unicode(linga))
                    self.modelFinalResults._data = pandas.DataFrame(forms, columns=vacanas, index=vibhaktis)
                    self.modelFinalResults.layoutChanged.emit()
                except Exception as e:
                    print(e)
        elif self.menuItemChosen == 'Krdanta':
            self.formWidget_4.setVisible(False)
            self.formWidget_5.setVisible(False)
            try:
                indexes = self.listView.selectedIndexes()
                if indexes:
                    index = indexes[0]
                    row = index.row()
                    status, krdantaWord = self.modelKrdanta.dataIscii[row]
                dialog = modalDialog_Krdanta(self, krdantaWord)
                # print('%s DhatuVidha %s KrdantaVidha %s Krdanta Mode %s'%(dialog.ok, dialog.DhatuVidah, dialog.KrdantaVidah, dialog.KrdMode))
                if dialog.okClicked:
                        if dialog.mainOption == 'Sorted List':
                            self.arthas, self.karmas, dhatuNo = Kosha_Subanta_Krdanta.krdanta_arthas_karmas(krdantaWord)
                            forms, vacanas, vibhaktis, self.krdData = Kosha_Subanta_Krdanta.Krdanta_SortedList(dhatuNo, dialog.DhatuVidah, dialog.KrdantaVidah,
                                                                                                 dialog.KrdMode)
                            self.setTexts(zip([self.txtDhatu, self.txtKrdanta, self.txtPratyaya, self.txtLinga],
                            [self.krdData[0].dhatuVidhah, self.krdData[0].krdantaVidhah, self.krdData[0].pratyayaVidhah, self.krdData[0].linga]))

                            self.page1Button.setEnabled(True)
                            self.page1Button.setVisible(True)
                            self.page2Button.setEnabled(True)
                            self.page2Button.setVisible(True)
                            self.page3Button.setEnabled(True)
                            self.page3Button.setVisible(True)
                        elif dialog.mainOption == 'Ganas':
                            forms, vacanas, vibhaktis = Kosha_Subanta_Krdanta.Krdanta_Ganas(krdantaWord, dialog.DhatuVidah, dialog.KrdantaVidah,
                                                                                                 dialog.KrdMode, dialog.Ganas)
                        elif dialog.mainOption == 'Padis':
                            forms, vacanas, vibhaktis = Kosha_Subanta_Krdanta.Krdanta_Padis(krdantaWord, dialog.DhatuVidah, dialog.KrdantaVidah,
                                                                                                 dialog.KrdMode, dialog.Padis)
                        elif dialog.mainOption == 'Karmas':
                            forms, vacanas, vibhaktis = Kosha_Subanta_Krdanta.Krdanta_Karmas(krdantaWord, dialog.DhatuVidah, dialog.KrdantaVidah,
                                                                                                 dialog.KrdMode, dialog.Karmas)
                        elif dialog.mainOption == 'Its':
                            forms, vacanas, vibhaktis = Kosha_Subanta_Krdanta.Krdanta_Its(krdantaWord, dialog.DhatuVidah, dialog.KrdantaVidah,
                                                                                                 dialog.KrdMode, dialog.Its)
                        # print(krdData)
                        self.modelFinalResults._data = pandas.DataFrame(forms, columns=vacanas, index=vibhaktis)
                        self.modelFinalResults.layoutChanged.emit()
                        self.formWidget_2.setVisible(True)
                        self.synonymView.setVisible(True)
            except Exception as e:
                        print(e)
        else: raise NameError('Invalid Category')
    def autoResize(self, text):
        font = text.document().defaultFont()
        # font.setPointSize(10)
        fontMetrics = QFontMetrics(font)
        textSize = fontMetrics.size(0, text.toPlainText())

        w = textSize.width() + 10
        h = textSize.height() + 10
        text.setMinimumSize(w, h)
        text.setMaximumSize(w, h)
        text.resize(w, h)
        text.setReadOnly(True)
    def setTexts(self, zipLists):
        for txt, value in zipLists: txt.setText(value)
    def displayPage(self):
        try:
            if self.sender().objectName() == 'page1Button':
                self.setTexts(zip([self.txtDhatu, self.txtKrdanta, self.txtPratyaya, self.txtLinga],
                                  [self.krdData[0].dhatuVidhah, self.krdData[0].krdantaVidhah, self.krdData[0].pratyayaVidhah, self.krdData[0].linga]))
            elif self.sender().objectName() == 'page2Button':
                  self.setTexts(zip([self.txtDhatu, self.txtKrdanta, self.txtPratyaya, self.txtLinga],
                                  [self.krdData[1].dhatuVidhah, self.krdData[1].krdantaVidhah, self.krdData[1].pratyayaVidhah, self.krdData[1].linga]))
            else: self.setTexts(zip([self.txtDhatu, self.txtKrdanta, self.txtPratyaya, self.txtLinga],
                    [self.krdData[2].dhatuVidhah, self.krdData[2].krdantaVidhah, self.krdData[2].pratyayaVidhah, self.krdData[2].linga]))
        except Exception as e:
            print(e)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
