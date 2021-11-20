__author__ = 'NarasMG'

import logging  #, icecream as ic #, inspect
import sys, os, pandas
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QRadioButton, QGridLayout, QGroupBox, QHBoxLayout, QListView, QFileDialog
from matplotlib.font_manager import FontProperties

sys.path.append(os.getcwd())
from source.Controller import Kosha_Subanta_Krdanta_Tiganta, SyntaxAnalysis
from source.Controller.Transliterate import *
from source.Model import AmaraKosha_Database_Queries, models
import networkx as nx
import matplotlib.pyplot as plt

qt_creator_file = os.path.join(os.getcwd(), "source/View", "amara_uiComposition.xml")
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
        self.DhatuVidhaButtons = ["केवलकृदन्तः", "णिजन्तः", "सन्नन्तः"]
        self.KrdVidhaButtons = ["विध्यर्थः", "भूतः", "वर्तमानः", "भविष्यत्:", "कृदव्ययम्:"]
        self.KrdModeButtons = ["तव्य", "अनीयर्", "य", "क्त", "क्तवतु", "शतृ", "शानच्", "स्यशतृ", "स्यशानच्", "तुमुन्", "क्त्वा"]
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
        self.addedListview = False
    def okClicked(self):
     self.okClicked = True
     indexes = self.listView_meanings.selectedIndexes()
     if indexes:
         index = indexes[0]
         row = index.row()
         status, self.arthas = self.modelKrdanta_meanings.data[row]
     else: status, self.arthas = self.modelKrdanta_meanings.data[0]
     self.close()
    def cancelClicked(self):
     self.okClicked = False
     self.close()
    def createOptionGroup(self, group, name, optionCatcher, default = True):
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
    '''def addDhatuKrdantaGroups(self):
        self.groupBoxDhatuVidha = self.createOptionGroup(self.DhatuVidhaButtons, 'धातुविदाः', self.optionDhatuVidha)
        self.groupBoxKrdantaVidha = self.createOptionGroup(self.KrdVidhaButtons, 'कृदंतविधाः', self.optionKrdantaVidha)
        self.groupBoxKrdMode = self.createOptionGroup(self.KrdModeButtons, 'Krdanta Mode', self.optionKrdMode)
        self.KrdMode = "तव्य"
        self.grid.addWidget(self.groupBoxKrdantaVidha, 2, 1)
        self.grid.addWidget(self.groupBoxDhatuVidha, 2, 2)
        self.grid.addWidget(self.groupBoxKrdMode, 2, 3)'''
    def dhatuVidahkrdVidahButtonCombinations(self):
        if self.groupBoxKrdMode != None and self.DhatuVidah != None and self.KrdantaVidah != None:
            option = self.groupBoxKrdMode.findChildren(QRadioButton)
            for opt in option: opt.setEnabled(False)
            if self.KrdantaVidah == "विध्यर्थः":
                for opt in option[:3]: opt.setEnabled(True)
                option[0].setChecked(True)
            elif self.KrdantaVidah == "भूतः":
                for opt in option[3:5]: opt.setEnabled(True)
                option[3].setChecked(True)
            elif self.KrdantaVidah == "कृदव्ययम्:":
                for opt in option[9:]: opt.setEnabled(True)
                option[9].setChecked(True)
            else:
                if self.DhatuVidah in ["केवलकृदन्तः", "सन्नन्तः"]:
                    if self.KrdantaVidah == "वर्तमानः":
                        option[5].setEnabled(True)
                        option[5].setChecked(True)
                    else:
                        option[7].setEnabled(True)
                        option[7].setChecked(True)
                else:
                    if self.KrdantaVidah == "वर्तमानः":
                        for opt in option[5:7]: opt.setEnabled(True)
                        option[5].setChecked(True)
                    else:
                        for opt in option[7:9]: opt.setEnabled(True)
                        option[7].setChecked(True)
    def optionDhatuVidha(self):
        if self.sender().isChecked(): self.DhatuVidah = self.sender().text
        self.dhatuVidahkrdVidahButtonCombinations()
    def optionKrdantaVidha(self):
        if self.sender().isChecked(): self.KrdantaVidah  = self.sender().text
        self.dhatuVidahkrdVidahButtonCombinations()
    def optionKrdMode(self):
        if self.sender().isChecked(): self.KrdMode = self.sender().text
    def optionSortedList(self):
        self.mainOption = self.sender().text()
        try:
            if not self.addedListview:
                self.listView_meanings = QListView(self)
            self.modelKrdanta_meanings = models.modelKrdanta_meanings()
            self.listView_meanings.setModel(self.modelKrdanta_meanings)
            self.listView_meanings.setUniformItemSizes(True)
            self.listView_meanings.setMaximumWidth(self.listView_meanings.sizeHintForColumn(0) + 125)
            self.listView_meanings.setMaximumHeight(self.listView_meanings.sizeHintForRow(0) + 35)
            arthas, _, _, _, _ = Kosha_Subanta_Krdanta_Tiganta.tiganta_krdanta_arthas_karmas(self.krdantaWord) #, requested_script=self.script)
            arthas = [transliterate_lines(item, IndianLanguages[self.script - 1]) for item in arthas]
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            if not self.addedListview:
                self.mainLayout.addWidget(self.listView_meanings)
                self.addedListview = True
            # self.listView_meanings.clicked.connect(self.gridDisplay)
            self.removeAllGroups()
            self.grid = QGridLayout(self)
            self.gridDisplay()
            self.modelKrdanta_meanings.layoutChanged.emit()
        except Exception as e:
            print('Exception Sorted list:%s' % e)
    def gridDisplay(self):
        # self.removeAllGroups()
        # self.grid = QGridLayout(self)
        self.groupBoxDhatuVidha = self.createOptionGroup(self.DhatuVidhaButtons, 'धातुविदाः', self.optionDhatuVidha)
        self.groupBoxKrdantaVidha = self.createOptionGroup(self.KrdVidhaButtons, 'कृदंतविधाः', self.optionKrdantaVidha)
        self.groupBoxKrdMode = self.createOptionGroup(self.KrdModeButtons, 'Krdanta Mode', self.optionKrdMode)
        # self.KrdMode = "तव्य"
        self.grid.addWidget(self.groupBoxDhatuVidha, 2, 1)
        self.grid.addWidget(self.groupBoxKrdantaVidha, 2, 2)
        self.grid.addWidget(self.groupBoxKrdMode, 2, 3)
        self.mainLayout.addLayout(self.grid)
        self.grid.update()
        self.okBtn.setEnabled(True)
        self.cancelBtn.setEnabled(True)
    def optionGanas(self):
        self.mainOption = self.sender().text()
        try:
             if self.sender().isChecked():
                self.removeAllGroups()
                self.grid = QGridLayout(self)
                self.groupBoxGanas = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.Tganas, 'गणः', self.optionGanaSelected)
                self.grid.addWidget(self.groupBoxGanas, 2, 0)
                self.mainLayout.addLayout(self.grid)
                self.grid.update()
                self.okBtn.setEnabled(False)
                self.cancelBtn.setEnabled(True)
        except Exception as e:
             print('exception Ganas:%s' % e)
    def optionPadis(self):
        self.mainOption = self.sender().text()
        try:
            if self.sender().isChecked():
                self.removeAllGroups()
                self.grid = QGridLayout(self)
                self.groupBoxPadis = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.Tpadis, 'पदीः', self.optionPadiSelected)
                self.grid.addWidget(self.groupBoxPadis, 2, 0)
                self.mainLayout.addLayout(self.grid)
                self.grid.update()
                self.okBtn.setEnabled(False)
                self.cancelBtn.setEnabled(True)
        except Exception as e:
            print('exception Padis:%s' % e)
    def optionKarmas(self):
        self.mainOption = self.sender().text()
        try:
            if self.sender().isChecked():
                self.removeAllGroups()
                self.grid = QGridLayout(self)
                self.groupBoxPadis = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.Tkarmas, 'कर्मः', self.optionKarmaSelected)
                self.grid.addWidget(self.groupBoxPadis, 2, 0)
                self.mainLayout.addLayout(self.grid)
                self.grid.update()
                self.okBtn.setEnabled(False)
                self.cancelBtn.setEnabled(True)
        except Exception as e:
            print('exception Karmas:%s' % e)
    def optionIts(self):
        self.mainOption = self.sender().text()
        try:
            if self.sender().isChecked():
                self.removeAllGroups()
                self.grid = QGridLayout(self)
                self.groupBoxPadis = self.createOptionGroup(Kosha_Subanta_Krdanta_Tiganta.Tyits, 'इट्', self.optionItSelected)
                self.grid.addWidget(self.groupBoxPadis, 2, 0)
                self.mainLayout.addLayout(self.grid)
                self.grid.update()
                self.okBtn.setEnabled(False)
                self.cancelBtn.setEnabled(True)
        except Exception as e:
            print('exception Its:%s' % e)
    def optionGanaSelected(self):
        if self.sender().isChecked():
            self.gana = self.sender().text
            if not self.addedListview: self.listView_meanings = QListView(self)
            self.modelKrdanta_meanings = models.modelKrdanta_meanings()
            self.listView_meanings.setModel(self.modelKrdanta_meanings)
            self.listView_meanings.setUniformItemSizes(True)
            self.listView_meanings.setMaximumWidth(self.listView_meanings.sizeHintForColumn(0) + 125)
            # self.listView_meanings.setMaximumHeight(self.listView_meanings.sizeHintForRow(0) + 35)
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta_Tiganta.krdanta_Gana(self.gana)
            self.arthas = [transliterate_lines(item, IndianLanguages[self.script-1]) for item in self.arthas]
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), self.arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            if not self.addedListview:
                self.mainLayout.addWidget(self.listView_meanings)
                self.addedListview = True
            self.modelKrdanta_meanings.layoutChanged.emit()
            self.gridDisplay()
    def optionPadiSelected(self):
        if self.sender().isChecked():
            self.padi = self.sender().text
            if not self.addedListview: self.listView_meanings = QListView(self)
            self.modelKrdanta_meanings = models.modelKrdanta_meanings()
            self.listView_meanings.setModel(self.modelKrdanta_meanings)
            self.listView_meanings.setUniformItemSizes(True)
            self.listView_meanings.setMaximumWidth(self.listView_meanings.sizeHintForColumn(0) + 125)
            # self.listView_meanings.setMaximumHeight(self.listView_meanings.sizeHintForRow(0) + 35)
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta_Tiganta.krdanta_Padi(self.padi)
            self.arthas = [transliterate_lines(item, IndianLanguages[self.script-1]) for item in self.arthas]
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), self.arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            if not self.addedListview:
                self.mainLayout.addWidget(self.listView_meanings)
                self.addedListview = True
            self.modelKrdanta_meanings.layoutChanged.emit()
            self.gridDisplay()
    def optionKarmaSelected(self):
        if self.sender().isChecked():
            self.karma = self.sender().text
            if not self.addedListview: self.listView_meanings = QListView(self)
            self.modelKrdanta_meanings = models.modelKrdanta_meanings()
            self.listView_meanings.setModel(self.modelKrdanta_meanings)
            self.listView_meanings.setUniformItemSizes(True)
            self.listView_meanings.setMaximumWidth(self.listView_meanings.sizeHintForColumn(0) + 125)
            # self.listView_meanings.setMaximumHeight(self.listView_meanings.sizeHintForRow(0) + 35)
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta_Tiganta.krdanta_Karma(self.karma)
            self.arthas = [transliterate_lines(item, IndianLanguages[self.script-1]) for item in self.arthas]
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), self.arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            if not self.addedListview:
                self.mainLayout.addWidget(self.listView_meanings)
                self.addedListview = True
            self.modelKrdanta_meanings.layoutChanged.emit()
            self.gridDisplay()
    def optionItSelected(self):
        if self.sender().isChecked():
            self.it = self.sender().text
            if not self.addedListview: self.listView_meanings = QListView(self)
            self.modelKrdanta_meanings = models.modelKrdanta_meanings()
            self.listView_meanings.setModel(self.modelKrdanta_meanings)
            self.listView_meanings.setUniformItemSizes(True)
            self.listView_meanings.setMaximumWidth(self.listView_meanings.sizeHintForColumn(0) + 125)
            # self.listView_meanings.setMaximumHeight(self.listView_meanings.sizeHintForRow(0) + 35)
            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = Kosha_Subanta_Krdanta_Tiganta.krdanta_It(self.it)
            self.arthas = [transliterate_lines(item, IndianLanguages[self.script-1]) for item in self.arthas]
            self.modelKrdanta_meanings.data = list(map(lambda item: (False, item), self.arthas))
            # self.modelKrdanta_meanings.dataIscii = list(map(lambda item: (False, item[3]), arthas))
            if not self.addedListview:
                self.mainLayout.addWidget(self.listView_meanings)
                self.addedListview = True
            self.modelKrdanta_meanings.layoutChanged.emit()
            self.gridDisplay()
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
         status, self.arthas = self.modelKrdanta_meanings.data[row]
     else: status, self.arthas = self.modelKrdanta_meanings.data[0]
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
    '''def addDhatuTigantaGroups(self):
        DhatuVidha = ["केवलतिगंतः", "णिजन्तः", "सन्नन्तः"]
        self.groupBoxDhatuVidha = self.createOptionGroup(DhatuVidha, 'धातुविदाः', self.optionDhatuVidha)
        KrdVidha = ["कर्तरि", "कर्मणि"]
        self.groupBoxKrdantaVidha = self.createOptionGroup(KrdVidha, 'कृदंतविधाः', self.optionVoice)
        pratvidha = ["लट्", "लिट्", "लुट्", "लृट्", "लोट्", "लङ्", "विधिलिङ्", "अशीर्लिङ्", "लुङ्", "लृङ्"]
        self.groupBoxKrdMode = self.createOptionGroup(pratvidha, 'Krdanta Mode', self.optionLakara)
        self.KrdMode = "तव्य"
        self.grid.addWidget(self.groupBoxKrdantaVidha, 2, 1)
        self.grid.addWidget(self.groupBoxDhatuVidha, 2, 2)
        self.grid.addWidget(self.groupBoxKrdMode, 2, 3)'''
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
            dhatus, _, _, _, _ = Kosha_Subanta_Krdanta_Tiganta.tiganta_krdanta_arthas_karmas(self.tigantaWord, requested_script=self.script)
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
                self.okBtn.setEnabled(False)
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
                self.okBtn.setEnabled(False)
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
                self.okBtn.setEnabled(False)
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
                self.okBtn.setEnabled(False)
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
        self.syntaxButton.pressed.connect(self.syntaxAnalysis)

        self.formWidget_2.setVisible(False)
        self.formWidget_4.setVisible(False)
        self.formWidget_5.setVisible(False)
        self.synonymView.setVisible(False)

        for pg in [self.page1Button, self.page2Button, self.page3Button, self.page4Button, self.page5Button, self.page6Button,
                            self.page7Button, self.page8Button, self.page9Button, self.page10Button, self.page11Button,
                            self.page12Button, self.page13Button, self.page14Button, self.page15Button, self.page16Button,
                            self.page17Button, self.page18Button, self.page19Button, self.page20Button, self.page21Button, self.page22Button,
                            self.page23Button, self.page24Button]:
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
        cols, data = AmaraKosha_Database_Queries.tblSelectUnicode('Amara_Words', maxrows=0)
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
        self.syntaxButton.setEnabled(False)
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
        cols, data = AmaraKosha_Database_Queries.tblSelectUnicode('Subanta', maxrows=0, script=self.wanted_script + 1)
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
        try:
            cols, data = AmaraKosha_Database_Queries.tblSelectUnicode('Sdhatu', maxrows=0, script=self.wanted_script + 1)
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
            self.colsSdhatudata, self.Sdhatudata = AmaraKosha_Database_Queries.tblSelectUnicode('Sdhatu', maxrows=0, script=self.wanted_script + 1)
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
    # fname = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())
    # if fname[0]:
    #     f = open(fname[0], 'r')
        f = open('Bandarkar.txt', 'r')
        self.synonymsButton.setText('पदरूप विश्लेषण/ಪದರೂಪ ವಿಶ್ಲೇಷಣೆ/Morphological Analysis')
        # self.syntaxButton.setVisible(True)
        self.wanted_script = self.scriptSelector.currentIndex()
        self.listView.clicked.connect(self.enableSynonymsButton)
        with f:
            dataIscii = f.readlines()
            data = [Kosha_Subanta_Krdanta_Tiganta.transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(item), IndianLanguages[self.wanted_script]) for item in dataIscii]
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
                    status, self.amaraWord = self.modelDhatus.data[row]  #  dataIscii[row]
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
                    print('%s for amara word %s'%(e, self.amaraWord))  # AmaraKosha_Database_Queries.iscii_unicode(self.amaraWord)
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
                status, base = self.modelDhatus.data[row]
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
                    status, krdantaWord = self.modelDhatus.data[row]
                dialog = modalDialog_Krdanta(self, krdantaWord, self.wanted_script + 1)
                # print('%s DhatuVidhas %s KrdantaVidha %s Krdanta Mode %s'%(dialog.ok, dialog.DhatuVidah, dialog.KrdantaVidah, dialog.KrdMode))
                if dialog.okClicked:
                        if dialog.mainOption == 'Sorted List':
                            self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = \
                                Kosha_Subanta_Krdanta_Tiganta.tiganta_krdanta_arthas_karmas(krdantaWord)
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
                    status, tigantaWord = self.modelDhatus.data[row]
                    self.gana = self.Sdhatudata[row][self.colsSdhatudata.index('Field9')] // 100  # int(self.Sdhatudata[row][self.colsSdhatudata.index('Field9')][0])
                    self.padi = (self.Sdhatudata[row][self.colsSdhatudata.index('Field9')] % 100) // 10  #int(self.Sdhatudata[row][self.colsSdhatudata.index('Field9')][1])
                    self.it = self.Sdhatudata[row][self.colsSdhatudata.index('Field9')] % 10  #int(self.Sdhatudata[row][self.colsSdhatudata.index('Field9')][2])
                dialog = modalDialog_Tiganta(self, tigantaWord, requested_script=self.wanted_script+1)
                # print('%s DhatuVidhas %s KrdantaVidha %s Krdanta Mode %s'%(dialog.ok, dialog.DhatuVidah, dialog.KrdantaVidah, dialog.KrdMode))
                if dialog.okClicked:
                    if dialog.mainOption == 'Sorted List(अकारादि)':
                        self.arthas, self.karmas, self.dhatuNo, self.dataDhatu, self.cols_dataDhatu = \
                            Kosha_Subanta_Krdanta_Tiganta.tiganta_krdanta_arthas_karmas(tigantaWord)
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
            self.syntaxButton.setVisible(True)
            self.syntaxButton.setEnabled(True)
            self.wanted_script = self.scriptSelector.currentIndex()
            indexes = self.listView.selectedIndexes()
            if indexes:
                index = indexes[0]
                row = index.row()
                status, base = self.modelDhatus.data[row]
                try:
                    self.subforms, self.tigforms, self.krdforms = [], [], []
                    self.Subantas, self.Krdantas, self.Tigantas = [], [], []
                    syntaxInputFile, bas = [], base.strip()
                    listOfControls = [self.lblDhatu, self.txtDhatu, self.lblDhatvarya, self.txtDhatvarya, self.lblNijidhatu, self.txtNijiDhatu,
                                      self.lblSaniDhatu, self.txtSaniDhatu, self.lblGana, self.txtGana, self.lblPadi, self.txtPadi, self.lblKarma, self.txtKarma,
                                      self.lblIt, self.txtIt, self.lblDhatuVidah, self.txtDhatuVidah, self.lblKrdantaVidah_prayoga, self.txtKrdantaVidah_prayoga,
                                      self.lblPratyaya_lakara, self.txtPratyaya_lakara, self.lblAnta, self.txtAnta, self.lblLinga, self.txtLinga,
                                      self.lblPratipadika, self.txtPratipadika, self.lblSabda, self.txtSabda]
                    listofLbls = [self.lblDhatu, self.lblDhatvarya, self.lblNijidhatu, self.lblSaniDhatu, self.lblGana, self.lblPadi, self.lblKarma,
                                  self.lblIt, self.lblDhatuVidah, self.lblKrdantaVidah_prayoga, self.lblPratyaya_lakara, self.lblAnta, self.lblLinga,
                                  self.lblPratipadika, self.lblSabda]
                    # listofTxts = [self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu, self.txtGana, self.txtPadi, self.txtKarma,
                    #               self.txtIt, self.txtDhatuVidah, self.txtKrdantaVidah_prayoga, self.txtPratyaya_lakara, self.txtAnta, self.txtLinga,
                    #               self.txtPratipadika, self.txtSabda]
                    numpages = 0
                    for i, word in enumerate(bas.split(' ')):
                        if word.strip() == '': continue
                        wids = 1
                        try:
                            forms, subDetails = Kosha_Subanta_Krdanta_Tiganta.subanta_Analysis(word, self.wanted_script+1)
                            if not forms==[]: self.subforms += forms
                            for item in subDetails:
                                numpages += 1
                                # anta, linga, rupam, vibhakti, vacana, base, erb, det, vibvach = item.anta, item.linga, item.rupam, item.vib, item.vach, item.base, item.erb, item.det, item.vibvach
                                self.Subantas.append([item.rupam, transliterate_lines(item.base,
                                                     IndianLanguages[self.wanted_script]), item.anta, item.linga, item.vib, item.vach, item.vibvach])
                                syntaxInputFile.append([i+1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 1, AmaraKosha_Database_Queries.unicode_iscii(item.base), AmaraKosha_Database_Queries.unicode_iscii(item.erb), item.det, item.vibvach + 1])
                                # ic.ic('subanta', i+1, word, wids, item.det, AmaraKosha_Database_Queries.iscii_unicode(word))
                                wids += 1
                            self.setTexts(zip([self.lblDhatu, self.txtDhatu, self.lblDhatvarya, self.txtDhatvarya, self.lblNijidhatu, self.txtNijiDhatu,
                                               self.lblSaniDhatu, self.txtSaniDhatu, self.lblGana, self.txtGana, self.lblPadi, self.txtPadi], ['रूपं', self.Subantas[0][0], 'प्रातिपदिकं', self.Subantas[0][1], 'अंतः', self.Subantas[0][2], 'लिंगः', self.Subantas[0][3],
                               'विभक्तिः', self.Subantas[0][4], 'वचनः', self.Subantas[0][5]]))
                            for lbl in listofLbls: lbl.setText(transliterate_lines(lbl.text(), IndianLanguages[self.wanted_script]))
                            self.Categories.setText(transliterate_lines('सुबंतः', IndianLanguages[self.wanted_script]))
                            for control in listOfControls[12:]: control.setVisible(False)
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
                            forms, krdData = Kosha_Subanta_Krdanta_Tiganta.krdanta_Analysis(word, self.wanted_script + 1)
                            if not forms == []: self.krdforms += forms
                            if not krdData == []:
                                self.Krdantas += krdData
                                numpages += len(krdData)
                                for krdDetail in krdData:
                                    # ic.ic('krdanta', i+1, word, wids)
                                    syntaxInputFile.append(
                                        [i + 1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 2, krdDetail.erb_iscii, krdDetail.sabda_iscii,
                                         krdDetail.det,
                                         krdDetail.vibvach + 1, krdDetail.ddet, krdDetail.Dno, krdDetail.verb_iscii,
                                         krdDetail.nijverb_iscii,
                                         krdDetail.sanverb_iscii, krdDetail.meaning_iscii, krdDetail.GPICode,
                                         krdDetail.CombinedM, krdDetail.karmaCode])
                                    wids += 1
                        except Exception as e:
                            print(e)
                        try:
                            forms, tigDatas = Kosha_Subanta_Krdanta_Tiganta.tiganta_Analysis(word, self.wanted_script + 1)
                            if not forms==[]: self.tigforms += forms
                            if not tigDatas == []:
                                self.Tigantas += tigDatas
                                numpages += len(tigDatas)
                                for tigData in tigDatas:
                                    # ic.ic('tiganta', i+1, word, wids)
                                    syntaxInputFile.append([i+1, AmaraKosha_Database_Queries.unicode_iscii(word), wids, 5, tigData.base_iscii, tigData.Dno, tigData.verb_iscii,
                                                            tigData.nijverb_iscii, tigData.sanverb_iscii, tigData.meaning_iscii,
                                                            ('%03d'%tigData.GPICode), tigData.pralak, tigData.purvach,
                                                            tigData.CombinedM, tigData.karmaCode])
                                    wids += 1
                        except Exception as e:
                            print(e)
                    # ic.ic(bas, numpages)
                    # ic.ic(self.Subantas, self.subforms, [tig.get() for tig in self.Tigantas], self.tigforms, [tig.get() for tig in self.Krdantas], self.krdforms)

                    for control in [self.page1Button, self.page2Button, self.page3Button, self.page4Button, self.page5Button, self.page6Button,
                                    self.page7Button, self.page8Button, self.page9Button, self.page10Button, self.page11Button,
                                    self.page12Button, self.page13Button, self.page14Button, self.page15Button, self.page16Button,
                                    self.page17Button, self.page18Button, self.page19Button, self.page20Button, self.page21Button, self.page22Button,
                                    self.page23Button, self.page24Button][:numpages]:
                        control.setEnabled(True)
                        control.setVisible(True)
                    for control in [self.page1Button, self.page2Button, self.page3Button, self.page4Button, self.page5Button, self.page6Button,
                                    self.page7Button, self.page8Button, self.page9Button, self.page10Button, self.page11Button,
                                    self.page12Button, self.page13Button, self.page14Button, self.page15Button, self.page16Button,
                                    self.page17Button, self.page18Button, self.page19Button, self.page20Button,
                                    self.page21Button, self.page22Button, self.page23Button, self.page24Button][numpages:]:
                        control.setEnabled(False)
                        control.setVisible(False)
                    # fOSOut = open('OSOut.Aci', 'w')
                    # fOSOut.write('ÔÚ³èÍÌè -- %s\n' % bas)
                    # for line in syntaxInputFile:
                    #     fOSOut.write('%d) ' % line[0])
                    #     for element in line[1:]: fOSOut.write('%s ' % element)
                    #     fOSOut.write('\n')
                    # fOSOut.write('----------\n')
                    # fOSOut.close()
                    self.syntaxInputFile = ['ÔÚ³èÍÌè -- %s' % AmaraKosha_Database_Queries.unicode_iscii(bas)]
                    for line in syntaxInputFile:
                        self.syntaxInputFile.append('%d) '%line[0] + ' '.join([str(x) for x in line[1:]]))
                    self.syntaxInputFile.append('----------')

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
            indx = ['page1Button', 'page2Button', 'page3Button', 'page4Button', 'page5Button', 'page6Button', 'page7Button',
                    'page8Button', 'page9Button', 'page10Button',  'page11Button', 'page12Button',  'page13Button',
                    'page14Button', 'page15Button', 'page16Button', 'page17Button','page18Button',  'page19Button',
                    'page20Button',  'page21Button', 'page22Button',  'page23Button', 'page24Button'
                    ].index(self.sender().objectName())
            listOfControls = [self.lblDhatu, self.txtDhatu, self.lblDhatvarya, self.txtDhatvarya, self.lblNijidhatu, self.txtNijiDhatu,
                              self.lblSaniDhatu, self.txtSaniDhatu, self.lblGana, self.txtGana, self.lblPadi, self.txtPadi,
                              self.lblKarma, self.txtKarma, self.lblIt, self.txtIt, self.lblDhatuVidah, self.txtDhatuVidah,
                              self.lblKrdantaVidah_prayoga, self.txtKrdantaVidah_prayoga, self.lblPratyaya_lakara, self.txtPratyaya_lakara,
                              self.lblAnta, self.txtAnta, self.lblLinga, self.txtLinga, self.lblPratipadika, self.txtPratipadika,
                              self.lblSabda, self.txtSabda]
            listofLbls = [self.lblDhatu, self.lblDhatvarya, self.lblNijidhatu, self.lblSaniDhatu, self.lblGana,  self.lblPadi,  self.lblKarma,
                          self.lblIt,  self.lblDhatuVidah,  self.lblKrdantaVidah_prayoga, self.lblPratyaya_lakara, self.lblAnta, self.lblLinga,
                          self.lblPratipadika, self.lblSabda]
            listofTxts = [self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu, self.txtGana,  self.txtPadi,  self.txtKarma,
                          self.txtIt,  self.txtDhatuVidah,  self.txtKrdantaVidah_prayoga, self.txtPratyaya_lakara,  self.txtAnta, self.txtLinga,
                          self.txtPratipadika, self.txtSabda]
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
                if self.Categories.text() == 'Syntax':
                    self.modelFinalResults._data = pandas.DataFrame(self.conclusions[indx]['cells'],
                                            columns=[transliterate_lines(category, IndianLanguages[self.wanted_script]) for category in ['', '', 'लिंग',  'विभक्ति',  'वचन' ]],
                                            index=[' '] * len(self.conclusions[indx]['cells']))
                    for i, conclusion in enumerate(self.conclusions[indx]['conclusions']):
                        listofTxts[i].setText(conclusion)
                        listofTxts[i].setVisible(True)
                    for control in listofLbls: control.setVisible(False)
                    for control in listofTxts[i + 1:]: control.setVisible(False)
                    numpages = min(len(self.conclusions)-1, 21)
                    # ic.ic(self.conclusions[indx]['conclusions'], len(self.conclusions))
                    for control in [self.page1Button, self.page2Button, self.page3Button, self.page4Button, self.page5Button, self.page6Button,
                            self.page7Button, self.page8Button, self.page9Button, self.page10Button, self.page11Button,
                            self.page12Button, self.page13Button, self.page14Button, self.page15Button, self.page16Button,
                            self.page17Button, self.page18Button, self.page19Button, self.page20Button, self.page21Button, self.page22Button,
                            self.page23Button, self.page24Button][:numpages]:
                        control.setEnabled(True)
                        control.setVisible(True)
                else:
                    subantas, tigantas, krdantas = ['सुबंतः'] * len(self.Subantas), ['तिगंतः'] * len(self.Tigantas), ['कृदंतः'] * len(self.Krdantas)
                    lst = subantas + tigantas + krdantas
                    self.Categories.setText(transliterate_lines(lst[indx], IndianLanguages[self.wanted_script]))
                    if self.Categories.text() == transliterate_lines('सुबंतः', IndianLanguages[self.wanted_script]): #indx == 0:
                        for control in [self.synonymView, self.formWidget_2] + listOfControls[:11]: control.setVisible(True)
                        for control in listOfControls[12:]: control.setVisible(False)
                        self.setTexts(zip(listofLbls[:6],
                                          [transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in
                                           ['रूपं', 'प्रातिपदिकं', 'अंतः', 'लिंगः', 'विभक्तिः', 'वचनः']]))
                        self.setTexts(zip([self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu, self.txtGana, self.txtPadi],
                                          self.Subantas[indx][:-1]))
                        for r in range(len(self.subforms)):
                            for c in range(3):
                                if self.subforms[r][c][0] == '(': self.subforms[r][c] = self.subforms[r][c][1:-1]
                        r, c = indx * 8 + (self.Subantas[indx][-1]) // 3, (self.Subantas[indx][-1]) % 3
                        if r > len(self.subforms): r = (self.Subantas[indx][-1]) // 3
                        # ic.ic(self.Categories.text(), len(self.subforms), self.subforms, self.Subantas[indx][-1], r, c)
                        if self.subforms[r][c][0] != '(': self.subforms[r][c] = '(' + self.subforms[r][c] + ')'
                        if indx > len(self.subforms) // 8 - 1: indx = len(self.subforms) // 8 - 1
                        self.modelFinalResults._data = pandas.DataFrame(self.subforms[indx * 8: indx * 8 + 8],
                                                                    columns=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vacanas],
                                                                    index=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vibhaktis])
                    elif self.Categories.text() == transliterate_lines('तिगंतः', IndianLanguages[self.wanted_script]): #indx in [1,2]:
                        indx = indx - len(subantas)
                        for control in listOfControls: control.setVisible(True)
                        self.setTexts(zip(listofLbls[:10], [transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in
                                       ['धातुः','धात्वर्य:','णिजि धातु:','सनि धातु:','गण:','पदिः','कर्मः','इट्','धातुविधः','प्रयोगः','लकारः']]))
                        self.setTexts(zip([self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu,
                             self.txtGana, self.txtPadi, self.txtKarma, self.txtIt, self.txtDhatuVidah,
                             self.txtKrdantaVidah_prayoga, self.txtPratyaya_lakara],
                            [transliterate_lines(txt, IndianLanguages[self.wanted_script]) for txt in
                             [self.Tigantas[indx].verb, self.Tigantas[indx].base,self.Tigantas[indx].nijverb, self.Tigantas[indx].sanverb,
                              self.Tigantas[indx].gana,self.Tigantas[indx].padi, self.Tigantas[indx].karma, self.Tigantas[indx].it,
                              self.Tigantas[indx].dhatuVidah, self.Tigantas[indx].voice, self.Tigantas[indx].lakara]]
                        ))
                        self.Categories.setText(transliterate_lines('तिगंतः', IndianLanguages[self.wanted_script]))
                        for control in listOfControls[22:]: control.setVisible(False)
                        for lbl in listofLbls: lbl.setText(transliterate_lines(lbl.text(), IndianLanguages[self.wanted_script]))
                        for r in range(len(self.tigforms)):
                            for c in range(3):
                                if self.tigforms[r][c][0] == '(': self.tigforms[r][c] = self.tigforms[r][c][1:-1]
                        r, c = indx * 3 + (self.Tigantas[indx].purvach - 1) // 3, (self.Tigantas[indx].purvach - 1) % 3
                        if self.tigforms[r][c] != '(': self.tigforms[r][c] = '(' + self.tigforms[r][c] + ')'
                        self.modelFinalResults._data = pandas.DataFrame(self.tigforms[indx * 3: indx * 3 + 3],
                                                                    columns=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.vacanas],
                                                                    index=[transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in Kosha_Subanta_Krdanta_Tiganta.purushas])
                    elif self.Categories.text() == transliterate_lines('कृदंतः', IndianLanguages[self.wanted_script]):
                        indx = indx - len(subantas) - len(tigantas)
                        self.setTexts(zip(listofLbls, [transliterate_lines(item, IndianLanguages[self.wanted_script]) for item in
                                   ['धातुः','धात्वर्य:','णिजि धातु:','सनि धातु:','गण:','पदिः','कर्मः','इट्','धातुविधः','कृदंतविधः','प्रत्ययः','अंतः','लिंगः','प्रातिपदिकं','रूपं']]))
                        ind = min(indx, len(self.Krdantas) - 1)
                        strt = min(indx * 8, len(self.krdforms) - 8)
                        krdData = self.Krdantas[ind]
                        for r in range(len(self.krdforms)):
                            for c in range(3):
                                if self.krdforms[r][c][0] == '(': self.krdforms[r][c] = self.krdforms[r][c][1:-1]
                        r, c = strt + (krdData.vibvach - 1) // 3, (krdData.vibvach - 1) % 3
                        if self.krdforms[r][c][0] != '(': self.krdforms[r][c] = '(' + self.krdforms[r][c] + ')'
                        self.setTexts(zip(listofTxts, [krdData.verb, krdData.meaning, krdData.nijverb, krdData.sanverb, krdData.gana, krdData.padi,
                                                       krdData.karma, krdData.it,  krdData.dhatuVidhah, krdData.krdantaVidhah, krdData.pratyayaVidhah,
                                                       krdData.anta, krdData.linga, krdData.sabda,
                                                       self.krdforms[ind][0]]))
                        for lbl in listofLbls: lbl.setText(transliterate_lines(lbl.text(), IndianLanguages[self.wanted_script]))
                        for control in listOfControls: control.setVisible(True)
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
            self.setTexts(zip([self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu,
                 self.txtGana, self.txtPadi, self.txtKarma, self.txtIt, self.txtDhatuVidah,
                 self.txtKrdantaVidah_prayoga, self.txtPratyaya_lakara, self.txtSabda, self.txtAnta, self.txtLinga,
                 self.txtPratipadika],
                [self.krdData[0].verb, transliterate_lines(dialog.arthas, IndianLanguages[self.wanted_script]), self.krdData[0].nijverb,
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
            self.setTexts(zip([self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu,
                 self.txtGana, self.txtPadi, self.txtKarma, self.txtIt, self.txtDhatuVidah,
                 self.txtKrdantaVidah_prayoga, self.txtPratyaya_lakara],
                [transliterate_lines(txt, IndianLanguages[self.wanted_script]) for txt in [dialog.tigantaWord, dialog.arthas,
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
    def syntaxAnalysis(self):
        self.synonymsButton.setEnabled(False)
        typeList = ['Noun(s)', 'Pronoun(s)', 'Adjective(s)', 'Krdanta(s)', 'KrdAvyaya(s)', 'Avyaya(s)']
        subtypeList = ['Subject(s)', 'Object(s)', 'Instrument(s)', 'Dative(s)', 'Ablative(s)', 'Genitive(s)', 'Locative(s)', 'Vocative(s)', 'Verb(s)', 'Verb']
        edges, set_edge_labels = {}, []
        font_prop = FontProperties(fname='NotoSansDevanagari-Regular.ttf', size=12)
        try:
            # out = SyntaxAnalysis.write_out_aci('OSOut.aci', outfile='out.aci')
            out = SyntaxAnalysis.write_out_aci(self.syntaxInputFile) #, outfile='out.aci')
            result = SyntaxAnalysis.write_result_aci(out)  #, resultfile='result.aci')
            # fresult = open('result.aci', 'r')
            # result = fresult.readlines()
            self.conclusions, sentence_no = [{'cells':[], 'conclusions':[]}], 0
            graphs = []
            plt.close()
            for line_no, line in enumerate(result):
                line = line.replace('\t', '').replace('\n', '').strip()
                words = line.split(' ')
                word = words[0]
                # if word == "ÔÚ³èÍÌè": sentence = line
                # if word in ["ÔÚ³èÍÌè", "", "The"] or "VOICE" in word or "can be assumed to be the" in line: pass
                if word == AmaraKosha_Database_Queries.unicode_iscii('वाक्यम्'): sentence = AmaraKosha_Database_Queries.iscii_unicode(line[line.index(' -- ') + 4:line.index(' (')])
                if word in [AmaraKosha_Database_Queries.unicode_iscii('वाक्यम्'), ""] or (len(words) == 1 and word == "subject"): pass
                elif word == "The" or "VOICE" in words or "Considering the verb" in line: self.conclusions[sentence_no]['conclusions'].append(line)
                elif any([phrase in line for phrase in ["can be assumed to be the", "Any subanta"]]):
                    cell = transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(line), IndianLanguages[self.wanted_script])
                    edges['Subject(s)'] = [cell.split()[0], '', '', '']
                    self.conclusions[sentence_no]['conclusions'].append(cell)
                elif any([phrase in line for phrase in ["Verb is", "No matching subject is available", "Considering krdanta", "There is an object"]]): self.conclusions[sentence_no]['conclusions'].append(line)
                elif word in typeList:
                    if len(words) <= 1: parts = ''
                    else: parts = line[line.index(' ( ') + 2:].split(' / ')
                    if parts == '': self.conclusions[sentence_no]['cells'].append([word, '', '', '', ''])
                    else:
                        cell = [transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(w), IndianLanguages[self.wanted_script]) for w in [word, words[2], parts[0], parts[1], parts[2][:-2]]]
                        self.conclusions[sentence_no]['cells'].append(cell)
                        w = line[:line.index(' ( ')].split(' : ')[1]
                        edges[word] = transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(w), IndianLanguages[self.wanted_script])
                        edges[word] = [edges[word]] + cell[1:]
                elif word in subtypeList or 'Verb(s) are : ' in result[line_no - 1]:
                    parts = line[line.index(' ( ') + 2:].split(' / ')
                    if 'Verb(s) are : ' in result[line_no - 1]: word = 'Verb(s)'
                    cell = [transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(w), IndianLanguages[self.wanted_script]) for w in [word, words[2], parts[0], parts[1], parts[2][:-2]]]
                    w = line[line.index(' '):line.index(' ( ')]
                    if w[0] == ':': w = w[1:]
                    edges[word] = transliterate_lines(AmaraKosha_Database_Queries.iscii_unicode(w), IndianLanguages[self.wanted_script])
                    edges[word] = [edges[word]] + cell[1:]
                    self.conclusions[sentence_no]['cells'].append(cell)
                elif word[0] == '-':
                    self.conclusions.append({'cells':[], 'conclusions':[]})
                    sentence_no += 1
                    if 'Verb' in edges.keys():
                        graph, edge_labels = self.karakaGraph(edges)
                        if edge_labels not in set_edge_labels:
                            set_edge_labels.append(edge_labels)
                            graphs.append((graph, edge_labels))
                    edges = {}
                # elif 'Verb(s) are : ' in result[line_no - 1]: pass
                else: raise NameError(line + '-' + word + ' -> Invalid Category')
            self.modelFinalResults._data = pandas.DataFrame(self.conclusions[0]['cells'],
                                            columns=[transliterate_lines(category, IndianLanguages[self.wanted_script]) for category in ['', '',  'लिंग',  'विभक्ति',  'वचन' ]],
                                            index=[' '] * len(self.conclusions[0]['cells'])) #[transliterate_lines(role, IndianLanguages[self.wanted_script]) for role in subtypeList[:5]])
            self.Categories.setText('Syntax')
            listOfControls = [self.lblDhatu, self.txtDhatu, self.lblDhatvarya, self.txtDhatvarya, self.lblNijidhatu, self.txtNijiDhatu,
                              self.lblSaniDhatu, self.txtSaniDhatu, self.lblGana, self.txtGana, self.lblPadi, self.txtPadi,
                              self.lblKarma, self.txtKarma, self.lblIt, self.txtIt, self.lblDhatuVidah, self.txtDhatuVidah,
                              self.lblKrdantaVidah_prayoga, self.txtKrdantaVidah_prayoga, self.lblPratyaya_lakara, self.txtPratyaya_lakara,
                              self.lblAnta, self.txtAnta, self.lblLinga, self.txtLinga, self.lblPratipadika, self.txtPratipadika,
                              self.lblSabda, self.txtSabda]
            listofLbls = [self.lblDhatu, self.lblDhatvarya, self.lblNijidhatu, self.lblSaniDhatu, self.lblGana, self.lblPadi, self.lblKarma,
                          self.lblIt, self.lblDhatuVidah, self.lblKrdantaVidah_prayoga, self.lblPratyaya_lakara, self.lblAnta, self.lblLinga,
                          self.lblPratipadika, self.lblSabda]
            listofTxts = [self.txtDhatu, self.txtDhatvarya, self.txtNijiDhatu, self.txtSaniDhatu, self.txtGana, self.txtPadi, self.txtKarma,
                          self.txtIt, self.txtDhatuVidah, self.txtKrdantaVidah_prayoga, self.txtPratyaya_lakara, self.txtAnta, self.txtLinga,
                          self.txtPratipadika, self.txtSabda]
            for i, conclusion in enumerate(self.conclusions[0]['conclusions']): listofTxts[i].setText(conclusion)
            for control in listofLbls: control.setVisible(False)
            for control in listofTxts[i + 1:]: control.setVisible(False)
            self.conclusions = [item for item in self.conclusions if not (item['cells'] == [] and item['conclusions'] == [])]
            numpages = min(len(self.conclusions), 21)
            for control in [self.page1Button, self.page2Button, self.page3Button, self.page4Button, self.page5Button, self.page6Button,
                            self.page7Button, self.page8Button, self.page9Button, self.page10Button, self.page11Button,
                            self.page12Button, self.page13Button, self.page14Button, self.page15Button, self.page16Button,
                            self.page17Button, self.page18Button, self.page19Button, self.page20Button, self.page21Button, self.page22Button,
                            self.page23Button, self.page24Button][:numpages]:
                control.setEnabled(True)
                control.setVisible(True)

            self.modelFinalResults.layoutChanged.emit()

            no_of_subplots = 100 + len(graphs) * 10
            for subplot_no, (graph, edge_labels) in enumerate(graphs):
                subax = plt.subplot(no_of_subplots + subplot_no + 1)
                pos = nx.spring_layout(graph)
                nx.draw(graph, pos, with_labels=True, font_family='Mangal')
                nx.draw_networkx_edge_labels(graph, pos, font_family='Mangal', edge_labels=edge_labels)
            plt.axis('off')
            plt.title(sentence, fontproperties=font_prop)
            plt.show()
        except Exception as e:
            self.statusBar().showMessage(str(e))
    def karakaGraph(self, interpretation):
        g = nx.Graph()
        edge_labels = {}
        for k, v in interpretation.items():
                if v[0] != '':
                    g.add_node(v[0])
                    if k != 'Verb': g.nodes[v[0]]['role'], g.nodes[v[0]]['linga'], g.nodes[v[0]]['vibhakti'], g.nodes[v[0]]['vacana'] = k, v[1], v[2], v[3]
                    else:  g.nodes[v[0]]['role'], g.nodes[v[0]]['purusha'], g.nodes[v[0]]['vacana'] = k, v[2], v[3]
        for k, v in interpretation.items():
            if k != 'Verb':
                g.add_edge(interpretation['Verb'][0], interpretation[k][0])
                edge_labels[(interpretation['Verb'][0], interpretation[k][0])] = k
        return g, edge_labels
logging.basicConfig(level=logging.DEBUG, filename='../../Amarakosha.log', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
