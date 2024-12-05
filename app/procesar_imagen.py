import cv2
import os
import numpy as np

def procesar_imagen(ruta_imagen):
    # Cargar la imagen
    img = cv2.imread(ruta_imagen)
    resizedImg = rescaleFrame(img)  # Llamar a una función de redimensión
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 240, 250)

    # Encontrar contornos
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    i = 0
    image_paths = []
    # Procesar contornos según el área o la jerarquía
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        crop_img = resizedImg[y:y+h, x:x+w]

        scale_factor = 1.5
        resized_image = cv2.resize(crop_img, None, fx=scale_factor, fy=scale_factor, 
                                   interpolation=cv2.INTER_LINEAR)
            
        # Guardar cada contorno como imagen procesada
        image_path = f"uploads/contour_{i}.jpg"
        cv2.imwrite(image_path, resized_image)
        image_paths.append(image_path)
        i += 1
    
    # Guardar la imagen procesada principal
    main_image_path = "uploads/imagen_procesada.jpg"
    cv2.imwrite(main_image_path, resizedImg)
    image_paths.append(main_image_path)
    
    return image_paths

def rescaleFrame(frame, scale=.55):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_CUBIC)
