import cv2
import numpy as np
import math

def dicePointDetector(kep, result, detectedPoints):
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
    points = 0
    if circles is not None:

        for i in circles[0, :]:
            center = (i[0], i[1])
            cv2.circle(img, center, 1, (255, 0, 0), 8)
            radius = i[2]
            cv2.circle(img, center, radius, (0, 255, 0), 8)
            points = points+1

    dices = 0
    circles2=circles.tolist()

    for z in range(0,5):
        for i in range(0, len(circles2[0])-1):
            for j in range(1, len(circles2[0])-2):
                '''and (circles2[0][i] != [0,0,0]) and (circles2[0][j] != [0,0,0])'''
                if  i != j and i <= len(circles2[0])-1 and j <= len(circles2[0])-1 :
                    if math.sqrt(float( ( (float(circles2[0][i][0])-float(circles2[0][j][0]))**2 + (float(circles2[0][i][1])-float(circles2[0][j][1]))**2 ))) <= 220:
                        x=(float(circles2[0][i][0])+float(circles2[0][j][0]))/2
                        y=(float(circles2[0][i][1])+float(circles2[0][j][1]))/2
                        circles2[0].append([x,y, 15])
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
                    
    print(circles2)
    print("--------------")
    dices=len(circles2[0])
    circles2np=np.array(circles2)
    #print(circles2[0][:])
    for i in circles2[0][:]:
            x=np.uint16(i[0])
            y=np.uint16(i[1])
            center = (x,y)
            radius = 120
            cv2.circle(img, center, radius, (222, 222, 222), 7)


    #Pontok értékének képre írása
    text = "Talalat: " + str(points)           
    cv2.putText(img,text,(10,30),0,1,(0,255,0), 4, cv2.LINE_AA)
    text = "Elvart: " + result           
    cv2.putText(img,text,(10,70),0,1,(0,255,0), 4, cv2.LINE_AA)
    text = "Kockak: " + str(dices)           
    cv2.putText(img,text,(10,110),0,1,(0,255,0), 4, cv2.LINE_AA)
    
    cv2.imshow("Detected circles", img)
    detectedPoints.append(points)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
detectedPoints = []
dicePointDetector("kepek/2.jpg", "18", detectedPoints)      # to test the function