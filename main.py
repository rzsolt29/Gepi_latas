from dobokocka_azonosito import dicePointDetector
import os

def textToList(inputFile):
    images = []
    results = []
    with open(inputFile) as file:
        lines = file.readlines()
        for line in lines:
            wasImage=False
            imgStr = ""
            resStr = ""
            for i in line:
                if(not wasImage and i != ','):
                    imgStr+=i
                elif(i == ','):
                    wasImage=True
                elif(wasImage and i.isnumeric):
                    resStr+= i

            images.append(imgStr)
            inputpath = resStr.rstrip()
            results.append(inputpath)
        
    return images,results
path = "inputKepekEsErtekek.txt"
if os.path.exists(path) == True:
    images, results = textToList(path)
    print(images)
    print(results)
    numberOfResult = 0
    for image in images:
        dicePointDetector(image, results[numberOfResult])
        numberOfResult += 1
else:
    print("Hiba: A megadott fájl nem létezik")