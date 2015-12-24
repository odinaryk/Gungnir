#encoding=utf-8
import sys,os
import item_get,item_show
import json
from PyQt4 import QtCore, QtGui
import time
import advance
pic_Dir='cache'
misc_Dir='misc'
class Window(QtGui.QMainWindow):
	def __init__(self):
		super(Window,self).__init__()
		self.itembox=QtGui.QWidget()
		self.initUI()

	def initUI(self):
		self.setFixedSize(750,900)
		grid=QtGui.QGridLayout()
		grid.setSpacing(25)
		widget=QtGui.QWidget()
		self.setCentralWidget(widget)
		bg=QtGui.QPixmap(os.path.join(misc_Dir,'background.jpg'))
		palette1=QtGui.QPalette()
		palette1.setBrush(widget.backgroundRole(),QtGui.QBrush(bg))
		self.setPalette(palette1)
		self.setAutoFillBackground(True)
		self.logo=QtGui.QLabel('',self)
		self.logo.setPixmap(QtGui.QPixmap(os.path.join(misc_Dir,'logo.png')).scaled(300,135))
		self.logo.setGeometry(225,225,300,135)
		layout=QtGui.QGridLayout(self)
		self.button(layout)
		widget.setLayout(layout)
		self.menu()
		self.setWindowIcon(QtGui.QIcon(os.path.join(misc_Dir,'icon.png')))
		self.setWindowTitle('Gungnir')
		self.show()

	def menu(self):
		self.statusBar()
		menubar=self.menuBar()

		fileMenu=menubar.addMenu('&File')
		self.SaveAction=QtGui.QAction(self.tr("Save"),self)
		self.SaveAction.setShortcut("Ctrl+S")
		self.SaveAction.triggered.connect(self.saveData)
		self.AnalysisAction=QtGui.QAction(self.tr("Analysis"),self)
		self.AnalysisAction.triggered.connect(self.analysisHistory)
		self.ExitAction=QtGui.QAction(self.tr("Exit"),self)
		self.ExitAction.setShortcut("Ctrl+Q")
		self.ExitAction.triggered.connect(QtGui.qApp.quit)		
		fileMenu.addAction(self.SaveAction)
		fileMenu.addAction(self.ExitAction)
		fileMenu.addAction(self.AnalysisAction)

		fileMenu=menubar.addMenu('&Sort')
		self.PriceAction=QtGui.QAction(self.tr("Price"),self)
		self.RateAction=QtGui.QAction(self.tr("Rate"),self)
		self.SaleAction=QtGui.QAction(self.tr("Sale"),self)
		fileMenu.addAction(self.PriceAction)
		fileMenu.addAction(self.RateAction)
		fileMenu.addAction(self.SaleAction)
		self.connect(self.PriceAction,QtCore.SIGNAL("triggered()"),self.priceSort)
		self.connect(self.RateAction,QtCore.SIGNAL("triggered()"),self.rateSort)
		self.connect(self.SaleAction,QtCore.SIGNAL("triggered()"),self.saleSort)

		fileMenu=menubar.addMenu('&About')
		self.HelpAction=QtGui.QAction(self.tr("Help"),self)
		self.HelpAction.setShortcut("Ctrl+H")
		self.connect(self.HelpAction,QtCore.SIGNAL("triggered()"),self.help)
		self.AboutAction=QtGui.QAction(self.tr("About us"),self)
		self.connect(self.AboutAction,QtCore.SIGNAL("triggered()"),self.about)
		fileMenu.addAction(self.HelpAction)
		fileMenu.addAction(self.AboutAction)

	def help(self):
		reply=QtGui.QMessageBox.about(self,"Help","1. Enter goodsname to search in the LineEdit\n2. Press Search button or Press Enter to Search\n3. File\\save to save data for analyze\n4. File\\analyze to draw history average price graph(Automatically save current data)\n5. View Sort menu to sort the items in respective order")

	def about(self):
		reply=QtGui.QMessageBox.about(self,"About",u"Version 1.0,2015-12-24\nRelease under GPL 3.0\nContributors(unordered):\n樊泽坤,计婷,徐瑾卿,楼思琦")

	def button(self,layout):
		self.SearchTable=QtGui.QLineEdit()
		self.connect(self.SearchTable, QtCore.SIGNAL("returnPressed()"), self.search)
		SearchButton=QtGui.QPushButton("search")
		SearchButton.clicked.connect(self.search)
		layout.addWidget(self.SearchTable,0,0)
		layout.addWidget(SearchButton,0,1)
	def search(self):
		self.goodsname=self.SearchTable.text().__str__()
		self.data=item_get.get_items(self.goodsname)
		self.logo.hide()
		self.renewIbox()
	def renewIbox(self):
		self.centralWidget().layout().removeWidget(self.itembox)
		self.itembox.deleteLater()
		self.itembox=item_show.QtItemBox(self.data)
		self.centralWidget().layout().addWidget(self.itembox,1,0)
	def priceSort(self):
		self.data.sort(key=lambda x:float(x['price']))
		self.renewIbox()
	def rateSort(self):
		self.data.sort(key=lambda x:x['rate'],reverse=True)
		self.renewIbox()
	def saleSort(self):
		self.data.sort(key=lambda x:float(x['sale']),reverse=True)
		self.renewIbox()
	def saveData(self):
		advance.saveprice(self.data,self.goodsname)
		QtGui.QMessageBox.about(self,"Success",u"Successfully Saved:\n"+self.goodsname)
	def analysisHistory(self):
		advance.saveprice(self.data,self.goodsname)
		advance.drawpic(self.goodsname)
def main():
	dirlist=[pic_Dir,misc_Dir]
	for d in dirlist:
		if not os.path.exists(d):
			os.mkdir(d)
	app=QtGui.QApplication(sys.argv)
	win=Window()
	sys.exit(app.exec_())

if __name__=='__main__':
	main()