# This Python file uses the following encoding: utf-8
from InFunks import * 
from PyQt5.QtWidgets import QLCDNumber, QWidget, QSpinBox
from PyQt5 import uic
from PyQt5 import *
import csv
from constants import CsvFileDelimetr, CsvFileNewLine, CsvFile, HeightOfFrame, SizeOfWidgets


class EditeList: #класс для генирации списка 
    def __init__(self): # создает словарь
        self.d = {}

    def put(self, elem, count): # добовляет значение в словарь
        if rightFormatOfName(elem) == 0: # проверка на правильный формат
            elem = "".join(list(map(lambda x: "е" if x == "ё" else x, list(elem.lower())))) # вместо ё е, нижний регистр, список из слов названия
            # проверка на пустую строку
            if elem.split() == [] or count == 0: # проверка на ноль
                return 0
            elem = " ".join(elem.split()) # соединение названия через 1 пробел
            
            if self.isInList(elem):
                self.d[elem] += count # добавление к предыдущему значению
            else:
                self.d[elem] = count # создание значения
        else:
            return -1

    def isInList(self, elem): # проверка, есть ли в списке елемент
        return elem in self.d.keys()

    def addListToCsv(self): # записывает список в csv файл
        addingLsit = []
        for product, count in self.d.items():
            addingLsit.append([product, str(count)])
        writecsv(addingLsit)
        


class WidgetEditor(QWidget): # редактор списка
    def __init__(self):
        super(WidgetEditor, self).__init__()
        uic.loadUi("listedit.ui", self)
        addAllToList(self, self.layout_, readcsv()) # добавляет в приложение в  "список покупок"
        self.add.clicked.connect(lambda: addByUser(self, self.layout_)) # добавление пользователем при нажатии кнопки
        self.ready.clicked.connect(lambda: ready(self.layout_, self)) # созранение при нажатии ок


def openeditor(): # открытие редактора списка
    widget = WidgetEditor()
    widget.show()


def ready(layout_, Widget):
    editingList = EditeList() # создание списка
    for i in reversed(range(1, layout_.count())): # обход по рамкам в layoutе
        product = layout_.itemAt(i).widget().layout().itemAt(0).widget().text() # название продукта в рамке
        count = layout_.itemAt(i).widget().layout().itemAt(1).widget().value() # количество продукта в рамке
        returned = editingList.put(product, count)
        if returned == -1:
            return -1
    editingList.addListToCsv() # запись списка в CSV файл
    Widget.deleteLater()
    Widget.close()


def addToList(Widget, layout, product="", count=0): # добавление прлодукта в layout 
    layout_of_frame = QGridLayout()
    frame = QFrame(Widget)
    frame.setMinimumHeight(HeightOfFrame)
    name_of_product = QLineEdit(frame)
    name_of_product.setText(product)
    name_of_product.setFixedHeight(SizeOfWidgets)
    count_of_product = QSpinBox(frame)
    count_of_product.setFixedHeight(SizeOfWidgets)
    count_of_product.setMinimum(0)
    count_of_product.setValue(count)
    layout_of_frame.addWidget(name_of_product, 1, 1)
    layout_of_frame.addWidget(count_of_product, 1, 4)
    frame.setLayout(layout_of_frame)
    layout.addWidget(frame)

def addAllToList(Widget, layout, products): # добавляет несколько рамок в layout
    for product, count in products:
        addToList(Widget, layout, product=product, count=int(count))


def readcsv(): # чтение CSV файла
    with open(CsvFile, "r", newline=CsvFileNewLine, encoding='UTF8') as file:
        reader = csv.reader(file, delimiter=CsvFileDelimetr)
        return list(reader)


def writecsv(elems): #
    with open(CsvFile, "w", newline=CsvFileNewLine, encoding='UTF8') as file:
        writer = csv.writer(file, delimiter=CsvFileDelimetr)
        writer.writerows(elems)

def addByUser(Widget, layout):
    addToList(Widget, layout)


def toBuyList():
    toBuyList_ = []
    for product, count in readcsv():
        count = int(count)
        if count > allShelfsCount(product):
            toBuyList_.append((product, count - allShelfsCount(product), ))
    return toBuyList_


def addAllProductsToToBuyList(Widget, layout):
    for product, count in toBuyList():
        addProductToToBuyList(Widget, layout, product, count)


def addProductToToBuyList(Widget, layout, product, count):
    layout_of_frame = QGridLayout()
    frame = QFrame(Widget)
    frame.setMinimumHeight(100)

    name_of_product = QLabel(frame)
    name_of_product.setText(product)
    name_of_product.setFixedHeight(50)
    count_of_product = QLCDNumber()
    count_of_product.setFixedHeight(50)
    count_of_product.display(count)
    layout_of_frame.addWidget(name_of_product, 1, 1)
    layout_of_frame.addWidget(count_of_product, 1, 2)

    frame.setLayout(layout_of_frame)
    layout.addWidget(frame)


if __name__ == '__main__':
    print(readcsv())
    print(writecsv([["bebra", "5"], ["aboba", "2"], ["boris", "1"], ["noskin", "6"], ["pubg", "2"]])) 
    openeditor()