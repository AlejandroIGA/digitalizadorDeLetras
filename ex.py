import cv2 as cv
import numpy as np

def rescaleFrame(frame, scale=.50):
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
    cv.imshow('Imagen redimensionada', frame)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_CUBIC)

# Cargar la imagen
img = cv.imread("imgEjm.jpg")

# Redimensionar la imagen (opcional)
resizedImg = rescaleFrame(img)

# Convertir a escala de grises y detectar bordes
gray = cv.cvtColor(resizedImg, cv.COLOR_BGR2GRAY)
canny = cv.Canny(gray, 20, 100)

# Encontrar contornos externos
contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Iterar sobre los contornos externos
for cnt in contours:
    # Obtener el rectángulo delimitador del contorno
    x, y, w, h = cv.boundingRect(cnt)

    # Recortar la imagen
    crop_img = resizedImg[y:y+h, x:x+w].copy()

    # Preprocesamiento (opcional)
    # ... (aquí puedes agregar tus pasos de preprocesamiento si los necesitas)
    gray = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 3)  # Filtro mediano
    thresh = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)  # Binarización adaptativa

    scale_factor = 1.5  # Puedes ajustar este valor según tus necesidades
    resized_image = cv.resize(crop_img , None, fx=scale_factor, fy=scale_factor, interpolation=cv.INTER_LINEAR)

    # Mostrar la imagen recortada (opcional)
    cv.imshow('Imagen recortada', resized_image)
    cv.waitKey(0)
    cv.destroyAllWindows()

cv.destroyAllWindows()