import cv2 as cv
import numpy as np

#kép importálás és átméretezés

img = cv.imread("src/01.jpg")
#print('Original Picture Dimensions : ',img.shape)
 
scale_percent = 20
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resized=cv.resize(img,dim)
#print('Resized Picture Dimensions : ',resized.shape)
#cv.imshow("Resized image", resized)


#kép szürkeárnyalatossá alakítása

gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)
cv.imshow("Grey image", gray)


#simítás

#gauss3=cv.GaussianBlur(gray,(3,3),0)
#cv.imshow("Blured image 3", gauss3)

#gauss5=cv.GaussianBlur(gray,(5,5),0)
#cv.imshow("Blured image 5", gauss5)

#bilateral = cv.bilateralFilter(gray,9,75,75)           #a kockán lévő pöttyök nem elég homogének
#cv.imshow("Bilateral filterde image",bilateral)

median = cv.medianBlur(gray,5)                          #ez a simítás tűnik a legjobbank
#cv.imshow("Median blured image",median)

# Canny éldetektor

edges = cv.Canny(median,100,200)                        #Gauss-nál kevésbé zajos
cv.imshow("Canny Edge Detection median",edges)
#edges2 = cv.Canny(gauss5,100,200)
#cv.imshow("Canny Edge Detection gauss5",edges2)





cv.waitKey(0)
cv.destroyAllWindows()