import cv2 as cv
import numpy as np

def rescaleFrame(frame, scale=.60):
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

    cv.imshow('Letra', frame)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_CUBIC)

# Cargar la imagen
img = cv.imread("superficieIrregular.jpg")

# Redimensionar la imagen (opcional)
resizedImg = rescaleFrame(img)

# Convertir a escala de grises y detectar bordes
gray = cv.cvtColor(resizedImg, cv.COLOR_BGR2GRAY)
canny = cv.Canny(gray, 20, 100)

# Encontrar contornos con jerarquía
contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
print(len(contours))
# Filtrar contornos por jerarquía y área
MIN_AREA = 15  # Ajusta este valor según tus necesidades
for i in range(len(contours)):
    if hierarchy[0][i][3] == -1 and cv.contourArea(contours[i]) > MIN_AREA:  # Contorno externo y área mínima
        # Procesar el contorno
        x, y, w, h = cv.boundingRect(contours[i])

        # Recortar la imagen
        crop_img = resizedImg[y:y+h, x:x+w].copy()

        # Preprocesamiento
        gray = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)
        #blur = cv.medianBlur(gray, 3)  # Filtro mediano
        thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)  # Binarización adaptativa

        # Encontrar componentes conectados
        num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(thresh, connectivity=8)

        # Iterar sobre los componentes conectados
        for label in range(1, num_labels):
            # Obtener el rectángulo delimitador del componente
            x1, y1, w1, h1, area = stats[label]

            # Si el área es lo suficientemente grande, considerar como una letra
            if area > 10:  # Ajusta este valor según tus necesidades
                # Recortar la imagen del componente
                letter_img = crop_img[y1:y1+h1, x1:x1+w1]

                # Aumentar el tamaño al doble usando interpolación cúbica
                scale_factor = 1.25  # Puedes ajustar este valor según tus necesidades
                resized_image = cv.resize(letter_img, None, fx=scale_factor, fy=scale_factor, interpolation=cv.INTER_LINEAR)

                # Mostrar la imagen escalada
                cv.imshow(f'Letra escalada {label}', resized_image)
                cv.waitKey(0)
                cv.destroyAllWindows()

cv.destroyAllWindows()