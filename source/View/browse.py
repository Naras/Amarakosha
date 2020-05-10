import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from source.Model import cli_browse

qt_creator_file = "mainwindow_uiComposition.xml"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)
tick = QtGui.QImage('tick.png')


class modelSchema(QtCore.QAbstractListModel):
    def __init__(self, *args, tables=None, **kwargs):
        super(modelSchema, self).__init__(*args, **kwargs)
        self.tables = tables or []
    def data(self, index, role):
        if role == Qt.DisplayRole:
            _, text = self.tables[index.row()]
            return text
        if role == Qt.DecorationRole:
            status, _ = self.tables[index.row()]
            if status:
                return tick
    def rowCount(self, index):
        return len(self.tables)

class modelContent(QtCore.QAbstractTableModel):
    def __init__(self, data=None):
        super(modelContent, self).__init__()
        self._data = data or [[]]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Get the raw value
            return self._data[index.row()][index.column()]
    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.modelTable = modelSchema()
        # self.modelContent = contentModel()
        self.modelContent = modelContent()
        self.load()
        self.browseButton.pressed.connect(self.browseTable)
        self.exitButton.pressed.connect(QtWidgets.qApp.quit)
        self.tableView.setModel(self.modelTable)
        # self.contentView.setModel(self.modelContent)
        self.contentView.setModel(self.modelContent)

    def load(self):
        try:
            self.modelTable.tables = list(map(lambda x: (False,x), cli_browse.schemaParse()))
        except Exception as e:
            print(e)
    def browseTable(self):
        indexes = self.tableView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status,tbl = self.modelTable.tables[row]
            # self.modelTable.tables[row] = (True, tbl)
            # self.modelTable.layoutChanged.emit()
            # self.modelContent.content = list(map(lambda x: (False,x), cli_browse.tblSelect(tbl)))
            self.modelContent._data = list(cli_browse.tblSelect(tbl))
            # print(self.modelContent._data)
            self.modelContent.layoutChanged.emit()
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()


