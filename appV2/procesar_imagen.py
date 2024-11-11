import cv2
import numpy as np

def procesar_imagen(ruta_imagen):
    # Cargar la imagen
    img = cv2.imread(ruta_imagen)
    resizedImg = rescaleFrame(img, 0.6)  # Llamar a una función de redimensión
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 20, 100)  # Detectar bordes

    # Encontrar contornos
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Procesar contornos según el área o la jerarquía
    for i in range(len(contours)):
        if hierarchy[0][i][3] == -1 and cv2.contourArea(contours[i]) > 15:
            x, y, w, h = cv2.boundingRect(contours[i])
            crop_img = resizedImg[y:y+h, x:x+w]
            
            # Guardar cada contorno como imagen procesada
            cv2.imwrite(f"uploads/contour_{i}.jpg", crop_img)
    
    # Guardar la imagen procesada principal
    cv2.imwrite("uploads/imagen_procesada.jpg", resizedImg)

def rescaleFrame(frame, scale=0.6):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)
