from dobokocka_azonosito import dicePointDetector
import os

def textToList(inputFile):
    images = []
    results = []
    dices=[]
    with open(inputFile) as file:
        lines = file.readlines()
        for line in lines:
            commaCounter=0
            imgStr = ""
            resStr = ""
            diceStr = ""
            for i in line:
                if(commaCounter == 0 and i != ','):
                    imgStr+=i
                elif(i == ','):
                    commaCounter += 1
                elif(commaCounter == 1 and i.isnumeric):
                    resStr += i
                elif(commaCounter == 2 and i.isnumeric):
                    diceStr += i

            images.append(imgStr)
            results.append(resStr)
            diceStr = diceStr.rstrip()
            dices.append(diceStr)
        
    return images,results, dices

detectedPoints = []
detectedDices = []

#fájl beolvasás és feldolgozás
path = "inputKepekEsErtekek.txt"
if os.path.exists(path) == True:
    images, pointsToGet, dicesToGet = textToList(path)
    #print(images)
    #print(results)
    #print(dices)
    numberOfResult = 0
    for image in images:
        dicePointDetector(image, pointsToGet[numberOfResult], dicesToGet[numberOfResult], detectedPoints, detectedDices)   #input kép, elvárt eredmény, output: list
        numberOfResult += 1
else:
    print("Hiba: A megadott fájl nem létezik")

#A megtalált és elvárt pontok közötti különbség megszámlálása
if len(detectedPoints) == len(pointsToGet):
    errors=0
    for i in range(len(detectedPoints)):
        if(detectedPoints[i] != int(pointsToGet[i])):
            errors+=1
    print("Elteresek szama megtalalt pontok es az elvart eredmeny kozott (ennyi kepnel talalhato hiba): "+str(errors))
else:
    print("hiba")

if len(detectedPoints) == len(pointsToGet):
    errors=0
    for i in range(len(detectedPoints)):
        if(detectedPoints[i] != int(pointsToGet[i])):
            errors=errors+abs(detectedPoints[i]-int(pointsToGet[i]))
    print("Elteresek szama megtalalt pontok es az elvart eredmeny kozott (osszes hibaszám): "+str(errors))
else:
    print("hiba")

#A megtalált és elvárt kockák közötti különbség megszámlálása
if len(detectedDices) == len(dicesToGet):
    errors=0
    for i in range(len(detectedDices)):
        if(detectedDices[i] != int(dicesToGet[i])):
            errors+=1
    print("Elteresek szama elvart es megtalalat kockak kozott (ennyi kepnel talalhato hiba): "+str(errors))
else:
    print("hiba")

if len(detectedDices) == len(dicesToGet):
    errors=0
    for i in range(len(detectedDices)):
        if(detectedDices[i] != int(dicesToGet[i])):
            errors=errors+abs(detectedDices[i]-int(dicesToGet[i]))
    print("Elteresek szama elvart es megtalalat kockak kozott (osszes hibaszám): "+str(errors))
else:
    print("hiba")