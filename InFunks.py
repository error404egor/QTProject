from os import error
from PIL.Image import new
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton, QGridLayout
from product_detection import *
from alwaysInFreezerListFunks import addAllProductsToToBuyList
import shutil
from constants import HeightOfFrame, SizeOfWidgets, EditBtnWidth, DeleteBtnWidth


class prevText(): # класс для хранения предыдущего текста
    def __init__(self, text):
        self.t = text

    def change(self, text):
        self.t = text

    def text(self):
        return self.t

def deleteAll(Widget, layout): # удаляет все frame из layoutа
    for i in reversed(range(1, layout.count())): 
        layout.itemAt(i).widget().deleteLater()

def reload(Widget, layout, layout2): # функция перезагрузки
    deleteAll(Widget, layout)
    deleteAll(Widget, layout2)
    addAllToFreezer(Widget, layout, layout2)

def reloadfunk(Widget, layout, layout2): # функция, возвращающая функцию перезагрузки с всталенными параметрами
    def r():
        reload(Widget, layout, layout2)
    return r

def addAllToFreezer(Widget, layout, layout2): #добавляет все продукты в "в холодильнике"
    clearinfreezerdb()
    inFreezerProducts = infreezerdetection()
    for shelf, products in inFreezerProducts.items():
        for photo, maxindex, maxindexphoto, name in products:
            addToFreezer(Widget, layout, shelf, name=name,
            img=os.path.join("./infreezerIMG", shelf, photo),
             maxindex=maxindex, maxindexphoto=maxindexphoto)
            putproducttoinfreezerdb(name, shelf)
    addAllProductsToToBuyList(Widget, layout2)

#добавляет рвмку с апродуктом в "в холодильнике"
def addToFreezer(Widget, layout, shelf, name="товар не опознан",
    img="./IMG/NoPhoto.png", maxindex=0, maxindexphoto=None, editon=True):
    def delete(): # удаляет рамку
        frame.deleteLater()
        os.remove(img)


    def edite(): # открывает редактирования
        btn_approve.setDisabled(False)
        btn_disgard.setDisabled(False)
        name_of_product.setDisabled(False)
        btn_edite.setDisabled(True)
        lastname.change(name_of_product.text())


    def approve():
        # проверка имени на присутствие только доопустимых символов
        if rightFormatOfName(name_of_product.text()) != 0:
            return -1
        # устанавливаем неактивность редактирорвания
        btn_disgard.setDisabled(True)
        btn_approve.setDisabled(True)
        name_of_product.setDisabled(True)
        btn_edite.setDisabled(False)
        # приводим к правильному формату(все маленькими буквами, вместо ё используестя е)
        name_of_product.setText("".join(list(map(lambda x: "е" if x == "ё" else x, 
         list(name_of_product.text().lower())))))
        # проверка на пустую строку
        if name_of_product.text().split() == []:
            delete()
        else:
            # изменение текста на слова, разделенныйе пробелами
            name_of_product.setText(" ".join(name_of_product.text().split()))
            # проверка существования папки с данным типом продуктов(если ее нет, то создает)
            if not os.path.exists(os.path.join("./pics_of_products", name_of_product.text())):
                os.mkdir(os.path.join("./pics_of_products", name_of_product.text()))
            # проверка на почти идентичность фото, распознанную, как самая похожая в бд(100 - % совпадения средних хешей)
            if maxindex != 100: # добавляет клпию фото рассматривоемого продукта в бд и папку фото-образцов, добавляет объект в холодильник
                newimgadress = (name_of_product.text() +
                 str(len(os.listdir(os.path.join("./pics_of_products", name_of_product.text())))))
                newimgadress = newname(newimgadress, os.path.splitext(img)[1], 
                 os.path.join("./pics_of_products", name_of_product.text()))
                shutil.copyfile(img, newimgadress)
                putproducttodbbyfile(newimgadress)
                putproducttoinfreezerdb(name_of_product.text(), shelf)
            else: # перемещает идентичную фото в папку с именем объекта, меняет ее адрес в бд 
                newimgadress = (name_of_product.text() +
                 str(len(os.listdir(os.path.join("./pics_of_products", name_of_product.text())))))
                newimgadress = newname(newimgadress, os.path.splitext(img)[1], 
                 os.path.join("./pics_of_products", name_of_product.text()))
                shutil.copyfile(maxindexphoto, newimgadress)
                os.remove(maxindexphoto)
                updateproductindb(maxindexphoto, newimgadress)
                putproducttoinfreezerdb(name_of_product.text(), shelf)
                putproducttoinfreezerdb(lastname.text(), shelf, count=-1)
            # создание новой рамки и удаление старой
            newframe = getMaxInAllFolders(newimgadress)
            addToFreezer(Widget, layout, shelf, name=newframe[2],
                img=img, 
                maxindex=newframe[0], maxindexphoto=newframe[1], editon=False)
            frame.deleteLater()


    def disgard(): # возвращает значения на значения до редактирования
        btn_disgard.setDisabled(True)
        btn_approve.setDisabled(True)
        name_of_product.setDisabled(True)
        btn_edite.setDisabled(False)
        name_of_product.setText(lastname.text())
        approve()
    # Создаем рамку и описываем ее
    layout_of_frame = QGridLayout(Widget)
    frame = QFrame(Widget)
    frame.setLayout(layout_of_frame)
    frame.setMinimumHeight(HeightOfFrame)
    btn_delete = QPushButton(frame)
    btn_delete.setText("Удалить")
    btn_delete.setFixedSize(DeleteBtnWidth, SizeOfWidgets)
    btn_delete.setStyleSheet("background-color: rgb(255, 255, 255);")
    lable_of_product = QLabel(frame)
    pixmap_of_product = QPixmap(img).scaled(SizeOfWidgets, SizeOfWidgets, 
        aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
    lable_of_product.setPixmap(pixmap_of_product)
    lable_of_product.setFixedSize(SizeOfWidgets, SizeOfWidgets)
    name_of_product = QLineEdit(frame)
    name_of_product.setDisabled(not editon)
    name_of_product.setText(name)
    name_of_product.setFixedHeight(SizeOfWidgets)
    btn_disgard = QPushButton(frame)
    btn_disgard.setStyleSheet("background-color: red;")
    btn_disgard.setDisabled(not editon)
    btn_disgard.setText(u"\u2718")
    btn_approve = QPushButton(frame)
    btn_approve.setStyleSheet("background-color: green;")
    btn_approve.setDisabled(not editon)
    btn_approve.setText(u"\u2713")
    btn_edite = QPushButton(frame)
    btn_edite.setText("Редактировать")
    btn_edite.setFixedSize(EditBtnWidth, SizeOfWidgets)
    btn_edite.setStyleSheet("background-color: rgb(255, 255, 255);")
    btn_edite.setDisabled(editon)
    btn_delete.clicked.connect(delete)
    btn_edite.clicked.connect(edite)
    btn_approve.clicked.connect(approve)
    btn_disgard.clicked.connect(disgard)
    layout_of_frame.addWidget(lable_of_product, 1, 1)
    layout_of_frame.addWidget(btn_approve, 1, 4)
    layout_of_frame.addWidget(btn_disgard, 1, 5)
    layout_of_frame.addWidget(name_of_product, 1, 3)
    layout_of_frame.addWidget(btn_edite, 1, 6)
    layout_of_frame.addWidget(btn_delete, 1, 7)
    # добавляем рамку в layout
    layout.addWidget(frame)
    # создаем значение предыдущего текста на текущий(для disgard)
    lastname = prevText(name_of_product.text())