import cv2 as cv
import numpy as np

def rescaleFrame(frame, scale=0.50):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_CUBIC )

#create a blank image
#blank = np.zeros((500,500,3), dtype="uint8")
#cv.imshow("Blank", blank)

#1. Paint the image a certain color
#blank[:] = 0,255,0 #reference all the pixels and setting the cnew color
#cv.imshow("Green",blank )

#read an image
img = cv.imread("pantera.jpeg")
resizedImg = rescaleFrame(img);

#display image as new window
#cv.imshow("pantera", resizedImg)

#converting to grayscale
gray = cv.cvtColor(resizedImg, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

#Blur
cv.imshow('Blur', cv.blur)

#delay for a key to be press
cv.waitKey(0)