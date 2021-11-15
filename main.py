# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtGui import QIcon, QKeySequence
from InFunks import * 
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QShortcut
from PyQt5 import uic
from PyQt5 import *
from alwaysInFreezerListFunks import openeditor
from product_detection import *
from searchFunks import *

def areAllFilesReady(): # проверяет все ли нужные файлы присутствуют
    thisdir = "./"
    if not ("IMG" in os.listdir(thisdir)):
        return False
    elif not ("NoPhoto.png" in os.listdir(os.path.join(thisdir, "IMG"))):
        return False
    elif not ("infreezerIMG" in os.listdir(thisdir)):
        return False
    elif not ("form.ui" in os.listdir(thisdir)):
        return False
    elif not ("listedit.ui" in os.listdir(thisdir)):
        return False
    elif not ("freezer.db" in os.listdir(thisdir)):
        return False
    elif not ("alwaysinfreezerlist.csv" in os.listdir(thisdir)):
        return False
    elif not ("searchFunks.py" in os.listdir(thisdir)):
        return False
    elif not ("product_detection.py" in os.listdir(thisdir)):
        return False
    elif not ("InFunks.py" in os.listdir(thisdir)):
        return False
    elif not ("alwaysInFreezerListFunks.py" in os.listdir(thisdir)):
        return False
    else:
        try:
            getMaxInAllFolders(os.path.join(thisdir, "IMG", "NoPhoto.png"))
        except ValueError:
            return False
    return True


class Widget(QWidget):
    def __init__(self):
        restartdb() # перезагружаем бд
        super(Widget, self).__init__()
        uic.loadUi("form.ui", self)
        self.reload.setIcon(QIcon("./IMG/reload.svg")) # ставим иконку кнопке перезагрузки
        self.reload.clicked.connect(reloadfunk(self, self.inFreezerLayout,
         self.listtobuylayout)) # перезагружаем при нажатии
        self.edit.clicked.connect(openeditor)
        self.searchButton.clicked.connect(lambda: addAllToSearchResultsList(self,
         self.searchlayout, self.searchEditLine.text())) # ищем при нажатии кнопки поиска
        addAllToFreezer(self, self.inFreezerLayout, self.listtobuylayout) # добавляет все продукты в бд и приложение
        self.reload_hotkew = QShortcut(QKeySequence('Ctrl+R'), self) # перезагрузка по горячим клавишам
        self.reload_hotkew.activated.connect(reloadfunk(self,
         self.inFreezerLayout, self.listtobuylayout))


if __name__ == "__main__":
    if areAllFilesReady(): # если все файлы нам месте, то запускает программу, иначе - выдает ошибку
        app = QApplication(sys.argv)
        widget = Widget()
        widget.show()
        sys.exit(app.exec_())
    else:
        app = QApplication(sys.argv)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Ошибка")
        msg.setInformativeText('Есть недостоющие файлы. переустановите программу.')
        msg.setWindowTitle("Ошибка")
        msg.show()
        sys.exit(app.exec_())
