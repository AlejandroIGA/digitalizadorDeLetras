import cv2

# Función de redimensionado
def rescaleFrame(frame, scale=.55):
    """Redimensiona una imagen manteniendo la proporción."""
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_CUBIC)

# Función para separar palabras
def separar_palabras(ruta_imagen, max_palabras=100):
    """
    Separa las palabras en una imagen y verifica si supera el límite.
    """
    # Cargar la imagen
    img = cv2.imread(ruta_imagen)
    if img is None:
        return "Error: No se pudo cargar la imagen desde la ruta especificada."

    resized_img = rescaleFrame(img)  

    # Convertir a escala de grises
    gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

    # Aplicar un umbral adaptativo para mejorar la visibilidad del texto
    _, thresh = cv2.threshold(gray, 250, 245, cv2.THRESH_BINARY_INV)

    # Aplicar dilatación para unir partes de texto que puedan estar separadas
    dilated = cv2.dilate(thresh, None, iterations=2)

    # Encontrar contornos
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Contar palabras y verificar límite
    num_palabras = 0
    for cnt in contours:
        # Filtrar contornos pequeños que no corresponden a palabras
        if cv2.contourArea(cnt) > 500:  # Ajusta este valor según tus imágenes
            num_palabras += 1

    # Verificar si se supera el límite de palabras
    if num_palabras > max_palabras:
        return f"¡La imagen supera el límite! Contiene {num_palabras} palabras."

    # Mostrar la cantidad de palabras encontradas
    return f"La imagen contiene {num_palabras} palabras."

ruta_imagen = './scaner.jpg'  
resultado = separar_palabras(ruta_imagen)
print(resultado)
