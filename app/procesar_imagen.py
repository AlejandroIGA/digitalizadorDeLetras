import cv2
import numpy as np
import io

def procesar_imagen(ruta_imagen):
    # Cargar la imagen
    img = cv2.imread(ruta_imagen)
    if img is None:
        raise ValueError(f"No se pudo cargar la imagen en la ruta: {ruta_imagen}")
    
    resizedImg = rescaleFrame(img)  # Llamar a una función de redimensión
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 240, 250)

    # Encontrar contornos
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    i = 0
    images_data = []
    # Procesar contornos según el área o la jerarquía
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        crop_img = resizedImg[y:y+h, x:x+w]

        scale_factor = 1.5
        resized_image = cv2.resize(crop_img, None, fx=scale_factor, fy=scale_factor, 
                                   interpolation=cv2.INTER_LINEAR)
            
        # Guardar la imagen procesada en memoria
        _, buffer = cv2.imencode('.jpg', resized_image)
        images_data.append((f"contour_{i}.jpg", buffer.tobytes()))
        i += 1
    
    # Guardar la imagen procesada principal
    _, main_buffer = cv2.imencode('.jpg', resizedImg)
    images_data.append(("imagen_procesada.jpg", main_buffer.tobytes()))
    
    return images_data

def rescaleFrame(frame, scale=.55):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_CUBIC)
