import cv2 as cv
import numpy as np

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
    cv.imshow('Imagen redimensionada', frame)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_CUBIC)

# Cargar la imagen
img = cv.imread("../lightedImage.jpg")
img2 = cv.imread("../superficieIrregular.jpg")



# Redimensionar la imagen (opcional)
resizedImg = rescaleFrame(img)
resizedImg2 = rescaleFrame(img2)

# Convertir a escala de grises y detectar bordes
gray = cv.cvtColor(resizedImg, cv.COLOR_BGR2GRAY)
mediana = np.median(gray)

gray2 = cv.cvtColor(resizedImg2, cv.COLOR_BGR2GRAY)
mediana2 = np.median(gray2)

var1 = .45
var2 = 1.40

# Define umbrales usando la mediana
lower = int(max(0, var1 * mediana))
upper = int(min(255, var2 * mediana))

# Define umbrales usando la mediana
lower2 = int(max(0, var1 * mediana2))
upper2 = int(min(255, var2 * mediana2))

thresh = cv.adaptiveThreshold(
    gray2, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2
)
cv.imshow('Imagen thresh', thresh)
cv.waitKey(0)
cv.destroyAllWindows()

canny = cv.Canny(gray,lower, upper)
canny2 = cv.Canny(gray2,lower2, upper2)


cv.imshow('Imagen Canny1', canny)
cv.imshow('Imagen Canny2', canny2)
cv.waitKey(0)
cv.destroyAllWindows()

# Encontrar contornos externos
contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
contours2, hierarchy2 = cv.findContours(canny2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

print(len(contours))
print(len(contours2))


# Dibujar los contornos
img_contours = cv.drawContours(resizedImg, contours, -1, (0, 255, 0), 1)
# Mostrar la imagen con los contornos
cv.imshow('Imagen con contornos', img_contours)
img_contours2 = cv.drawContours(resizedImg2, contours, -1, (0, 255, 0), 1)
# Mostrar la imagen con los contornos
cv.imshow('Imagen con contornos2', img_contours2)
cv.waitKey(0)
cv.destroyAllWindows()
