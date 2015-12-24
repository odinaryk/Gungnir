from PyQt4 import QtGui
import json
import sys
import os
import item_get
import webbrowser
Pic_dir='cache'
class QtItemLayout(QtGui.QGridLayout):

	def __init__(self,item):
		super(QtItemLayout,self).__init__()
		self.data=item
		self.initUI()

	def initUI(self):
		picture=QtGui.QLabel()
		picture.setPixmap(QtGui.QPixmap(os.path.join(Pic_dir,self.data['picture'])).scaled(150,150))
		name=QtGui.QLabel(self.data['name'])
		name.adjustSize()
		name.setGeometry(0,0,150,150)
		name.setWordWrap(True)
		price=QtGui.QLabel("Price: "+self.data['price'])
		rate=QtGui.QLabel("Rate: "+self.data['rate'])
		sale=QtGui.QLabel("Sale: "+self.data['sale'])
		rsl=QtGui.QHBoxLayout()
		rsl.addWidget(rate)
		rsl.addWidget(sale)
		viewSource=QtGui.QPushButton("View Source")
		viewSource.clicked.connect(self.web)
		self.setSpacing(10)
		self.addWidget(picture,1,0)
		self.addWidget(name,2,0)
		self.addWidget(price,3,0)
		self.addLayout(rsl,4,0)
		self.addWidget(viewSource)
	def web(self):
		webbrowser.open(self.data['source'])

class QtItemBox(QtGui.QWidget):
	def __init__(self,itemList):
		super(QtItemBox,self).__init__()
		self.data=itemList
		self.items=[]
		self.ibox=QtGui.QGridLayout()
		self.initUI()
	def initUI(self):
		for item in self.data:
			self.items.append(QtItemLayout(item))
		self.ibox.setSpacing(10)
		for i in range(len(self.items)):
			self.ibox.addLayout(self.items[i],i/4,i%4)
		self.setLayout(self.ibox)
		self.setGeometry(600,600,600,600)

def testItem():
	app = QtGui.QApplication(sys.argv)
	data=json.load(open('test.json','r'))
	x=QtItem(data[0])
	sys.exit(app.exec_())

def testItemBox():
	app = QtGui.QApplication(sys.argv)
	data=json.load(open('test.json','r'))
	x=QtItemBox(data)
	sys.exit(app.exec_())

def testGetShow():
	app = QtGui.QApplication(sys.argv)
	data=item_get.get_items('K701')
	x=QtItemBox(data)
	sys.exit(app.exec_())
