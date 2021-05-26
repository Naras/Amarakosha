__author__ = 'NarasMG'

import pandas
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
tick = QtGui.QImage('tick.png')

class modelDhatus(QtCore.QAbstractListModel):
    def __init__(self, *args, data=None, **kwargs):
        super(modelDhatus, self).__init__(*args, **kwargs)
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
class modelFinalResults_DataFrame(QtCore.QAbstractTableModel):
    def __init__(self, data=pandas.DataFrame([[]], columns=[], index=[])):
        super(modelFinalResults_DataFrame, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        # if role == Qt.ForegroundRole:
        #     value = self._data.iloc[index.row(), index.column()]
        #     if value != None and value[0] == '(' and value[len(value) - 1] == ')': return QtGui.QColor('blue')

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

