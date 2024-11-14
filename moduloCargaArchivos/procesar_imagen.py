import cv2

def procesar_imagen(ruta_imagen):
    img = cv2.imread(ruta_imagen)
    cv2.imwrite("imagen_procesada.jpg", img)