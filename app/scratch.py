import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread(r"imgEjm.jpg")
image = img.copy()  #  Creating a copy of the image to make changes
img_resized = cv2.resize(img, (1080, 800))

grey = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
# Aplicar umbralización de Otsu con inversión
otsu1 = cv2.threshold(grey, 50, 150, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
dilation = cv2.dilate(otsu1, kernel, iterations = 3)

#Contours cotiene las coordenadas de los contornos de cada elemento dentro de la imagen.
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

first_contour = contours[60]
print(first_contour)


# Dibujar los contornos
img_contours = cv2.drawContours(img_resized, contours, -1, (0, 255, 0), 3)

# Mostrar la imagen con los contornos
cv2.imshow('Imagen con contornos', img_contours)
cv2.waitKey(0)
cv2.destroyAllWindows()

img_list = []  #  initialize empty list
count = 0  #  keep a count for the words (optional)
for c in contours:
    x, y, w, h = cv2.boundingRect(c)  #  get coordinates of contouts
    if w>10 and h>10:  #  threshold for size of bounding box
        count += 1
    img_list.append(cv2.resize(otsu1[y:h+y, x:w+x], (128, 64))) # Resizing to fixed size
    rect = cv2.rectangle(img_resized, (x, y), (x + w, y + h), (0, 255, 0), 2) # Draw Bounding boxes

print(count, " words extracted!")

# Mostrar la imagen binaria
cv2.imshow('Imagen binaria', img_resized)
cv2.waitKey(0)
cv2.destroyAllWindows()


