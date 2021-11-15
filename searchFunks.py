from InFunks import deleteAll, HeightOfFrame, SizeOfWidgets
from product_detection import rightFormatOfName
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel
import sqlite3


def search(name): # поиск по имени в 'продуктах в холодильнике'
    if rightFormatOfName(name) == -1: # проверка на правильность формата
        return []
    if name.split() == []: # проверка на пустую строку
        return []
    name = " ".join("".join(list(map(lambda x: "е" if x == "ё" else x, 
         list(name.lower())))).split())
    con = sqlite3.connect("./freezer.db")
    search_result = con.cursor().execute("""SELECT * FROM infreezer 
     WHERE productname = ?""", (name, )).fetchall()
    con.commit()
    con.close()
    return search_result


def addAllToSearchResultsList(Widget, layout, name): # добавляет все товары в приложение в "поиск"
    deleteAll(Widget, layout)
    for product, shelf, count in search(name):
        addToSearchResultsList(Widget, layout, product, shelf, count)


def addToSearchResultsList(Widget, layout, product, shelf, count): # добавляет товар в приложение в "поиск"
    layout_of_frame = QGridLayout()
    frame = QFrame(Widget)
    frame.setMinimumHeight(HeightOfFrame)
    name_of_product = QLabel(frame)
    name_of_product.setText(product + " найден " + """на полке '""" + shelf + """' """ + "в количестве " + str(count))
    name_of_product.setFixedHeight(SizeOfWidgets)
    layout_of_frame.addWidget(name_of_product, 1, 1)
    frame.setLayout(layout_of_frame)
    layout.addWidget(frame)