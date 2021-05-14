import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
sys.path.append(os.getcwd())
from source.Model import AmaraKosha_Database_Queries
# from source.Controller import Transliterate
import pandas

from source.Model.AmaraKosha_Database_Queries import isascii
qt_creator_file = os.path.join(os.getcwd(), "source/View", "browseTables_uiComposition.xml")
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
'''
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
'''

class modelContent_DataFrame(QtCore.QAbstractTableModel):

    def __init__(self, data=pandas.DataFrame([[]], columns=[], index=[])):
        super(modelContent_DataFrame, self).__init__()
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
        self.tableView.setUniformItemSizes(True)
        self.tableView.setMaximumWidth(self.tableView.sizeHintForColumn(0) + 150)
        self.modelTable = modelSchema()
        self.modelContent = modelContent_DataFrame()
        self.load()
        self.browseButton.pressed.connect(self.browseTable)
        self.deleteButton.pressed.connect(self.deleteRow)
        self.deleteRowsButton.pressed.connect(self.deleteRows)
        self.exitButton.pressed.connect(QtWidgets.qApp.quit)
        self.tableView.setModel(self.modelTable)
        self.contentView.setModel(self.modelContent)
        self.contentView.clicked.connect(self.detectCell)

    def load(self):
        try:
            self.modelTable.tables = list(map(lambda x: (False,x), AmaraKosha_Database_Queries.schemaParse()))
        except Exception as e:
            print(e)
    def browseTable(self):
        scriptSelect = self.languageSelector.currentIndex()
        indexes = self.tableView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, self.tbl = self.modelTable.tables[row]
            # self.modelContent._data = list(cli_browse.tblSelect(tbl))
            self.cols, dbdata = AmaraKosha_Database_Queries.tblSelect(self.tbl, maxrows=0, duplicate=True) #, script=int(scriptSelect)+1)
            # print('%s\n%s' % (cols, dbdata))
            # try:
            #     rows = []
            #     for item in dbdata:
            #         rowofcols = []
            #         for col in item:
            #             if isascii(str(col)): x = col
            #             else: x = Transliterate.transliterate_lines(col, Transliterate.IndianLanguages[scriptSelect])
            #             rowofcols.append(x)
            #         rows.append(rowofcols)
            # except Exception as e:
            #     print(e)
            self.modelContent._data = pandas.DataFrame(dbdata,columns=self.cols)
            self.modelContent.layoutChanged.emit()
    def detectCell(self, item):
        try:
            indexes = self.contentView.selectedIndexes()
            # print('clicked cell: row %s col %s value %s'%(item.row(), item.column(), self.modelContent.data(indexes[0], Qt.DisplayRole)))
            self.rowId = self.modelContent.data(indexes[0], Qt.DisplayRole)
            if str(self.deleteFrom.text()).strip() in ['', '?']: self.deleteFrom.setText(self.rowId)
            else: self.deleteTo.setText(self.rowId)
            self.colname = self.cols[item.column()]
        except Exception as e:
            print(e)
    def deleteRow(self):
        qry = 'delete * from ' + self.tbl + ' where ' + self.colname + '=?'
        print('sql qry = %s id=%s'%(qry, self.rowId))
        try:
            delcursor = AmaraKosha_Database_Queries.conn.cursor()
            delcursor.execute(qry, self.rowId)
            delcursor.commit
            delcursor.close()
            qry = 'select * from ' + self.tbl + ' where ' + self.colname + '=?'
            cols, result = AmaraKosha_Database_Queries.sqlQuery(qry, param=self.rowId, duplicate=False)
            print('cols %s\nresult %s'%(cols,result))  # should be empty
        except Exception as e:
            print(e)

    def deleteRows(self):
        qry = 'delete * from ' + self.tbl + ' where ' + self.colname + ' between ' + self.deleteFrom.text() + ' and ' + self.deleteTo.text()
        print('sql qry = %s'%(qry))
        try:
            delcursor = AmaraKosha_Database_Queries.conn.cursor()
            delcursor.execute(qry)
            delcursor.commit
            delcursor.close()
            qry = 'select * from ' + self.tbl + ' where ' + self.colname + ' between ' + self.deleteFrom.text() + ' and ' + self.deleteTo.text()
            cols, result = AmaraKosha_Database_Queries.sqlQuery(qry, duplicate=False)
            print('cols %s\nresult %s'%(cols,result))  # should be empty
            self.deleteFrom.setText('?')
            self.deleteTo.setText('?')
        except Exception as e:
            print(e)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()


