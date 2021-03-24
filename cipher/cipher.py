from PyQt5 import QtWidgets, QtCore, QtGui
import random
import time

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.setWindowTitle('Шифрователь - 3000')
        self.setWindowIcon(QtGui.QIcon("lockIco.ico"))
        self.resize(400,20)
        
        self.line = QtWidgets.QLineEdit('Введите строку')
        self.line.editingFinished.connect(self.CheckLine)
        vbox = QtWidgets.QVBoxLayout()
        hbox = QtWidgets.QHBoxLayout()
        
        self.btnOk = QtWidgets.QPushButton('Start')
        self.btnOk.clicked.connect(self.CheckBtn)

        self.btnDic = QtWidgets.QPushButton('Help')
        self.btnDic.clicked.connect(self.Dictionary)

        vbox.addWidget(self.line)
        vbox.addWidget(self.btnDic)
        vbox.addWidget(self.btnOk)
        

        self.tupEngU = []

        self.tupRusU = []

        self.specialSymbols = [' ','-','+','=','_']
        
        for i in range(10):
            self.specialSymbols.append(str(i))
        self.tupRusL = ['а', 'б', 'в', 'г', 'д', 'е',
                           'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р',
                           'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь',
                           'э', 'ю', 'я']
        self.tupEngL = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
                        'p','q','r','s','t','u','v','w','x','y','z']
        for i in range(len(self.tupRusL)):
            self.tupRusU.append(self.tupRusL[i].upper())
        for i in range(len(self.tupEngL)):
            self.tupEngU.append(self.tupEngL[i].upper())



        self.setLayout(vbox)
        self.show()

    def Dictionary(self):
        text = 'Rus:'
        for i in self.tupRusL:
            text += f' {i}'
        text += '\nEng:'
        for i in self.tupEngL:
            text += f' {i}'
        text += '\nSpec:'
        for i in self.specialSymbols:
            text += f' {i}'
        text += '\nСправка: Шиврователь шифрует введенное вами слово, после чего вам надо угадать N(сдвиг по словарю).\nНа угадывание слова вам дается 3 попытки по 20 секунд.'
        dialogElse = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                                         'Dictionary',
                                                         text,
                                                         QtWidgets.QMessageBox.Ok)
        dialogElse.setWindowIcon(QtGui.QIcon("lockIco.ico"))
        return dialogElse.exec()
    def SearchIndex(self, arr, sym):
        for i in range(len(arr)):
            if arr[i] == sym:
                ind = i
        return ind
    
    def CheckLine(self):
        text = self.line.text()

    def CheckAnswer(self):
            text = '' 
            
            try:
                if int(self.lineDialog.text()) == int(self.N):
                    text = 'Правильно!'
            except BaseException:
                pass

            if time.time() - self.time > 20:
                text = 'Время вышло!'
                self.dialog.reject()
                
            elif self.count >= 3:
                text = 'Попытки закончились!'
                self.dialog.reject()
                
            if text == '':
                text = 'Неправильно!'
                self.count += 1
                self.time = time.time()
                
            dialogElse = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                                         'Attention',
                                                         text,
                                                         QtWidgets.QMessageBox.Ok)
                
            dialogElse.setWindowIcon(QtGui.QIcon("lockIco.ico"))
            dialogElse.exec_()
            if text == 'Правильно!':
                self.dialog.reject()


    def CheckBtn(self):
        self.N = random.randint(2, 9)
        print(f'Answer :{self.N}')
        self.text = self.line.text()
        if self.text == '':
            return
        self.count = 0

        self.newtext = ''
        for symbol in self.text:
            if symbol in self.tupRusL:
                ind = self.SearchIndex(self.tupRusL, symbol) + self.N
                if ind >= len(self.tupRusL):
                    ind -= len(self.tupRusL)
                self.newtext += self.tupRusL[ind]
            
            if symbol in self.tupRusU:
                ind = self.SearchIndex(self.tupRusU, symbol) + self.N
                if ind >= len(self.tupRusU):
                    ind -= len(self.tupRusU)
                self.newtext += self.tupRusU[ind]
            
            if symbol in self.tupEngL:
                ind = self.SearchIndex(self.tupEngL, symbol) + self.N
                if ind > len(self.tupEngL):
                    ind -= len(self.tupEngL)
                self.newtext += self.tupEngL[ind]

            if symbol in self.tupEngU:
                ind = self.SearchIndex(self.tupEngU, symbol) + self.N
                if ind >= len(self.tupEngU):
                    ind -= len(self.tupEngU)
                self.newtext += self.tupEngU[ind]
            if symbol in self.specialSymbols:
                ind = self.SearchIndex(self.specialSymbols, symbol) + self.N
                if ind >= len(self.specialSymbols):
                    ind -= len(self.specialSymbols)
                self.newtext += self.specialSymbols[ind]

        self.time = time.time()
        
        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowIcon(QtGui.QIcon("lockIco.ico"))
        self.dialog.setWindowTitle('Введите N')
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.label = QtWidgets.QLabel(f'{self.text} \n to \n{self.newtext}')
        
        self.lineDialog = QtWidgets.QLineEdit()
        self.lineDialog.setInputMask("9;")
        self.btnDialog = QtWidgets.QPushButton('Ok')
        self.btnDialog.clicked.connect(self.CheckAnswer)
        
        
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.lineDialog)
        vbox.addWidget(self.btnDialog)
        self.dialog.setLayout(vbox)



        self.dialog.exec_()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
