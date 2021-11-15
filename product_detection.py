import os
from PIL import Image
from PIL import UnidentifiedImageError
import imagehash
import sqlite3
from PyQt5.QtWidgets import QMessageBox

def allShelfsCount(name): # считает количество имеющегося товара, вне зависимости от полки
    con = sqlite3.connect("./freezer.db")
    count = con.cursor().execute("""SELECT productcount FROM infreezer 
     WHERE productname = ?""", (name,)).fetchall()
    con.commit()
    con.close()
    if count == []:
        return 0
    else:
        return sum(list(map(lambda x: int(x[0]), count)))


def newname(img, ext, folder): # создает уникальное имя файлу
    while img + ext in os.listdir(folder):
        img += "n"
    return os.path.join(folder, img + ext)

def ifInFreezer(name, shelf): # проверяет, есть ли этот продукт в бд infreezer
    con = sqlite3.connect("./freezer.db")
    count = con.cursor().execute("""SELECT productcount FROM infreezer 
     WHERE productname = ? and productshelf = ?""", (name, shelf)).fetchone()
    con.commit()
    con.close()
    if count == None:
        return None
    else:
        return count[0]

def getproduct(src_pic, src_0):
    try:
        hash0 = getproducthashfromdb(src_0)
        hash1 = imagehash.average_hash(Image.open(src_pic)) 
    except UnidentifiedImageError or TypeError:
        return (0, "", )
    return (100 - (hash1 - hash0), src_0)

def putproducttodbbyfile(file):
    try:
        hash = imagehash.average_hash(Image.open(file))
        putproducttodb(file, hash)
    except UnidentifiedImageError and TypeError and sqlite3.IntegrityError:
        pass

def updateproductindb(src, newsrc):
    con = sqlite3.connect("./freezer.db")
    con.cursor().execute("""UPDATE hashes
     SET filepath = ?
     WHERE filepath = ?""", (newsrc, src))
    con.commit()
    con.close()

def updateproductininfreezerdb(name, shelf, count):
    con = sqlite3.connect("./freezer.db")
    con.cursor().execute("""UPDATE infreezer
     SET productcount = ?
     WHERE productshelf = ? and productname = ?""", (count, shelf, name, ))
    con.commit()
    con.close()

def putproducttoinfreezerdb(name, shelf, count=1):
    con = sqlite3.connect("./freezer.db")
    countBefore = ifInFreezer(name, shelf)
    if countBefore == None:
        con.cursor().execute("""INSERT INTO infreezer(productname, 
        productshelf, productcount) VALUES(?, ?, ?);""", (name, shelf, count))
        con.commit()
        con.close()
    else:
        con.commit()
        con.close()
        count += countBefore
        updateproductininfreezerdb(name, shelf, count)

def putproducttodb(src, hash):
    hash = str(hash)
    con = sqlite3.connect("./freezer.db")
    con.cursor().execute("""INSERT INTO hashes(filepath, filehash) VALUES(?, ?);""", (src, hash))
    con.commit()
    con.close()

def getproducthashfromdb(src):
    con = sqlite3.connect("./freezer.db")
    hash = con.cursor().execute("""SELECT filehash FROM hashes WHERE filepath = ?""", (src, )).fetchone()
    con.commit()
    con.close()
    hash = imagehash.hex_to_hash(hash[0])
    return hash

def getmaxinfolder(src_pic, directory):
    percents_of_folder = {}
    for filename in os.listdir(directory):
        if not filename.startswith('.'):
            file_percent = getproduct(src_pic, os.path.join(directory, filename))
            percents_of_folder[file_percent[0]] = file_percent
        else:
            pass
    return percents_of_folder[max(percents_of_folder.keys())]

def getMaxInAllFolders(src_pic, directory="./pics_of_products"):
    maxpercents_of_folders = {}
    for foldername in os.listdir(directory):
        if (os.path.isfile(os.path.join(directory, foldername)) or
         len(tuple(filter(lambda file: not file.startswith('.'),
         os.listdir(os.path.join(directory, foldername))))) == 0):
            continue
        folder_max = getmaxinfolder(src_pic, os.path.join(directory, foldername))
        maxpercents_of_folders[folder_max[0]] = (*folder_max, foldername, )
    maxpercent = maxpercents_of_folders[max(maxpercents_of_folders.keys())]
    return maxpercent

def infreezerdetection (directory="./infreezerIMG"):
    infreezerdetection = {}
    for foldername in os.listdir(directory):
        if (os.path.isfile(os.path.join(directory, foldername)) or
         len(tuple(filter(lambda file: not file.startswith('.'),
         os.listdir(os.path.join(directory, foldername))))) == 0):
            continue
        infreezerdetection[foldername] = infreezerdetectioninfolder(os.path.join(directory, foldername))
    return infreezerdetection
        

def infreezerdetectioninfolder(directory):
    infreezerproducts = []
    for filename in os.listdir(directory):
        if not filename.startswith('.'):
            infreezerproducts.append((filename, *getMaxInAllFolders(os.path.join(directory, filename)), ))
    return infreezerproducts

def clearinfreezerdb():
    con = sqlite3.connect("./freezer.db")
    con.cursor().execute("""DELETE from infreezer where True""")
    con.commit()
    con.close()

def cleardb():
    con = sqlite3.connect("./freezer.db")
    con.cursor().execute("""DELETE from hashes where True""")
    con.commit()
    con.close()

def setupdb(directory="./pics_of_products"):
    for foldername in os.listdir(directory):
        if os.path.isfile(foldername):
            continue
        for filename in os.listdir(os.path.join(directory, foldername)):
            fileway = os.path.join(directory, foldername, filename)
            if os.path.isdir(fileway):
                continue
            try:
                hash = imagehash.average_hash(Image.open(fileway))
            except UnidentifiedImageError:
                continue
            try:
                putproducttodb(fileway, hash)
            except sqlite3.IntegrityError:
                pass


def rightFormatOfName(text):
    if not all(x.isalpha() or x.isspace() or x.isdigit() for x in text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("В названии есть недопустимые символы")
        msg.setInformativeText("Допустивы только цифры, буквы и пробелы")
        msg.setWindowTitle("Ошибка")
        msg.exec_()
        return -1
    else:
        return 0

def restartdb():
    cleardb()
    setupdb()

def main():
    restartdb()
    print(infreezerdetection())
    print(ifInFreezer("aboba", "2"))
    print(ifInFreezer("bebra", "1"))
    print(ifInFreezer("kek", "1"))
    putproducttoinfreezerdb("aboba", "2", count=10)
    putproducttoinfreezerdb("bebra", "1")
    putproducttoinfreezerdb("kek", "1", count=2)

if __name__ == '__main__':
    main()