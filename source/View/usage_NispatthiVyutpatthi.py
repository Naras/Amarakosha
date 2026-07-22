
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QRadioButton, QGridLayout, QGroupBox, QHBoxLayout, QListView, QFileDialog

def Nishpatthi(self):
    # self.nishpathiButton.setEnabled(False)
    self.nishpathiButton.setStyleSheet('QPushButton::enabled""{""background-color : ' + self.theme + ';""}')
    indexes = self.listView.selectedIndexes()
    if indexes:
        index = indexes[0]
        row = index.row()
        try:
            status, self.amaraWord = self.modelDhatus.data[row]
            nishpatthi = Kosha_Subanta_Krdanta_Tiganta.nishpatthi(transliterate_lines(self.amaraWord, IndianLanguages[0]))  # don't ask for non-devanagari script, invalid results!
            if len(nishpatthi) > 0:
                txtNishpatthi = '\n'.join([item[0] for item in nishpatthi])
                self.txtNishpatthi.setText(transliterate_lines(txtNishpatthi, self.wanted_script))
                self.autoResize(self.txtNishpatthi)
                self.lblNishpatthi.setVisible(True)
                self.txtNishpatthi.setVisible(True)
                self.lblNishpatthi.setText(transliterate_lines('निश्पत्ति', self.wanted_script))
        except Exception as e:
                self.statusBar().showMessage('Nishpatthi:%s'%e)
def Vyutpatthi(self):
    # self.vyutpathiButton.setEnabled(False)
    self.vyutpathiButton.setStyleSheet('QPushButton::enabled""{""background-color : ' + self.theme + ';""}')
    indexes = self.listView.selectedIndexes()
    if indexes:
        index = indexes[0]
        row = index.row()
        try:
            status, self.amaraWord = self.modelDhatus.data[row]
            vyupatthi = Kosha_Subanta_Krdanta_Tiganta.vyutpatthi(transliterate_lines(self.amaraWord, IndianLanguages[0]),
                                                                    ['Sanskrit', 'Hindi', 'Odiya'][self.vyutpathiSelector.currentIndex()])
            if len(vyupatthi) > 0:
                txtNishpatthi = '\n'.join([item[0] for item in vyupatthi])
                self.txtNishpatthi.setText(transliterate_lines(txtNishpatthi, self.wanted_script))
                self.autoResize(self.txtNishpatthi)
                self.lblNishpatthi.setVisible(True)
                self.txtNishpatthi.setVisible(True)
                self.lblNishpatthi.setText(transliterate_lines('व्युत्त्पत्ति', self.wanted_script))
        except Exception as e:
                self.statusBar().showMessage('Vyutpatthi:%s'%e)
 