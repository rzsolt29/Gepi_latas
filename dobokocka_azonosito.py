import cv2
import numpy as np
import math

def dicePointDetector(kep, pointsToGet, dicesToGet, detectedPoints, detectedDices):
    #kép importálás és átméretezés
    img = cv2.imread(kep)

    x = 650 / img.shape[0]
    y = x
    img = cv2.resize(img, None, None, x, y, cv2.INTER_CUBIC)

    #Szürke árnyalatossá alakítás + medián szűrő
    GrayImg = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    imgMedian = cv2.medianBlur(GrayImg, 11)

    #morphológiai zárás
    k = np.ones((3, 3))
    imgMedian = cv2.morphologyEx(imgMedian, cv2.MORPH_CLOSE, k)

    #pontok detektálása
    rows = imgMedian.shape[0]
    circles = cv2.HoughCircles(imgMedian, cv2.HOUGH_GRADIENT, 1, rows / 100,
                                param1=240, param2=23,
                                minRadius=1, maxRadius=50)
    circles = np.uint16(np.around(circles))
    
    circles2=circles.tolist()

    #átlag
    '''radiusSum=0
    for i in circles2[0]:
        radiusSum += i[2]
    radiusAvg = radiusSum / len(circles2[0])'''
    
    #medián
    orderedCircles=sorted(circles2[0], key=lambda x: x[2])
    radiusMedian=0
    if(len(orderedCircles)>0):
        radiusMedian=orderedCircles[int(round(len(orderedCircles)/2))][2]

    i=0
    while i <= len(circles2[0])-1:
        if (circles2[0][i][2] > (radiusMedian+10) or circles2[0][i][2] < (radiusMedian-5)):
            toDelete = circles2[0][i]
            circles2[0].remove(toDelete)
        i += 1
    
    circles= np.array(circles2)
    circles2=circles.tolist()

    #pontok megszámlálása és képre írása
    points = 0
    if circles is not None:

        for i in circles[0, :]:
            center = (i[0], i[1])
            cv2.circle(img, center, 1, (255, 0, 0), 8)
            radius = i[2]
            cv2.circle(img, center, radius, (0, 255, 0), 8)
            points = points+1

    #kockák megszámlálása
    dices = 0

    for z in range(0,6):
        for i in range(0, len(circles2[0])-1):
            for j in range(0, len(circles2[0])):
                '''and (circles2[0][i] != [0,0,0]) and (circles2[0][j] != [0,0,0])'''
                if  i != j and i <= len(circles2[0])-1 and j <= len(circles2[0])-1 :
                    if math.sqrt(float( ( (float(circles2[0][i][0])-float(circles2[0][j][0]))**2 + (float(circles2[0][i][1])-float(circles2[0][j][1]))**2 ))) <= 85:
                        x=(float(circles2[0][i][0])+float(circles2[0][j][0]))/2
                        y=(float(circles2[0][i][1])+float(circles2[0][j][1]))/2
                        
                        if i<j:
                            toDelete=circles2[0][i]
                            circles2[0].remove(toDelete)
                            toDelete=circles2[0][j-1]
                            circles2[0].remove(toDelete)
                        else:
                            toDelete=circles2[0][i]
                            circles2[0].remove(toDelete)
                            toDelete=circles2[0][j]
                            circles2[0].remove(toDelete)
                        circles2[0].append([x,y, 15])
 

    dices=len(circles2[0])
    circles2np=np.array(circles2)
    
    
    for i in circles2[0][:]:
            x=np.uint16(i[0])
            y=np.uint16(i[1])
            center = (x,y)
            radius = 100
            cv2.circle(img, center, radius, (222, 222, 222), 7)


    #Pontok értékének képre írása
    text = "Talalat: " + str(points)           
    cv2.putText(img,text,(10,30),0,1,(0,255,0), 4, cv2.LINE_AA)

    if(int(points) == int(pointsToGet)):
        text = "Elvart: " + pointsToGet           
        cv2.putText(img,text,(10,70),0,1,(0,255,0), 4, cv2.LINE_AA)
    else:
        text = "Elvart: " + pointsToGet
        cv2.putText(img,text,(10,70),0,1,(0,0,255), 4, cv2.LINE_AA)

    text = "Kockak: " + str(dices)           
    cv2.putText(img,text,(10,110),0,1,(0,255,0), 4, cv2.LINE_AA)
    
    if(int(dicesToGet) == int(dices)):
        text = "Elvart: " + str(dicesToGet)           
        cv2.putText(img,text,(10,140),0,1,(0,255,0), 4, cv2.LINE_AA)
    else:
        text = "Elvart: " + str(dicesToGet)           
        cv2.putText(img,text,(10,140),0,1,(0,0,255), 4, cv2.LINE_AA)

    #cv2.imshow("Detected circles", img)
    detectedPoints.append(points)
    detectedDices.append(dices)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# to test the function

#detectedPoints = []
#detectedDices = []
#dicePointDetector("kepek/61.jpg", "13","3", detectedPoints, detectedDices)