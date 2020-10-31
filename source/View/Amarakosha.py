# import inspect
import logging
import sys

import pandas
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QRadioButton, QGridLayout, QGroupBox, QHBoxLayout, \
    QListView, QFileDialog

from source.Controller import Kosha_Subanta_Krdanta_Tiganta
from source.Controller.Transliterate import *
from source.Model import AmaraKosha_Database_Queries, models

qt_creator_file = "amara_uiComposition.xml"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)
class modalDialog_Krdanta(QDialog):
    def __init__(self, parent, krdantaWord, requested_script):
     super(modalDialog_Krdanta, self).__init__(parent)
     self.script = requested_script
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
            arthas, _, _, _, _ = Kosha_Subanta_Krdanta_Tiganta.krdanta_arthas_karmas(self.krdantaWord, requested_script=self.script)
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
                self.groupBoxGanas = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.Tganas, 'गनाः', self.optionGanaSelected, default=False)
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
                self.groupBoxPadis = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.Tpadis, 'परस्मैपदी', self.optionPadiSelected, default=False)
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
                self.groupBoxPadis = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.Tkarmas, 'सकर्मकः', self.optionKarmaSelected, default=False)
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
                self.groupBoxPadis = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.Tyits, 'सेट्',
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
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta_Tiganta.krdanta_Gana(self.gana)
            self.arthas = [transliterate_lines(item, IndianLanguages[self.script-1]) for item in self.arthas]
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
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta_Tiganta.krdanta_Padi(self.padi)
            self.arthas = [transliterate_lines(item, IndianLanguages[self.script-1]) for item in self.arthas]
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
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta_Tiganta.krdanta_Karma(self.karma)
            self.arthas = [transliterate_lines(item, IndianLanguages[self.script-1]) for item in self.arthas]
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
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta_Tiganta.krdanta_It(self.it)
            self.arthas = [transliterate_lines(item, IndianLanguages[self.script-1]) for item in self.arthas]
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
class modalDialog_Tiganta(QDialog):
    def __init__(self, parent, tigantaWord, requested_script):
     super(modalDialog_Tiganta, self).__init__(parent)
     self.script = requested_script
     self.tigantaWord = tigantaWord
     self.mainLayout = QVBoxLayout(self)
     self.initialGrid()
     self.lakara = "लट्"
     self.setLayout(self.mainLayout)
     self.setWindowTitle('तिङ्ंत')
     self.setGeometry(500, 550, 550, 150)
     self.setModal(True)
     self.exec_()
    def initialGrid(self):
        self.grid = None
        self.groupBoxDhatuVidha, self.groupBoxKrdantaVidha, self.groupBoxKrdMode, self.groupBoxGanas, \
        self.groupBoxPadis, self.groupBoxKarmas, self.groupBoxIts = None, None, None, None, None, None, None
        self.OptionChosen = None
        self.optSorted = QPushButton('Sorted List', self)
        self.optSorted.setText('Sorted List(अकारादि)')
        self.optSorted.setCheckable(True)
        self.optSorted.clicked.connect(self.optionSortedList)
        self.optGanas = QPushButton('Ganas', self)
        self.optGanas.setText('Ganas(गण)')
        self.optGanas.setCheckable(True)
        self.optGanas.clicked.connect(self.optionGanas)
        self.optPadis = QPushButton('Padis', self)
        self.optPadis.setText('Padis(पदि)')
        self.optPadis.setCheckable(True)
        self.optPadis.clicked.connect(self.optionPadis)
        self.optKarmas = QPushButton('Karmas', self)
        self.optKarmas.setText('Karmas(कर्म)')
        self.optKarmas.setCheckable(True)
        self.optKarmas.clicked.connect(self.optionKarmas)
        self.optIts = QPushButton('Its', self)
        self.optIts.setText('Its(इट्)')
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
         status, self.meaning = self.modelKrdanta_meanings.data[row]
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
    def addDhatuTigantaGroups(self):
        DhatuVidha = ["केवलतिगंतः", "णिजन्तः", "सन्नन्तः"]
        self.groupBoxDhatuVidha = self.createOptionGroup(DhatuVidha, 'धातुविदाः', self.optionDhatuVidha)

        KrdVidha = ["कर्तरि", "कर्मणि"]
        self.groupBoxKrdantaVidha = self.createOptionGroup(KrdVidha, 'कृदंतविधाः', self.optionVoice)

        pratvidha = ["लट्", "लिट्", "लुट्", "लृट्", "लोट्", "लङ्", "विधिलिङ्", "अशीर्लिङ्", "लुङ्", "लृङ्"]
        self.groupBoxKrdMode = self.createOptionGroup(pratvidha, 'Krdanta Mode', self.optionLakara)
        self.KrdMode = "तव्य"
        self.grid.addWidget(self.groupBoxKrdantaVidha, 2, 1)
        self.grid.addWidget(self.groupBoxDhatuVidha, 2, 2)
        self.grid.addWidget(self.groupBoxKrdMode, 2, 3)
    def optionDhatuVidha(self):
     if self.sender().isChecked():
        self.DhatuVidah = self.sender().text
    def optionVoice(self):
     if self.sender().isChecked():
        self.voice = self.sender().text
    def optionLakara(self):
     if self.sender().isChecked():
        self.lakara = self.sender().text
    def optionSortedList(self):
        self.mainOption = self.sender().text()
        try:
            self.listView_meanings = QListView(self)
            self.modelKrdanta_meanings = models.modelKrdanta_meanings()
            self.listView_meanings.setModel(self.modelKrdanta_meanings)
            self.listView_meanings.setUniformItemSizes(True)
            self.listView_meanings.setMaximumWidth(self.listView_meanings.sizeHintForColumn(0) + 125)
            self.listView_meanings.setMaximumHeight(self.listView_meanings.sizeHintForRow(0) + 35)
            dhatus, _, _, _, _ = Kosha_Subanta_Krdanta_Tiganta.krdanta_arthas_karmas(self.tigantaWord, requested_script=self.script)
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), dhatus))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            self.mainLayout.addWidget(self.listView_meanings)
            self.modelKrdanta_meanings.layoutChanged.emit()
            self.removeAllGroups()
            self.grid = QGridLayout(self)
            self.DhatuVidha = "केवलतिगंतः"
            self.groupBoxDhatuVidha = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.DhatuVidhasTiganta, 'धातुविदाः', self.optionDhatuVidha)
            self.voice = "कर्तरि"
            self.groupBoxVoices = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.voices, 'प्रयोगः', self.optionVoice)
            self.groupBoxLakara = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.lakaras, 'लकारः', self.optionLakara)
            self.lakara = "लट्"
            self.grid.addWidget(self.groupBoxDhatuVidha, 2, 1)
            self.grid.addWidget(self.groupBoxVoices, 2, 2)
            self.grid.addWidget(self.groupBoxLakara, 2, 3)
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
                self.groupBoxGanas = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.Tganas, 'गनाः', self.optionGanaSelected, default=False)
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
                self.groupBoxPadis = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.Tpadis, 'परस्मैपदी', self.optionPadiSelected, default=False)
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
                self.groupBoxPadis = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.Tkarmas, 'सकर्मकः', self.optionKarmaSelected, default=False)
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
                self.groupBoxPadis = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.Tyits, 'सेट्',
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
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta_Tiganta.krdanta_Gana(self.gana)
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), self.arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            self.mainLayout.addWidget(self.listView_meanings)
            self.modelKrdanta_meanings.layoutChanged.emit()

            DhatuVidha = ["केवलतिगंतः", "णिजन्तः", "सन्नन्तः"]
            self.groupBoxDhatuVidha = self.createOptionGroup(DhatuVidha, 'धातुविदाः', self.optionDhatuVidha)
            self.voice = "कर्तरि"
            self.groupBoxVoices = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.voices, 'प्रयोगः', self.optionVoice)
            self.groupBoxLakara = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.lakaras, 'lakaras', self.optionLakara)
            self.lakara = "लट्"
            self.grid.addWidget(self.groupBoxDhatuVidha, 2, 1)
            self.grid.addWidget(self.groupBoxVoices, 2, 2)
            self.grid.addWidget(self.groupBoxLakara, 2, 3)
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
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta_Tiganta.krdanta_Padi(self.padi)
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), self.arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            self.mainLayout.addWidget(self.listView_meanings)
            self.modelKrdanta_meanings.layoutChanged.emit()

            DhatuVidha = ["केवलतिगंतः", "णिजन्तः", "सन्नन्तः"]
            self.groupBoxDhatuVidha = self.createOptionGroup(DhatuVidha, 'धातुविदाः', self.optionDhatuVidha)
            self.voice = "कर्तरि"
            self.groupBoxVoices = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.voices, 'प्रयोगः', self.optionVoice)
            self.groupBoxLakara = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.lakaras, 'lakaras', self.optionLakara)
            self.lakara = "लट्"
            self.grid.addWidget(self.groupBoxDhatuVidha, 2, 1)
            self.grid.addWidget(self.groupBoxVoices, 2, 2)
            self.grid.addWidget(self.groupBoxLakara, 2, 3)
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
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta_Tiganta.krdanta_Karma(self.karma)
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), self.arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            self.mainLayout.addWidget(self.listView_meanings)
            self.modelKrdanta_meanings.layoutChanged.emit()

            DhatuVidha = ["केवलतिगंतः", "णिजन्तः", "सन्नन्तः"]
            self.groupBoxDhatuVidha = self.createOptionGroup(DhatuVidha, 'धातुविदाः', self.optionDhatuVidha)
            self.voice = "कर्तरि"
            self.groupBoxVoices = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.voices, 'प्रयोगः', self.optionVoice)
            self.groupBoxLakara = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.lakaras, 'lakaras', self.optionLakara)
            self.lakara = "लट्"
            self.grid.addWidget(self.groupBoxDhatuVidha, 2, 1)
            self.grid.addWidget(self.groupBoxVoices, 2, 2)
            self.grid.addWidget(self.groupBoxLakara, 2, 3)
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
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta_Tiganta.krdanta_It(self.it)
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), self.arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            self.mainLayout.addWidget(self.listView_meanings)
            self.modelKrdanta_meanings.layoutChanged.emit()

            DhatuVidha = ["केवलतिगंतः", "णिजन्तः", "सन्नन्तः"]
            self.groupBoxDhatuVidha = self.createOptionGroup(DhatuVidha, 'धातुविदाः', self.optionDhatuVidha)
            self.voice = "कर्तरि"
            self.groupBoxVoices = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.voices, 'प्रयोगः', self.optionVoice)
            self.groupBoxLakara = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.lakaras, 'lakaras', self.optionLakara)
            self.lakara = "लट्"
            self.grid.addWidget(self.groupBoxDhatuVidha, 2, 1)
            self.grid.addWidget(self.groupBoxVoices, 2, 2)
            self.grid.addWidget(self.groupBoxLakara, 2, 3)
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
        self.modelDhatus = models.modelDhatus()
        self.menuItemChosen = None
        self.modelFinalResults = models.modelFinalResults_DataFrame()
        self.synonymView.setModel(self.modelFinalResults)
        self.synonymsButton.pressed.connect(self.synonyms_generate_or_analyse)
        self.nishpathiButton.pressed.connect(self.Nishpatthi)
        self.vyutpathiButton.pressed.connect(self.Vyutpatthi)
        self.lblNishpatthi.setVisible(False)
        self.txtNishpatthi.setVisible(False)

        self.formWidget_2.setVisible(False)
        self.formWidget_4.setVisible(False)
        self.formWidget_5.setVisible(False)
        self.synonymView.setVisible(False)

        for pg in [self.page1Button, self.page2Button, self.page3Button, self.page4Button, self.page5Button, self.page6Button, self.page7Button, self.page8Button]:
            pg.pressed.connect(self.generationPageDisplay)

        self.toolbar = self.addToolBar('Amara')
        self.amaraAction = QtWidgets.QAction('अमरकोश(Amarakosha)', self)
        self.amaraAction.setShortcut('Ctrl+A')
        self.amaraAction.setCheckable(True)
        self.amaraAction.triggered.connect(self.loadAmara)
        self.toolbar.addAction(self.amaraAction)

        self.toolbar = self.addToolBar('Subanta')
        self.subantaAction = QtWidgets.QAction('सुबंत(Subanta)', self)
        self.subantaAction.setShortcut('Ctrl+S')
        self.subantaAction.setCheckable(True)
        self.subantaAction.triggered.connect(self.loadSubanta)
        self.toolbar.addAction(self.subantaAction)

        self.toolbar = self.addToolBar('Krdanta')
        self.krdantaAction = QtWidgets.QAction('कृदंत(Krdanta)', self)
        self.krdantaAction.setShortcut('Ctrl+K')
        self.krdantaAction.setCheckable(True)
        self.krdantaAction.triggered.connect(self.loadKrdanta)
        self.toolbar.addAction(self.krdantaAction)

        self.toolbar = self.addToolBar('Tiganta')
        self.tigantaAction = QtWidgets.QAction('तिङंत(Tiganta)', self)
        self.tigantaAction.setShortcut('Ctrl+T')
        self.tigantaAction.setCheckable(True)
        self.tigantaAction.triggered.connect(self.loadTiganta)
        self.toolbar.addAction(self.tigantaAction)

        self.toolbar = self.addToolBar('Analysis')
        self.analysisAction = QtWidgets.QAction('Analysis', self)
        self.analysisAction.setShortcut('Ctrl+N')
        self.analysisAction.setCheckable(True)
        self.analysisAction.triggered.connect(self.loadAnalysis)
        self.toolbar.addAction(self.analysisAction)

        self.toolbar = self.addToolBar('Exit')
        self.exitAction = QtWidgets.QAction('निर्गमनम्(Exit)', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(QtWidgets.qApp.quit)
        self.toolbar.addAction(self.exitAction)

        self.statusBar().showMessage('Ready')
    def resetToolbarItems(self):
        self.amaraAction.setChecked(False)
        self.subantaAction.setChecked(False)
        self.krdantaAction.setChecked(False)
        self.tigantaAction.setChecked(False)
        self.analysisAction.setChecked(False)
    def loadAmara(self):
        self.menuItemChosen = 'Amara'
        self.resetToolbarItems()
        self.amaraAction.setChecked(True)
        self.wanted_script = self.scriptSelector.currentIndex()
        cols, data = AmaraKosha_Database_Queries.tblSelect('Amara_Words', maxrows=0)
        self.modelDhatus.data = list(map(lambda item: (False, transliterate_lines(item[2], IndianLanguages[self.wanted_script])), data))
        self.modelDhatus.dataIscii = list(map(lambda item: (False, item[3]), data))
        self.listView.setModel(self.modelDhatus)
        self.modelDhatus.layoutChanged.emit()

        self.listView.clicked.connect(self.enableSynonymsButton)
        self.synonymsButton.setText('पर्यायशब्द(Synonyms)')
        self.synonymsButton.setEnabled(False)
        self.nishpathiButton.setVisible(False)
        self.nishpathiButton.setEnabled(False)
        self.lblNishpatthi.setVisible(False)
        self.txtNishpatthi.setVisible(False)

        for control in [self.page1Button, self.page2Button, self.page3Button, self.page4Button, self.page5Button, self.page6Button, self.page7Button, self.page8Button]:
            control.setEnabled(False)
            control.setVisible(False)

    def enableSynonymsButton(self):
        self.synonymsButton.setEnabled(True)
        if self.menuItemChosen == 'Amara':
            self.nishpathiButton.setVisible(True)
            self.nishpathiButton.setEnabled(True)
            self.vyutpathiButton.setVisible(True)
            self.vyutpathiButton.setEnabled(True)
            self.vyutpathiSelector.setVisible(True)
            self.vyutpathiSelector.setEnabled(True)
        else:
            self.nishpathiButton.setVisible(False)
            self.nishpathiButton.setEnabled(False)
            self.vyutpathiButton.setVisible(False)
            self.vyutpathiButton.setEnabled(False)
            self.vyutpathiSelector.setVisible(False)
            self.vyutpathiSelector.setEnabled(False)
    def loadSubanta(self):
        self.menuItemChosen = 'Subanta'
        self.resetToolbarItems()
        self.subantaAction.setChecked(True)
        self.wanted_script = self.scriptSelector.currentIndex()
        self.nishpathiButton.setVisible(False)
        self.nishpathiButton.setEnabled(False)
        self.vyutpathiButton.setVisible(False)
        self.vyutpathiButton.setEnabled(False)
        self.vyutpathiSelector.setVisible(False)
        self.vyutpathiSelector.setEnabled(False)
        self.lblNishpatthi.setVisible(False)
        self.txtNishpatthi.setVisible(False)
        self.wanted_script = 0 if self.wanted_script == 5 else self.wanted_script  # ban tamil, always screws up things!
        cols, data = AmaraKosha_Database_Queries.tblSelect('Subanta', maxrows=0, script=self.wanted_script + 1)
        self.modelDhatus.data = list(map(lambda item: (False, item[2]), data))
        self.modelDhatus.dataIscii = list(map(lambda item: (False, item[3]), data))
        self.listView.setModel(self.modelDhatus)
        self.modelDhatus.layoutChanged.emit()
        self.listView.clicked.connect(self.enableSynonymsButton)
        self.synonymsButton.setText('Subanta Generation')
        self.synonymsButton.setEnabled(False)
        for control in [self.page1Button, self.page2Button, self.page3Button, self.page4Button, self.page5Button,
                        self.page6Button, self.page7Button, self.page8Button]:
            control.setEnabled(False)
            control.setVisible(False)
    def loadKrdanta(self):
        self.menuItemChosen = 'Krdanta'
        self.resetToolbarItems()
        self.krdantaAction.setChecked(True)
        self.wanted_script = self.scriptSelector.currentIndex()
        self.wanted_script = 0 if self.wanted_script == 5 else self.wanted_script  # ban tamil, always screws up things!
        self.nishpathiButton.setVisible(False)
        self.nishpathiButton.setEnabled(False)
        self.vyutpathiButton.setVisible(False)
        self.vyutpathiButton.setEnabled(False)
        self.vyutpathiSelector.setVisible(False)
        self.vyutpathiSelector.setEnabled(False)
        self.lblNishpatthi.setVisible(False)
        self.txtNishpatthi.setVisible(False)
        qry = 'select * from Sdhatu'
        param = None
        try:
            cols, data = AmaraKosha_Database_Queries.sqlQuery(qry, param, maxrows=0, script=self.wanted_script + 1)
            # print('%s\n%s'%(cols, data))
            self.modelDhatus.data = list(map(lambda item: (False, item[4]), data))
            self.modelDhatus.dataIscii = list(map(lambda item: (False, item[5]), data))
            self.listView.setModel(self.modelDhatus)
            self.modelDhatus.layoutChanged.emit()
            self.listView.clicked.connect(self.enableSynonymsButton)
            self.synonymsButton.setText('Krdanta Generation')
            self.synonymsButton.setEnabled(False)
        except Exception as e:
            print(e)
    def loadTiganta(self):
        self.menuItemChosen = 'Tiganta'
        self.resetToolbarItems()
        self.tigantaAction.setChecked(True)
        qry = 'select * from Sdhatu'
        param = None
        self.wanted_script = self.scriptSelector.currentIndex()
        self.wanted_script = 0 if self.wanted_script == 5 else self.wanted_script  # ban tamil, always screws up things!
        self.nishpathiButton.setVisible(False)
        self.nishpathiButton.setEnabled(False)
        self.vyutpathiButton.setVisible(False)
        self.vyutpathiButton.setEnabled(False)
        self.vyutpathiSelector.setVisible(False)
        self.vyutpathiSelector.setEnabled(False)
        self.lblNishpatthi.setVisible(False)
        self.txtNishpatthi.setVisible(False)
        try:
            self.colsSdhatudata, self.Sdhatudata = AmaraKosha_Database_Queries.sqlQuery(qry, param, maxrows=0, script=self.wanted_script + 1)
            self.modelDhatus.data = list(map(lambda item: (False, item[self.colsSdhatudata.index('Field2')]), self.Sdhatudata))
            self.modelDhatus.dataIscii = list(map(lambda item: (False, item[self.colsSdhatudata.index('Field2') + 1]), self.Sdhatudata))
            # print('loadTiganta gana=%i padi=%i it=%i'%(self.gana, self.padi, self.it))
            self.listView.setModel(self.modelDhatus)
            self.modelDhatus.layoutChanged.emit()
            self.listView.clicked.connect(self.enableSynonymsButton)
            self.synonymsButton.setText('Tiganta Generation')
            self.synonymsButton.setEnabled(False)
        except Exception as e:
            print(e)
    def loadAnalysis(self):
        self.menuItemChosen = 'Analysis'
        self.resetToolbarItems()
        self.analysisAction.setChecked(True)
        self.wanted_script = self.scriptSelector.currentIndex()
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'I:/VMBox-Shared-WinXP-VB/ChaamiMaama/Narasimhan/all_in_one_DAO/Bandarkar')
        if fname[0]:
            f = open(fname[0], 'r')
            self.synonymsButton.setText('ಪದರೂಪ ವಿಶ್ಲೇಷಣೆ(Morphological Analysis)')
            self.wanted_script = self.scriptSelector.currentIndex()
            self.listView.clicked.connect(self.enableSynonymsButton)
            with f:
                dataIscii = f.readlines()
                data = [AmaraKosha_Database_Queries.iscii_unicode(item) for item in dataIscii]
                self.modelDhatus.data = list(map(lambda item: (False, item[:-1]), data))
                self.modelDhatus.dataIscii = list(map(lambda item: (False, item[:-1]), dataIscii))
                self.listView.setModel(self.modelDhatus)
                self.modelDhatus.layoutChanged.emit()
    def synonyms_generate_or_analyse(self):
        self.statusBar().showMessage('Ready')
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
                    status, self.amaraWord = self.modelDhatus.dataIscii[row]
                    self.Amarasynonyms, KanWord, EngWord, HinWord = Kosha_Subanta_Krdanta_Tiganta.Amarakosha(self.amaraWord, self.wanted_script+1)
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
                    self.modelFinalResults._data = pandas.DataFrame(self.Amarasynonyms[0])
                    for pg in [self.page1Button, self.page2Button, self.page3Button, self.page4Button, self.page5Button, self.page6Button, self.page7Button, self.page7Button]:
                        pg.setEnabled(False)
                        pg.setVisible(False)
                    for i in range(len(self.Amarasynonyms)):
                      pg = [self.page1Button, self.page2Button, self.page3Button, self.page4Button, self.page5Button, self.page6Button][i]
                      pg.setEnabled(True)
                      pg.setVisible(True)
                    self.modelFinalResults.layoutChanged.emit()
                except Exception as e:
                    print('%s for amara word %s'%(e, AmaraKosha_Database_Queries.iscii_unicode(self.amaraWord)))
                    self.statusBar().showMessage(str(e)) #str('%s for amara word %s' % (e, AmaraKosha_Database_Queries.iscii_unicode(self.amaraWord, self.wanted_script))))
        elif self.menuItemChosen == 'Subanta':
            self.formWidget_2.setVisible(False)
            self.formWidget_4.setVisible(True)
            self.formWidget_5.setVisible(False)
            self.synonymView.setVisible(True)
            for control in [self.page4Button, self.page5Button, self.page6Button, self.page7Button, self.page8Button]:
                control.setEnabled(False)
                control.setVisible(False)
            indexes = self.listView.selectedIndexes()
            if indexes:
                index = indexes[0]
                row = index.row()
                status, base = self.modelDhatus.dataIscii[row]
                try:
                    forms, anta, linga = Kosha_Subanta_Krdanta_Tiganta.subanta_Generation(base, self.wanted_script + 1)
                    self.antaLineEdit.setText(AmaraKosha_Database_Queries.iscii_unicode(anta, self.wanted_script+1))
                    self.lingaLineEdit.setText(AmaraKosha_Database_Queries.iscii_unicode(linga, self.wanted_script+1))
                    self.labelSubanta.setText(transliterate_lines("अंत/लिंग", IndianLanguages[self.wanted_script]))
                    self.antaLabel.setText(transliterate_lines("अंत", IndianLanguages[self.wanted_script]))
                    self.lingaLabel.setText(transliterate_lines("लिंग", IndianLanguages[self.wanted_script]))
                    self.Categories.setText('सुबंतः')
                    self.modelFinalResults._data = pandas.DataFrame(forms,
                                                                    columns=[transliterate_lines(vacana, IndianLanguages[self.wanted_script]) for vacana in Kosha_Subanta_Krdanta_Tiganta.vacanas],
                                                                    index=[transliterate_lines(vibhakti, IndianLanguages[self.wanted_script]) for vibhakti in Kosha_Subanta_Krdanta_Tiganta.vibhaktis])
                    self.modelFinalResults.layoutChanged.emit()
                except Exception as e:
                    self.statusBar().showMessage(str(e))
        elif self.menuItemChosen == 'Krdanta':
            self.formWidget_4.setVisible(False)
            self.formWidget_5.setVisible(False)
            try:
                indexes = self.listView.selectedIndexes()
                if indexes:
                    index = indexes[0]
                    row = index.row()
                    status, krdantaWord = self.modelDhatus.dataIscii[row]
                dialog = modalDialog_Krdanta(self, krdantaWord, self.wanted_script + 1)
                # print('%s DhatuVidhas %s KrdantaVidha %s Krdanta Mode %s'%(dialog.ok, dialog.DhatuVidah, dialog.KrdantaVidah, dialog.KrdMode))
                if dialog.okClicked:
                        if dialog.mainOption == 'Sorted List':
                            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = \
                                Kosha_Subanta_Krdanta_Tiganta.krdanta_arthas_karmas(krdantaWord)
                            if not dialog.KrdantaVidah == "कृदव्ययम्":
                                self.generationResults(self.dhatuNo, dialog)
                            else:
                                self.krdData = Kosha_Subanta_Krdanta_Tiganta.krdanta_SortedList_KrDantavyayam(self.dhatuNo, dialog.DhatuVidah, dialog.KrdantaVidah,
                                                                                                              dialog.KrdMode, self.dataDhatu, self.cols_dataDhatu)
                                self.setTexts(zip(
                                    [self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu,
                                     self.txtGana, self.txtPadi, self.txtKarma, self.txtIt, self.txtDhatuVidah,
                                     self.txtKrdantaVidah_prayoga, self.txtPratyaya_lakara, self.txtSabda],
                                    [self.krdData[0].verb, self.arthas[0], self.krdData[0].nijverb,
                                     self.krdData[0].sanverb, self.krdData[0].gana, self.krdData[0].padi,
                                     self.karmas[0], self.krdData[0].it, self.krdData[0].dhatuVidhah,
                                     self.krdData[0].krdantaVidhah, self.krdData[0].pratyayaVidhah,
                                     self.krdData[0].sabda]))
                                for control in [self.synonymView, self.lblAnta, self.txtAnta, self.lblLinga, self.txtLinga,
                                                self.lblPratipadika,self.txtPratipadika]: control.setVisible(False)
                                # self.synonymView.setVisible(False)
                                self.formWidget_2.setVisible(True)
                                self.LabelSabda.setVisible(True)
                                self.txtSabda.setVisible(True)
                                for control in [self.page1Button, self.page2Button, self.page1Button, self.page3Button]:
                                    control.setEnabled(False)
                                    control.setVisible(False)
                        else:
                            self.arthas, self.karmas = dialog.arthas, dialog.karmas
                            self.generationResults(dialog.dhatuNo, dialog)
            except Exception as e:
                self.statusBar().showMessage(str(e))
        elif self.menuItemChosen == 'Tiganta':
            self.formWidget_4.setVisible(False)
            self.formWidget_5.setVisible(False)
            try:
                indexes = self.listView.selectedIndexes()
                if indexes:
                    index = indexes[0]
                    row = index.row()
                    status, tigantaWord = self.modelDhatus.dataIscii[row]
                    self.gana = int(self.Sdhatudata[row][self.colsSdhatudata.index('Field9')][0])
                    self.padi = int(self.Sdhatudata[row][self.colsSdhatudata.index('Field9')][1])
                    self.it = int(self.Sdhatudata[row][self.colsSdhatudata.index('Field9')][2])
                dialog = modalDialog_Tiganta(self, tigantaWord, requested_script=self.wanted_script+1)
                # print('%s DhatuVidhas %s KrdantaVidha %s Krdanta Mode %s'%(dialog.ok, dialog.DhatuVidah, dialog.KrdantaVidah, dialog.KrdMode))
                if dialog.okClicked:
                    if dialog.mainOption == 'Sorted List(अकारादि)':
                        self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = \
                            Kosha_Subanta_Krdanta_Tiganta.krdanta_arthas_karmas(tigantaWord)
                        self.generationResults(self.dhatuNo, dialog)
                    else:
                        self.arthas, self.karmas = dialog.arthas, dialog.karmas
                        self.generationResults(dialog.dhatuNo, dialog)
            except Exception as e:
                self.statusBar().showMessage(str(e))
        elif self.menuItemChosen == 'Analysis':
            self.formWidget_4.setVisible(False)
            self.formWidget_5.setVisible(False)
            self.synonymView.setVisible(True)
            indexes = self.listView.selectedIndexes()
            if indexes:
                index = indexes[0]
                row = index.row()
                status, base = self.modelDhatus.dataIscii[row]
                try:
                    self.subforms, self.tigforms, self.krdforms = [], [], []
                    self.Subantas, self.Krdantas, self.Tigantas = [], [], []
                    for word in base.split(' '):
                        try:
                            forms, anta, linga, rupam, vibhakti, vacana = Kosha_Subanta_Krdanta_Tiganta.subanta_Analysis(word, self.wanted_script+1)
                            if not forms==[]:
                                self.subforms += forms
                                self.Subantas.append([rupam, anta, linga, vibhakti, vacana])
                            self.setTexts(zip([self.txtDhatu, self.lblDhatvarya, self.txtDhatvarya, self.lblNijidhatu, self.txtNijiDhatu,
                                               self.lblSaniDhatu, self.txtSaniDhatu, self.lblGana, self.txtGana],
                                [rupam, 'अंतः', anta, 'लिंगः', linga, 'विभक्तिः', vibhakti, 'वचनः', vacana]))
                            for lbl in [self.lblDhatu, self.lblDhatvarya, self.lblNijidhatu, self.lblSaniDhatu,
                                        self.lblGana, self.lblPadi, self.lblKarma, self.lblIt, self.lblDhatuVidah,
                                        self.lblKrdantaVidah_prayoga, self.lblPratyaya_lakara, self.lblAnta,
                                        self.lblLinga, self.lblPratipadika, self.lblSabda]:
                                lbl.setText(transliterate_lines(lbl.text(), IndianLanguages[self.wanted_script]))
                            self.Categories.setText(transliterate_lines('सुबंतः', IndianLanguages[self.wanted_script]))
                            for control in [self.lblAnta, self.txtAnta, self.lblLinga, self.txtLinga, self.lblPadi, self.txtPadi,
                                            self.lblKarma, self.txtKarma, self.lblIt, self.txtIt, self.lblPratyaya_lakara,
                                            self.txtPratyaya_lakara, self.lblDhatuVidah, self.txtDhatuVidah, self.lblKrdantaVidah_prayoga,
                                            self.txtKrdantaVidah_prayoga, self.lblPratipadika, self.txtPratipadika,
                                            self.lblSabda, self.txtSabda]: control.setVisible(False)
                            self.modelFinalResults._data = pandas.DataFrame(self.subforms[0:8],
                                                                            columns=[transliterate_lines(vacana,IndianLanguages[self.wanted_script]) for vacana in Kosha_Subanta_Krdanta_Tiganta.vacanas],
                                                                            index=[transliterate_lines(vibhakti,IndianLanguages[self.wanted_script]) for vibhakti in Kosha_Subanta_Krdanta_Tiganta.vibhaktis])
                            self.modelFinalResults.layoutChanged.emit()
                        except Exception as e:
                            print(e)
                        for control in [self.synonymView, self.formWidget_2]: control.setVisible(True)
                        for control in [self.page1Button, self.page2Button, self.page1Button, self.page3Button, self.page4Button,
                                        self.page5Button, self.page6Button, self.page7Button, self.page8Button]:
                            control.setEnabled(True)
                            control.setVisible(True)
                        try:
                            forms, tigData = Kosha_Subanta_Krdanta_Tiganta.tiganta_Analysis(word, self.wanted_script + 1)
                            if not forms==[]:
                                self.tigforms += forms
                            if not tigData == []: self.Tigantas.append(tigData)
                            # print('UI-Analysis tigforms %s'%self.tigforms)
                            forms, krdData = Kosha_Subanta_Krdanta_Tiganta.krdanta_Analysis(word, self.wanted_script + 1)
                            if not forms==[]:
                                self.krdforms += forms
                            if not krdData == []: self.Krdantas.append(krdData)
                            # print('UI-Analysis krdforms %s'%self.krdforms)
                        except Exception as e:
                            print(e)
                    # for tigData in self.Tigantas:
                    #     for item in tigData: print('UI-Analysis tiganta Details %s'%item.get())
                    # for krdData in self.Krdantas:
                    #     for item in krdData: print('UI-Analysis krdanta Details %s'%item.get())
                    # print('UI-Analysis subanta %i %s\ntiganta %i %s\nkrdanta %i %s'%(len(self.subforms), self.subforms, len(self.tigforms), self.tigforms, len(self.krdforms), self.krdforms))
                except Exception as e:
                    self.statusBar().showMessage(str(e))
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
    def generationPageDisplay(self):
        try:
            indx = ['page1Button', 'page2Button', 'page3Button', 'page4Button', 'page5Button', 'page6Button',
                    'page7Button', 'page8Button'].index(self.sender().objectName())
            if self.menuItemChosen == 'Amara':
                self.modelFinalResults._data = pandas.DataFrame(self.Amarasynonyms[indx])
            elif self.menuItemChosen == 'Krdanta':
                self.setTexts(zip([self.txtLinga, self.txtAnta, self.txtSabda], [self.krdData[indx].linga, self.krdData[indx].anta, self.forms[indx][0]]))
                self.modelFinalResults._data = pandas.DataFrame(self.forms[indx * 8: indx * 8 + 8],
                                                                columns=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vacanas],
                                                                index=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vibhaktis])
                self.modelFinalResults.layoutChanged.emit()
            elif self.menuItemChosen == 'Tiganta':
                self.modelFinalResults._data = pandas.DataFrame(self.forms[indx * 3: indx * 3 + 3],
                                                                columns=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vacanas],
                                                                index=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.purushas])

                self.modelFinalResults.layoutChanged.emit(self.forms[indx * 3: indx * 3 + 3],)
            else: #Analysis
                self.Categories.setText(transliterate_lines(['सुबंतः','तिगंतः','तिगंतः','कृदंतः','कृदंतः','कृदंतः','कृदंतः','कृदंतः'][indx], IndianLanguages[self.wanted_script]))
                if indx == 0:
                    for control in [self.synonymView, self.formWidget_2, self.txtDhatu, self.lblDhatvarya, self.txtDhatvarya,
                                    self.lblNijidhatu, self.txtNijiDhatu]: control.setVisible(True)
                    for control in [self.lblAnta, self.txtAnta, self.lblLinga, self.txtLinga, self.lblSabda, self.txtSabda, self.lblGana,
                                    self.txtGana, self.lblPadi, self.txtPadi, self.lblKarma, self.txtKarma, self.lblIt, self.txtIt,
                                    self.lblPratyaya_lakara, self.txtPratyaya_lakara, self.txtDhatuVidah, self.txtKrdantaVidah_prayoga,
                                    self.lblDhatuVidah, self.lblKrdantaVidah_prayoga, self.lblPratipadika]: control.setVisible(False)
                    self.setTexts(zip([self.txtDhatu, self.lblDhatvarya, self.txtDhatvarya, self.lblNijidhatu, self.txtNijiDhatu],
                        [self.Subantas[0][0], transliterate_lines('अंतः', IndianLanguages[self.wanted_script]), self.Subantas[0][1],
                         transliterate_lines('लिंगः', IndianLanguages[self.wanted_script]),
                         self.Subantas[0][2], 'विभक्तिः', self.Subantas[0][3],'वचनः', self.Subantas[0][4]]))
                    self.modelFinalResults._data = pandas.DataFrame(self.subforms[indx * 8: indx * 8 + 8],
                                                                columns=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vacanas],
                                                                index=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vibhaktis])
                elif indx in [1,2]:
                    for control in [self.lblAnta, self.txtAnta, self.lblLinga, self.txtLinga, self.lblSabda,
                                    self.txtSabda, self.lblGana, self.txtGana, self.lblPadi, self.txtPadi, self.lblKarma,
                                    self.txtKarma, self.lblIt, self.txtIt, self.lblPratyaya_lakara, self.txtPratyaya_lakara, self.txtDhatuVidah,
                                    self.txtKrdantaVidah_prayoga, self.lblDhatuVidah, self.lblKrdantaVidah_prayoga,
                                    self.lblPratipadika]: control.setVisible(True)
                    for control,text in zip([self.lblDhatu, self.lblDhatvarya, self.lblNijidhatu, self.lblSaniDhatu, self.lblGana, self.lblPadi,
                                    self.lblKarma, self.lblIt, self.lblDhatuVidah,self.lblKrdantaVidah_prayoga, self.lblPratyaya_lakara,
                                        self.lblAnta, self.lblLinga, self.lblPratipadika, self.lblSabda],
                                   ['धातुः','धात्वर्य:','णिजि धातु:','सनि धातु:','गण:','पदिः','कर्मः','इट्','धातुविधः','कृदंतविधः','प्रत्ययः','अंतः','लिंगः','प्रतिपादिकं','रूपं']):
                        control.setText(text)
                    self.setTexts(zip([self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu,
                         self.txtGana, self.txtPadi, self.txtKarma, self.txtIt, self.txtDhatuVidah,
                         self.txtKrdantaVidah_prayoga, self.txtPratyaya_lakara],
                        [transliterate_lines(txt, IndianLanguages[self.wanted_script]) for txt in
                         [self.Tigantas[indx-1][0].verb, self.Tigantas[indx-1][0].base,self.Tigantas[indx-1][0].sanverb,
                          self.Tigantas[indx-1][0].nijverb, self.Tigantas[indx-1][0].gana,self.Tigantas[indx-1][0].padi, self.Tigantas[indx-1][0].karma,
                          self.Tigantas[indx-1][0].it,self.Tigantas[indx-1][0].dhatuVidah, self.Tigantas[indx-1][0].voice, self.Tigantas[indx-1][0].lakara]]
                    ))
                    self.lblPratyaya_lakara.setText(transliterate_lines('लकारः', IndianLanguages[self.wanted_script]))
                    self.lblKrdantaVidah_prayoga.setText(transliterate_lines('प्रयोगः', IndianLanguages[self.wanted_script]))
                    self.Categories.setText(transliterate_lines('तिगंतः', IndianLanguages[self.wanted_script]))
                    for control in [self.lblAnta, self.txtAnta, self.lblLinga, self.txtLinga,
                                    self.lblPratipadika, self.txtPratipadika, self.lblSabda, self.txtSabda]: control.setVisible(False)
                    for lbl in [self.lblDhatu, self.lblDhatvarya, self.lblNijidhatu, self.lblSaniDhatu, self.lblGana,
                            self.lblPadi, self.lblKarma, self.lblIt, self.lblDhatuVidah, self.lblKrdantaVidah_prayoga,
                            self.lblPratyaya_lakara, self.lblAnta,self.lblLinga, self.lblPratipadika, self.lblSabda]: lbl.setText(transliterate_lines(lbl.text(), IndianLanguages[self.wanted_script]))
                    self.modelFinalResults._data = pandas.DataFrame(self.tigforms[(indx-1) * 3: (indx-1) * 3 + 3],
                                                                columns=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vacanas],
                                                                index=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.purushas])
                else:
                    for control,text in zip([self.lblDhatu, self.lblDhatvarya, self.lblNijidhatu, self.lblSaniDhatu, self.lblGana, self.lblPadi,
                                    self.lblKarma, self.lblIt, self.lblDhatuVidah,self.lblKrdantaVidah_prayoga, self.lblPratyaya_lakara,
                                        self.lblAnta, self.lblLinga, self.lblPratipadika, self.lblSabda],
                                   ['धातुः','धात्वर्य:','णिजि धातु:','सनि धातु:','गण:','पदिः','कर्मः','इट्','धातुविधः','कृदंतविधः','प्रत्ययः','अंतः','लिंगः','प्रतिपादिकं','रूपं']):
                        control.setText(transliterate_lines(text, IndianLanguages[self.wanted_script]))
                    ind = min(indx-3, len(self.Krdantas[0]))
                    krdData = self.Krdantas[0][ind]
                    self.setTexts(zip([self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu,
                    self.txtGana, self.txtPadi, self.txtKarma, self.txtIt, self.txtDhatuVidah,
                    self.txtKrdantaVidah_prayoga, self.txtPratyaya_lakara, self.txtAnta, self.txtLinga,
                    self.txtPratipadika, self.txtSabda],
                    [krdData.verb, krdData.meaning, krdData.nijverb,
                     krdData.sanverb, krdData.gana, krdData.padi,
                     krdData.karma, krdData.it, krdData.dhatuVidhah,
                     krdData.krdantaVidhah, krdData.pratyayaVidhah, krdData.anta,
                     krdData.linga, krdData.sabda,  self.krdforms[indx-3][0]]))

                    self.lblPratyaya_lakara.setText('प्रत्ययः')
                    self.lblKrdantaVidah_prayoga.setText('कृदंतविधः')
                    for lbl in [self.lblDhatu, self.lblDhatvarya, self.lblNijidhatu, self.lblSaniDhatu, self.lblGana,
                            self.lblPadi, self.lblKarma, self.lblIt, self.lblDhatuVidah, self.lblKrdantaVidah_prayoga,
                            self.lblPratyaya_lakara, self.lblAnta,self.lblLinga, self.lblPratipadika, self.lblSabda]:
                        lbl.setText(transliterate_lines(lbl.text(), IndianLanguages[self.wanted_script]))
                    for control in [self.txtDhatu, self.lblDhatvarya, self.txtDhatvarya,
                                    self.lblNijidhatu, self.txtNijiDhatu, self.lblAnta, self.txtAnta, self.lblLinga, self.txtLinga,
                                    self.lblSabda, self.txtSabda, self.lblGana, self.txtGana, self.lblPadi, self.txtPadi, self.lblKarma,
                                    self.txtKarma, self.lblIt, self.txtIt, self.lblPratyaya_lakara, self.txtPratyaya_lakara,
                                    self.txtDhatuVidah, self.txtKrdantaVidah_prayoga, self.lblDhatuVidah, self.lblKrdantaVidah_prayoga,
                                    self.lblPratipadika, self.txtPratipadika]: control.setVisible(True)

                    strt = min((indx-3) * 8, len(self.krdforms) - 8)
                    self.modelFinalResults._data = pandas.DataFrame(self.krdforms[strt: strt + 8],
                                                                columns=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vacanas],
                                                                index=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vibhaktis])
                self.modelFinalResults.layoutChanged.emit()

        except Exception as e:
            print(e)
    def generationResults(self, dhatuNo, dialog):
        if self.menuItemChosen == 'Krdanta':
            self.forms, self.krdData = Kosha_Subanta_Krdanta_Tiganta.krdanta_Generation(dhatuNo,
                                                                                      dialog.DhatuVidah,
                                                                                      dialog.KrdantaVidah,
                                                                                      dialog.KrdMode,
                                                                                      requested_script=self.wanted_script+1)
            self.modelFinalResults._data = pandas.DataFrame(self.forms[:8],
                                                            columns=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vacanas],
                                                            index=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vibhaktis])
            self.modelFinalResults.layoutChanged.emit()
            self.setTexts(zip(
                [self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu,
                 self.txtGana, self.txtPadi, self.txtKarma, self.txtIt, self.txtDhatuVidah,
                 self.txtKrdantaVidah_prayoga, self.txtPratyaya_lakara, self.txtSabda, self.txtAnta, self.txtLinga,
                 self.txtPratipadika],
                [self.krdData[0].verb, transliterate_lines(self.arthas[0], IndianLanguages[self.wanted_script]), self.krdData[0].nijverb,
                 self.krdData[0].sanverb, self.krdData[0].gana, self.krdData[0].padi,
                 transliterate_lines(self.karmas[0], IndianLanguages[self.wanted_script]), self.krdData[0].it, self.krdData[0].dhatuVidhah,
                 self.krdData[0].krdantaVidhah, self.krdData[0].pratyayaVidhah,
                 self.krdData[0].sabda, self.krdData[0].anta, self.krdData[0].linga,
                 self.forms[0][0]]))
            self.lblPratyaya_lakara.setText('प्रत्ययः')
            self.lblKrdantaVidah_prayoga.setText('कृदंतविधः')
            self.Categories.setText(transliterate_lines('कृदंतः', IndianLanguages[self.wanted_script]))
        else: # Tiganta
            self.forms, self.tigData = Kosha_Subanta_Krdanta_Tiganta.tiganta_Generation(dhatuNo,
                                                                                        dialog.DhatuVidah,
                                                                                        dialog.voice,
                                                                                        dialog.lakara,
                                                                                        requested_script=self.wanted_script+1)
            self.modelFinalResults._data = pandas.DataFrame(self.forms[:9],
                                                            columns=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vacanas],
                                                            index=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.purushas])
            self.modelFinalResults.layoutChanged.emit()
            self.setTexts(zip(
                [self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu,
                 self.txtGana, self.txtPadi, self.txtKarma, self.txtIt, self.txtDhatuVidah,
                 self.txtKrdantaVidah_prayoga, self.txtPratyaya_lakara],
                [transliterate_lines(txt, IndianLanguages[self.wanted_script]) for txt in [AmaraKosha_Database_Queries.iscii_unicode(dialog.tigantaWord), self.arthas[0],
                                                                                           self.Sdhatudata[0][self.colsSdhatudata.index('Field3')], self.Sdhatudata[0][self.colsSdhatudata.index('Field4')],
                                                                                           Kosha_Subanta_Krdanta_Tiganta.Tganas[self.gana], Kosha_Subanta_Krdanta_Tiganta.Tganas[self.padi], self.karmas[0],
                                                                                           Kosha_Subanta_Krdanta_Tiganta.Tganas[self.it],
                                                                                           dialog.DhatuVidah, dialog.voice, dialog.lakara]]
            ))
            self.lblPratyaya_lakara.setText('लकारः')
            self.lblKrdantaVidah_prayoga.setText('प्रयोगः')
            self.Categories.setText(transliterate_lines('तिगंतः', IndianLanguages[self.wanted_script]))
        for lbl in [self.lblDhatu, self.lblDhatvarya, self.lblNijidhatu, self.lblSaniDhatu, self.lblGana,  self.lblPadi,  self.lblKarma,  self.lblIt,
                    self.lblDhatuVidah,  self.lblKrdantaVidah_prayoga,  self.lblPratyaya_lakara,  self.lblAnta,  self.lblLinga,  self.lblPratipadika,
                    self.lblSabda]:
            lbl.setText(transliterate_lines(lbl.text(), IndianLanguages[self.wanted_script]))
        self.formWidget_2.setVisible(True)
        self.synonymView.setVisible(True)
        if self.menuItemChosen == 'Krdanta':
            for control in [self.lblAnta, self.txtAnta, self.lblLinga, self.txtLinga, self.lblPratipadika,
                            self.txtPratipadika,self.lblSabda,self.txtSabda]: control.setVisible(True)
            for control in [self.page1Button, self.page2Button, self.page1Button, self.page3Button]:
                control.setEnabled(True)
                control.setVisible(True)
            if len(self.forms) > 24:
                for control in [self.page4Button, self.page5Button, self.page6Button]:
                    control.setEnabled(True)
                    control.setVisible(True)
            else:
                for control in [self.page4Button, self.page5Button, self.page6Button]:
                    control.setEnabled(False)
                    control.setVisible(False)
            for control in [self.page7Button, self.page8Button]:
                control.setEnabled(False)
                control.setVisible(False)
        else:
            for control in [self.lblAnta, self.txtAnta, self.lblLinga, self.txtLinga, self.lblPratipadika,
                            self.txtPratipadika,self.lblSabda,self.txtSabda]: control.setVisible(False)
            for control in [self.page1Button, self.page2Button, self.page1Button, self.page3Button, self.page4Button,
                            self.page5Button, self.page6Button, self.page7Button, self.page8Button]:
                control.setEnabled(False)
                control.setVisible(False)
    def Nishpatthi(self):
        indexes = self.listView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            try:
                status, self.amaraWord = self.modelDhatus.dataIscii[row]
                nishpatthi = Kosha_Subanta_Krdanta_Tiganta.nishpatthi(self.amaraWord)  # don't ask for non-devanagari script, invalid results!
                if len(nishpatthi) > 0:
                    txtNishpatthi = '\n'.join([item[0] for item in nishpatthi])
                    self.txtNishpatthi.setText(txtNishpatthi)
                    self.autoResize(self.txtNishpatthi)
                    self.lblNishpatthi.setVisible(True)
                    self.txtNishpatthi.setVisible(True)
                    self.lblNishpatthi.setText('निश्पत्ति')
            except Exception as e:
                 self.statusBar().showMessage('Nishpatthi:%s'%e)
    def Vyutpatthi(self):
        indexes = self.listView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            try:
                status, self.amaraWord = self.modelDhatus.dataIscii[row]
                vyupatthi = Kosha_Subanta_Krdanta_Tiganta.vyutpatthi(self.amaraWord,
                                                                     ['Sanskrit', 'Hindi', 'Odiya'][self.vyutpathiSelector.currentIndex()])
                if len(vyupatthi) > 0:
                    txtNishpatthi = '\n'.join([item[0] for item in vyupatthi])
                    self.txtNishpatthi.setText(txtNishpatthi)
                    self.autoResize(self.txtNishpatthi)
                    self.lblNishpatthi.setVisible(True)
                    self.txtNishpatthi.setVisible(True)
                    self.lblNishpatthi.setText('व्युत्त्पत्ति')
            except Exception as e:
                 self.statusBar().showMessage('Vyutpatthi:%s'%e)

logging.basicConfig(level=logging.DEBUG, filename='../../Amarakosha.log', format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
