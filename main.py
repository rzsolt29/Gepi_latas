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

detectedPoints = []

#fájl beolvasás és feldolgozás
path = "inputKepekEsErtekek.txt"
if os.path.exists(path) == True:
    images, results = textToList(path)
    #print(images)
    #print(results)
    numberOfResult = 0
    for image in images:
        dicePointDetector(image, results[numberOfResult], detectedPoints)   #input kép, elvárt eredmény, output: list
        numberOfResult += 1
else:
    print("Hiba: A megadott fájl nem létezik")

#A megtalált és elvárt pontok közötti különbségnek a megszámlálása
if len(detectedPoints) == len(results):
    errors=0
    for i in range(len(detectedPoints)):
        if(detectedPoints[i] != int(results[i])):
            errors+=1
    print("Elteresek szam a megtalalt pontok és az elvart eredmeny kozott: "+str(errors))
