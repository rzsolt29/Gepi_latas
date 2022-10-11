import cv2
import numpy as np
import matplotlib.pyplot as plt

#kép importálás és átméretezés

img = cv2.imread("src/kozeli/13.jpg",0)

x = 650 / img.shape[0]
y = x
img = cv2.resize(img, None, None, x, y, cv2.INTER_CUBIC)


#kép szürkeárnyalatossá alakítása

#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)       #HoughCircles miatt kimarad, mert a HoughCircles végtelen ciklusba esne
#cv2.imshow("Grey image", gray)


#simítás

#gauss3=cv2.GaussianBlur(gray,(3,3),0)
#cv2.imshow("Blured image 3", gauss3)

gauss5=cv2.GaussianBlur(img,(5,5),0)
#cv2.imshow("Blured image 5", gauss5)

bilateral = cv2.bilateralFilter(img,9,75,75)           
#cv2.imshow("Bilateral filterde image",bilateral)

median = cv2.medianBlur(img,5)                          #ez a simítás tűnik a legjobbank, de a HoughCircles mégias a bilateralt jobban kezeli
#cv2.imshow("Median blured image",median)


#morphologyEx 
k = np.ones((3, 3))
morph = cv2.morphologyEx(median, cv2.MORPH_CLOSE, k)
#cv2.imshow("morph image", morph)


# Canny éldetektor

edges = cv2.Canny(morph,100,200)
#cv2.imshow("Canny Edge Detection median",edges)
edges2 = cv2.Canny(gauss5,100,200)
#cv2.imshow("Canny Edge Detection gauss5",edges2)
edges3 = cv2.Canny(bilateral,90,190)
#cv2.imshow("Canny Edge Detection bilateral",edges2)


cimg = cv2.cvtColor(edges3,cv2.COLOR_GRAY2BGR)

rows = edges3.shape[0]
circles = cv2.HoughCircles(edges3, cv2.HOUGH_GRADIENT, 1, rows / 100,
                            param1=240, param2=23,
                            minRadius=1, maxRadius=90)                      #max=90 eddig a legjobb

circles = np.uint16(np.around(circles))
points=0
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    points+=1


cv2.imshow('detected circles',cimg)
print("Dobott pontok:")
print(points)


cv2.waitKey(0)
cv2.destroyAllWindows()