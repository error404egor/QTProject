from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QGridLayout

def addToFreezer(Widget, layout, name="товар не опознан", img="./IMG/NoPhoto.png"):
    layout_of_frame = QGridLayout(Widget)

    frame = QFrame(Widget)
    frame.setLayout(layout_of_frame)
    frame.setMinimumHeight(100)
    btn_delete = QPushButton(Widget)
    btn_delete.setText("Удалить")
    btn_delete.setFixedSize(100, 50)
    btn_delete.setStyleSheet("background-color: rgb(255, 255, 255);")
    lable_of_product = QLabel()
    pixmap_of_product = QPixmap(img)
    lable_of_product.setPixmap(pixmap_of_product)
    lable_of_product.setFixedSize(50, 50)
    name_of_product = QLabel()
    name_of_product.setText(name)
    name_of_product.setFixedHeight(50)
    btn_edite = QPushButton()
    btn_edite.setText("Удалить")
    btn_edite.setFixedSize(100, 50)
    btn_edite.setStyleSheet("background-color: rgb(255, 255, 255);")
    layout_of_frame.addWidget(lable_of_product, 1, 1)
    layout_of_frame.addWidget(name_of_product, 1, 3)
    layout_of_frame.addWidget(btn_edite, 1, 5)
    layout_of_frame.addWidget(btn_delete, 1, 6)
    
    layout.addWidget(frame)