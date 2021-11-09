import os
from PIL import Image
from PIL import UnidentifiedImageError
import imagehash

def getproduct(src_pic, src_0):
    try:
        hash0 = imagehash.average_hash(Image.open(src_0)) 
        hash1 = imagehash.average_hash(Image.open(src_pic)) 
    except UnidentifiedImageError:
        return 0
    cutoff = 30
    #if hash1 - hash0 < cutoff:
    return 100 - (hash1 - hash0)
    #else:
    #    return 0

def getmaxinfolder(src_pic, directory):
    percents_of_folder = []
    for filename in os.listdir(directory):
        percents_of_folder.append(getproduct(src_pic, os.path.join(directory, filename)))
    print(percents_of_folder)
    return sum(percents_of_folder) // (len(percents_of_folder) - percents_of_folder.count(0) - percents_of_folder.count(-1))

def getmaxinallfolders(src_pic, directory="./pics_of_products"):
    maxpercents_of_folders = {}
    for foldername in os.listdir(directory):
        if os.path.isfile(foldername):
            continue
        folder_max = getmaxinfolder(src_pic, os.path.join(directory, foldername))
        maxpercents_of_folders[folder_max] = foldername
    print(maxpercents_of_folders)
    return maxpercents_of_folders[max(maxpercents_of_folders.keys())]     



print(getmaxinallfolders("./infreezerIMG/milk.jpg"))
print(getmaxinallfolders("./infreezerIMG/sir.jpg"))
print(getmaxinallfolders("./infreezerIMG/MORGEN.png"))