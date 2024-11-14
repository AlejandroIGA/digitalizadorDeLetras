import cv2 
import numpy as np

def procesar_imagen(ruta_imagen):
    # Cargar la imagen
    img = cv2.imread(ruta_imagen)
    resizedImg = rescaleFrame(img)  # Llamar a una función de redimensión
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray,240, 250)

    # Encontrar contornos
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    i = 0
    # Procesar contornos según el área o la jerarquía
    for cnt in contours:
        # Obtener el rectángulo delimitador del contorno
        x, y, w, h = cv2.boundingRect(cnt)
        
        crop_img = resizedImg[y:y+h, x:x+w]

        scale_factor = 1.5  # Puedes ajustar este valor según tus necesidades
        resized_image = cv2.resize(crop_img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
            
        # Guardar cada contorno como imagen procesada
        cv2.imwrite(f"uploads/contour_{i}.jpg", resized_image)
        
        i = i+1
    
    # Guardar la imagen procesada principal
    cv2.imwrite("uploads/imagen_procesada.jpg", resizedImg)

def rescaleFrame(frame, scale=.55):
    """Redimensiona una imagen manteniendo la proporción.

    Args:
        frame: La imagen a redimensionar.
        scale: El factor de escala (valor entre 0 y 1).

    Returns:
        La imagen redimensionada.
    """
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    # Mostrar la imagen redimensionada (opcional)
    cv2.imshow('Imagen redimensionada', frame)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_CUBIC)
