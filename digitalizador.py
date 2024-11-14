import cv2

img = cv2.imread(r"letrasSeparadas.jpg")
image = img.copy()  #  Creating a copy of the image to make changes
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #  Converting to greyscale
# Apply Otsu filtering
otsu1 = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilation = cv2.dilate(grey, kernel, iterations = 1)
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_NONE)
img_contours = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

img_list = []  #  initialize empty list
count = 0  #  keep a count for the words (optional)
for c in contours:
    x, y, w, h = cv2.boundingRect(c)  #  get coordinates of contouts
    if w>5 and h>25:  #  threshold for size of bounding box
        count += 1
        img_list.append(cv2.resize(otsu1[y:h+y, x:w+x], (128, 64))) # Resizing to fixed size
        rect = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) # Draw Bounding boxes

print(count, " words extracted!")

import matplotlib.pyplot as plt
ax = plt.subplots(2,3, figsize=(12,7))[1]
ax[0,0].imshow(image)
ax[0,0].set_title('Image')
ax[0,1].imshow(otsu1)
ax[0,1].set_title('Otsuing')
ax[0,2].imshow(img)
ax[0,2].set_title('Contours')
ax[1,0].imshow(img_contours)
ax[1,0].set_title('Re-Otsuing')
ax[1,1].imshow(dilation)
ax[1,1].set_title('Dilated')
ax[1,2].imshow(image)
ax[1,2].set_title('Result')
plt.show()