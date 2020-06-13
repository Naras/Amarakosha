import inspect
import sys

import pandas
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QRadioButton, QGridLayout, QGroupBox, QHBoxLayout, QListView

from source.Controller import Kosha_Subanta_Krdanta
from source.Model import AmaraKosha_Subanta_Krdanta_Queries, models

qt_creator_file = "amara_uiComposition.xml"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

class modalDialog_Krdanta(QDialog):
    def __init__(self, parent, krdantaWord):
     super(modalDialog_Krdanta, self).__init__(parent)
     self.krdantaWord = krdantaWord
     self.mainLayout = QVBoxLayout(self)
     self.initialGrid()
     self.KrdMode = "तव्य"
     self.setLayout(self.mainLayout)
     self.setWindowTitle('कृदंत')
     self.setGeometry(500, 550, 550, 150)
     self.setModal(True)
     self.exec_()
    def initialGrid(self):
        self.grid = None
        self.groupBoxDhatuVidha, self.groupBoxKrdantaVidha, self.groupBoxKrdMode, self.groupBoxGanas, \
        self.groupBoxPadis, self.groupBoxKarmas, self.groupBoxIts = None, None, None, None, None, None, None
        self.OptionChosen = None
        self.optSorted = QPushButton('Sorted List', self)
        self.optSorted.setText('Sorted List')
        self.optSorted.setCheckable(True)
        self.optSorted.clicked.connect(self.optionSortedList)
        self.optGanas = QPushButton('Ganas', self)
        self.optGanas.setText('Ganas')
        self.optGanas.setCheckable(True)
        self.optGanas.clicked.connect(self.optionGanas)
        self.optPadis = QPushButton('Padis', self)
        self.optPadis.setText('Padis')
        self.optPadis.setCheckable(True)
        self.optPadis.clicked.connect(self.optionPadis)
        self.optKarmas = QPushButton('Karmas', self)
        self.optKarmas.setText('Karmas')
        self.optKarmas.setCheckable(True)
        self.optKarmas.clicked.connect(self.optionKarmas)
        self.optIts = QPushButton('Its', self)
        self.optIts.setText('Its')
        self.optIts.setCheckable(True)
        self.optIts.clicked.connect(self.optionIts)

        self.buttonLayout = QHBoxLayout(self)
        self.buttonLayout.addWidget(self.optSorted)
        self.buttonLayout.addWidget(self.optGanas)
        self.buttonLayout.addWidget(self.optPadis)
        self.buttonLayout.addWidget(self.optKarmas)
        self.buttonLayout.addWidget(self.optIts)
        self.mainLayout.addLayout(self.buttonLayout)
        # self.mainLayout.addLayout(self.grid)
        self.ok_cancel_btnLayout = QHBoxLayout(self)
        self.okBtn = QPushButton(self)
        self.okBtn.setText('Ok')
        self.okBtn.setEnabled(False)
        self.okBtn.clicked.connect(self.okClicked)
        self.ok_cancel_btnLayout.addWidget(self.okBtn)
        self.cancelBtn = QPushButton(self)
        self.cancelBtn.setText('Cancel')
        self.cancelBtn.setEnabled(False)
        self.cancelBtn.clicked.connect(self.cancelClicked)
        self.ok_cancel_btnLayout.addWidget(self.cancelBtn)
        self.mainLayout.addLayout(self.ok_cancel_btnLayout)
        self.okClicked = False
    def okClicked(self):
     self.okClicked = True
     indexes = self.listView_meanings.selectedIndexes()
     if indexes:
         index = indexes[0]
         row = index.row()
         status, self.krdantaWord = self.modelKrdanta_meanings.data[row]
     self.close()
    def cancelClicked(self):
     self.okClicked = False
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
    def removeAllGroups(self):
        if not self.grid == None:
            for item in [self.groupBoxDhatuVidha, self.groupBoxKrdantaVidha, self.groupBoxKrdMode, self.groupBoxGanas,
                         self.groupBoxPadis, self.groupBoxKarmas, self.groupBoxIts]:
                if (not item == None) and item.isWidgetType():
                    self.grid.removeWidget(item)
            self.grid.update()
            self.mainLayout.removeItem(self.grid)
            self.groupBoxDhatuVidha, self.groupBoxKrdantaVidha, self.groupBoxKrdMode, self.groupBoxGanas, \
            self.groupBoxPadis, self.groupBoxKarmas, self.groupBoxIts = None, None, None, None, None, None, None
            self.grid == None
    def addDhatuKrdantaGroups(self):
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
    def optionDhatuVidha(self):
     if self.sender().isChecked():
        self.DhatuVidah = self.sender().text
    def optionKrdantaVidha(self):
     if self.sender().isChecked():
        self.KrdantaVidah = self.sender().text
    def optionKrdMode(self):
     if self.sender().isChecked():
        self.KrdMode = self.sender().text
    def optionSortedList(self):
        self.mainOption = self.sender().text()
        try:
            self.listView_meanings = QListView(self)
            self.modelKrdanta_meanings = models.modelKrdanta_meanings()
            self.listView_meanings.setModel(self.modelKrdanta_meanings)
            self.listView_meanings.setUniformItemSizes(True)
            self.listView_meanings.setMaximumWidth(self.listView_meanings.sizeHintForColumn(0) + 125)
            self.listView_meanings.setMaximumHeight(self.listView_meanings.sizeHintForRow(0) + 35)
            arthas, _, _, _, _ = Kosha_Subanta_Krdanta.krdanta_arthas_karmas(self.krdantaWord)
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            self.mainLayout.addWidget(self.listView_meanings)
            self.modelKrdanta_meanings.layoutChanged.emit()
            self.removeAllGroups()
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
            self.mainLayout.addLayout(self.grid)
            self.grid.update()
            self.okBtn.setEnabled(True)
            self.cancelBtn.setEnabled(True)
        except Exception as e:
            print('Exception Sorted list:%s' % e)
    def optionGanas(self):
        self.mainOption = self.sender().text()
        try:
             if self.sender().isChecked():
                self.removeAllGroups()
                self.grid = QGridLayout(self)
                self.groupBoxGanas = self.createOptionGroup(Kosha_Subanta_Krdanta.Tganas, 'गनाः', self.optionGanaSelected, default=False)
                self.grid.addWidget(self.groupBoxGanas, 2, 0)
                self.mainLayout.addLayout(self.grid)
                self.grid.update()
                self.okBtn.setEnabled(True)
                self.cancelBtn.setEnabled(True)
        except Exception as e:
             print('exception Ganas:%s' % e)
    def optionPadis(self):
        self.mainOption = self.sender().text()
        try:
            if self.sender().isChecked():
                self.removeAllGroups()
                self.grid = QGridLayout(self)
                self.groupBoxPadis = self.createOptionGroup(Kosha_Subanta_Krdanta.Tpadis, 'परस्मैपदी',self.optionPadiSelected, default=False)
                self.grid.addWidget(self.groupBoxPadis, 2, 0)
                self.mainLayout.addLayout(self.grid)
                self.grid.update()
                self.okBtn.setEnabled(True)
                self.cancelBtn.setEnabled(True)
        except Exception as e:
            print('exception Padis:%s' % e)
    def optionKarmas(self):
        self.mainOption = self.sender().text()
        try:
            if self.sender().isChecked():
                self.removeAllGroups()
                self.grid = QGridLayout(self)
                self.groupBoxPadis = self.createOptionGroup(Kosha_Subanta_Krdanta.Tkarmas, 'सकर्मकः',self.optionKarmaSelected, default=False)
                self.grid.addWidget(self.groupBoxPadis, 2, 0)
                self.mainLayout.addLayout(self.grid)
                self.grid.update()
                self.okBtn.setEnabled(True)
                self.cancelBtn.setEnabled(True)
        except Exception as e:
            print('exception Karmas:%s' % e)
    def optionIts(self):
        self.mainOption = self.sender().text()
        try:
            if self.sender().isChecked():
                self.removeAllGroups()
                self.grid = QGridLayout(self)
                self.groupBoxPadis = self.createOptionGroup(Kosha_Subanta_Krdanta.Tyits, 'सेट्',
                                                            self.optionItSelected, default=False)
                self.grid.addWidget(self.groupBoxPadis, 2, 0)
                self.mainLayout.addLayout(self.grid)
                self.grid.update()
                self.okBtn.setEnabled(True)
                self.cancelBtn.setEnabled(True)
        except Exception as e:
            print('exception Its:%s' % e)
    def optionGanaSelected(self):
        if self.sender().isChecked():
            self.gana = self.sender().text
            self.listView_meanings = QListView(self)
            self.modelKrdanta_meanings = models.modelKrdanta_meanings()
            self.listView_meanings.setModel(self.modelKrdanta_meanings)
            self.listView_meanings.setUniformItemSizes(True)
            self.listView_meanings.setMaximumWidth(self.listView_meanings.sizeHintForColumn(0) + 125)
            # self.listView_meanings.setMaximumHeight(self.listView_meanings.sizeHintForRow(0) + 35)
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta.krdanta_Gana(self.gana)
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), self.arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            self.mainLayout.addWidget(self.listView_meanings)
            self.modelKrdanta_meanings.layoutChanged.emit()

            DhatuVidha = ["केवलकृदन्तः", "णिजन्तः", "सन्नन्तः"]
            self.groupBoxDhatuVidha = self.createOptionGroup(DhatuVidha, 'धातुविदाः', self.optionDhatuVidha)
            KrdVidha = ["विध्यर्थः", "भूतः", "वर्तमानः", "भविष्यत्", "कृदव्ययम्"]
            self.groupBoxKrdantaVidha = self.createOptionGroup(KrdVidha, 'कृदंतविधाः', self.optionKrdantaVidha)
            pratvidha = ["तव्य", "अनीयर्", "य", "क्त", "क्तवतु", "शतृ", "शानच्", "स्यशतृ", "स्यशानच्", "तुमुन्","क्त्वा"]
            self.groupBoxKrdMode = self.createOptionGroup(pratvidha, 'Krdanta Mode', self.optionKrdMode)
            self.grid.addWidget(self.groupBoxKrdantaVidha, 2, 1)
            self.grid.addWidget(self.groupBoxDhatuVidha, 2, 2)
            self.grid.addWidget(self.groupBoxKrdMode, 2, 3)
            self.mainLayout.addLayout(self.grid)
            self.grid.update()
            self.okBtn.setEnabled(True)
            self.cancelBtn.setEnabled(True)
    def optionPadiSelected(self):
        if self.sender().isChecked():
            self.padi = self.sender().text
            self.listView_meanings = QListView(self)
            self.modelKrdanta_meanings = models.modelKrdanta_meanings()
            self.listView_meanings.setModel(self.modelKrdanta_meanings)
            self.listView_meanings.setUniformItemSizes(True)
            self.listView_meanings.setMaximumWidth(self.listView_meanings.sizeHintForColumn(0) + 125)
            # self.listView_meanings.setMaximumHeight(self.listView_meanings.sizeHintForRow(0) + 35)
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta.krdanta_Padi(self.padi)
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), self.arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            self.mainLayout.addWidget(self.listView_meanings)
            self.modelKrdanta_meanings.layoutChanged.emit()

            DhatuVidha = ["केवलकृदन्तः", "णिजन्तः", "सन्नन्तः"]
            self.groupBoxDhatuVidha = self.createOptionGroup(DhatuVidha, 'धातुविदाः', self.optionDhatuVidha)
            KrdVidha = ["विध्यर्थः", "भूतः", "वर्तमानः", "भविष्यत्", "कृदव्ययम्"]
            self.groupBoxKrdantaVidha = self.createOptionGroup(KrdVidha, 'कृदंतविधाः', self.optionKrdantaVidha)
            pratvidha = ["तव्य", "अनीयर्", "य", "क्त", "क्तवतु", "शतृ", "शानच्", "स्यशतृ", "स्यशानच्", "तुमुन्","क्त्वा"]
            self.groupBoxKrdMode = self.createOptionGroup(pratvidha, 'Krdanta Mode', self.optionKrdMode)
            self.grid.addWidget(self.groupBoxKrdantaVidha, 2, 1)
            self.grid.addWidget(self.groupBoxDhatuVidha, 2, 2)
            self.grid.addWidget(self.groupBoxKrdMode, 2, 3)
            self.mainLayout.addLayout(self.grid)
            self.grid.update()
            self.okBtn.setEnabled(True)
            self.cancelBtn.setEnabled(True)
    def optionKarmaSelected(self):
        if self.sender().isChecked():
            self.karma = self.sender().text
            self.listView_meanings = QListView(self)
            self.modelKrdanta_meanings = models.modelKrdanta_meanings()
            self.listView_meanings.setModel(self.modelKrdanta_meanings)
            self.listView_meanings.setUniformItemSizes(True)
            self.listView_meanings.setMaximumWidth(self.listView_meanings.sizeHintForColumn(0) + 125)
            # self.listView_meanings.setMaximumHeight(self.listView_meanings.sizeHintForRow(0) + 35)
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta.krdanta_Karma(self.karma)
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), self.arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            self.mainLayout.addWidget(self.listView_meanings)
            self.modelKrdanta_meanings.layoutChanged.emit()

            DhatuVidha = ["केवलकृदन्तः", "णिजन्तः", "सन्नन्तः"]
            self.groupBoxDhatuVidha = self.createOptionGroup(DhatuVidha, 'धातुविदाः', self.optionDhatuVidha)
            KrdVidha = ["विध्यर्थः", "भूतः", "वर्तमानः", "भविष्यत्", "कृदव्ययम्"]
            self.groupBoxKrdantaVidha = self.createOptionGroup(KrdVidha, 'कृदंतविधाः', self.optionKrdantaVidha)
            pratvidha = ["तव्य", "अनीयर्", "य", "क्त", "क्तवतु", "शतृ", "शानच्", "स्यशतृ", "स्यशानच्", "तुमुन्","क्त्वा"]
            self.groupBoxKrdMode = self.createOptionGroup(pratvidha, 'Krdanta Mode', self.optionKrdMode)
            self.grid.addWidget(self.groupBoxKrdantaVidha, 2, 1)
            self.grid.addWidget(self.groupBoxDhatuVidha, 2, 2)
            self.grid.addWidget(self.groupBoxKrdMode, 2, 3)
            self.mainLayout.addLayout(self.grid)
            self.grid.update()
            self.okBtn.setEnabled(True)
            self.cancelBtn.setEnabled(True)
    def optionItSelected(self):
        if self.sender().isChecked():
            self.it = self.sender().text
            self.listView_meanings = QListView(self)
            self.modelKrdanta_meanings = models.modelKrdanta_meanings()
            self.listView_meanings.setModel(self.modelKrdanta_meanings)
            self.listView_meanings.setUniformItemSizes(True)
            self.listView_meanings.setMaximumWidth(self.listView_meanings.sizeHintForColumn(0) + 125)
            # self.listView_meanings.setMaximumHeight(self.listView_meanings.sizeHintForRow(0) + 35)
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta.krdanta_It(self.it)
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), self.arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            self.mainLayout.addWidget(self.listView_meanings)
            self.modelKrdanta_meanings.layoutChanged.emit()

            DhatuVidha = ["केवलकृदन्तः", "णिजन्तः", "सन्नन्तः"]
            self.groupBoxDhatuVidha = self.createOptionGroup(DhatuVidha, 'धातुविदाः', self.optionDhatuVidha)
            KrdVidha = ["विध्यर्थः", "भूतः", "वर्तमानः", "भविष्यत्", "कृदव्ययम्"]
            self.groupBoxKrdantaVidha = self.createOptionGroup(KrdVidha, 'कृदंतविधाः', self.optionKrdantaVidha)
            pratvidha = ["तव्य", "अनीयर्", "य", "क्त", "क्तवतु", "शतृ", "शानच्", "स्यशतृ", "स्यशानच्", "तुमुन्","क्त्वा"]
            self.groupBoxKrdMode = self.createOptionGroup(pratvidha, 'Krdanta Mode', self.optionKrdMode)
            self.grid.addWidget(self.groupBoxKrdantaVidha, 2, 1)
            self.grid.addWidget(self.groupBoxDhatuVidha, 2, 2)
            self.grid.addWidget(self.groupBoxKrdMode, 2, 3)
            self.mainLayout.addLayout(self.grid)
            self.grid.update()
            self.okBtn.setEnabled(True)
            self.cancelBtn.setEnabled(True)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.listView.setUniformItemSizes(True)
        self.listView.setMaximumWidth(self.listView.sizeHintForColumn(0) + 125)
        self.modelAmara = models.modelAmara()
        self.modelSubanta = models.modelSubanta()
        self.modelKrdanta = models.modelKrdanta()
        self.menuItemChosen = None
        self.modelFinalResults = models.modelFinalResults_DataFrame()
        self.synonymView.setModel(self.modelFinalResults)
        self.synonymsButton.pressed.connect(self.findSynonyms)

        self.formWidget_2.setVisible(False)
        self.formWidget_4.setVisible(False)
        self.formWidget_5.setVisible(False)
        self.synonymView.setVisible(False)

        self.page1Button.pressed.connect(self.displayPage)
        self.page2Button.pressed.connect(self.displayPage)
        self.page3Button.pressed.connect(self.displayPage)
        self.page4Button.pressed.connect(self.displayPage)
        self.page5Button.pressed.connect(self.displayPage)
        self.page6Button.pressed.connect(self.displayPage)

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
        self.page1Button.setVisible(False)
        self.page2Button.setVisible(False)
        self.page3Button.setVisible(False)
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
        self.page1Button.setVisible(False)
        self.page2Button.setVisible(False)
        self.page3Button.setVisible(False)
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
                            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = \
                                Kosha_Subanta_Krdanta.krdanta_arthas_karmas(krdantaWord)
                            if not dialog.KrdantaVidah == "कृदव्ययम्":
                                self.finalResults(self.dhatuNo, dialog)
                            else:
                                self.krdData = Kosha_Subanta_Krdanta.Krdanta_SortedList_KrDantavyayam(self.dhatuNo, dialog.DhatuVidah, dialog.KrdantaVidah,
                                                                                                 dialog.KrdMode, self.dataDhatu, self.cols_dataDhatu)
                                self.setTexts(zip(
                                    [self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu,
                                     self.txtGana, self.txtPadi, self.txtKarma, self.txtIt, self.txtDhatuVidah,
                                     self.txtKrdantaVidah, self.txtPratyaya, self.txtSabda],
                                    [self.krdData[0].verb, self.arthas[0], self.krdData[0].nijverb,
                                     self.krdData[0].sanverb, self.krdData[0].gana, self.krdData[0].padi,
                                     self.karmas[0], self.krdData[0].it, self.krdData[0].dhatuVidhah,
                                     self.krdData[0].krdantaVidhah, self.krdData[0].pratyayaVidhah,
                                     self.krdData[0].sabda]))
                                self.synonymView.setVisible(False)
                                self.formWidget_2.setVisible(True)
                                self.LabelAnta.setVisible(False)
                                self.txtAnta.setVisible(False)
                                self.LabelLinga.setVisible(False)
                                self.txtLinga.setVisible(False)
                                self.LabelPratipadika.setVisible(False)
                                self.txtPratipadika.setVisible(False)
                                self.LabelSabda.setVisible(True)
                                self.txtSabda.setVisible(True)
                                self.page1Button.setEnabled(False)
                                self.page1Button.setVisible(False)
                                self.page2Button.setEnabled(False)
                                self.page2Button.setVisible(False)
                                self.page3Button.setEnabled(False)
                                self.page3Button.setVisible(False)
                        else:
                            self.arthas, self.karmas = dialog.arthas, dialog.karmas
                            self.finalResults(dialog.dhatuNo, dialog)
                        # elif dialog.mainOption == 'Padis':
                        #     self.arthas, self.karmas = dialog.arthas, dialog.karmas
                        #     self.finalResults(dialog.dhatuNo, dialog)
                        # elif dialog.mainOption == 'Karmas':
                        #     self.arthas, self.karmas = dialog.arthas, dialog.karmas
                        #     self.finalResults(dialog.dhatuNo, dialog)
                        # elif dialog.mainOption == 'Its':
                        #     self.arthas, self.karmas = dialog.arthas, dialog.karmas
                        #     self.finalResults(dialog.dhatuNo, dialog)
                        # print(krdData)
            except Exception as e:
                        print(e)
        else: raise NameError('Invalid Category')
    def autoResize(self, text):
        font = text.document().defaultFont()
        # font.setPointSize(10)
        fontMetrics = QFontMetrics(font)
        textSize = fontMetrics.size(0, text.toPlainText())

        w = textSize.width() + 25
        h = textSize.height() + 25
        text.setMinimumSize(w, h)
        text.setMaximumSize(w, h)
        text.resize(w, h)
        text.setReadOnly(True)
    def setTexts(self, zipLists):
        for txt, value in zipLists: txt.setText(value)
    def displayPage(self):
        try:
            indx = ['page1Button', 'page2Button', 'page3Button', 'page4Button', 'page5Button', 'page6Button'].index(self.sender().objectName())
            self.setTexts(zip([self.txtLinga, self.txtAnta], [self.krdData[indx].linga, self.krdData[indx].anta]))
            self.modelFinalResults._data = pandas.DataFrame(self.forms[indx * 8: indx * 8 + 8], columns=self.vacanas, index=self.vibhaktis)
            self.modelFinalResults.layoutChanged.emit()
        except Exception as e:
            print(e)
    def finalResults(self, dhatuNo, dialog):
        self.forms, self.vacanas, self.vibhaktis, self.krdData = Kosha_Subanta_Krdanta.KrdantaGeneration(dhatuNo,
                                                                                                         dialog.DhatuVidah,
                                                                                                         dialog.KrdantaVidah,
                                                                                                         dialog.KrdMode)
        self.modelFinalResults._data = pandas.DataFrame(self.forms[:8], columns=self.vacanas,
                                                        index=self.vibhaktis)
        self.modelFinalResults.layoutChanged.emit()
        self.setTexts(zip(
            [self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu,
             self.txtGana, self.txtPadi, self.txtKarma, self.txtIt, self.txtDhatuVidah,
             self.txtKrdantaVidah, self.txtPratyaya, self.txtSabda, self.txtAnta, self.txtLinga,
             self.txtPratipadika],
            [self.krdData[0].verb, self.arthas[0], self.krdData[0].nijverb,
             self.krdData[0].sanverb, self.krdData[0].gana, self.krdData[0].padi,
             self.karmas[0], self.krdData[0].it, self.krdData[0].dhatuVidhah,
             self.krdData[0].krdantaVidhah, self.krdData[0].pratyayaVidhah,
             self.krdData[0].sabda, self.krdData[0].anta, self.krdData[0].linga,
             self.krdData[0].sabda]))
        self.formWidget_2.setVisible(True)
        self.synonymView.setVisible(True)
        self.LabelAnta.setVisible(True)
        self.txtAnta.setVisible(True)
        self.LabelLinga.setVisible(True)
        self.txtLinga.setVisible(True)
        self.LabelPratipadika.setVisible(True)
        self.txtPratipadika.setVisible(True)
        self.LabelSabda.setVisible(False)
        self.txtSabda.setVisible(False)
        self.page1Button.setEnabled(True)
        self.page1Button.setVisible(True)
        self.page2Button.setEnabled(True)
        self.page2Button.setVisible(True)
        self.page3Button.setEnabled(True)
        self.page3Button.setVisible(True)
        if len(self.forms) > 24:
            self.page4Button.setEnabled(True)
            self.page4Button.setVisible(True)
            self.page5Button.setEnabled(True)
            self.page5Button.setVisible(True)
            self.page6Button.setEnabled(True)
            self.page6Button.setVisible(True)
        else:
            self.page4Button.setEnabled(False)
            self.page4Button.setVisible(False)
            self.page5Button.setEnabled(False)
            self.page5Button.setVisible(False)
            self.page6Button.setEnabled(False)
            self.page6Button.setVisible(False)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
