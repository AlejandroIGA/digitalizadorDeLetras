import cv2

def rescaleFrame(frame, scale=.55):
    """Redimensiona una imagen manteniendo la proporción."""
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_CUBIC)

def contar_palabras(ruta_imagen):
    """
    Procesa la imagen para contar el número de palabras encontradas en la misma.
    Devuelve el número de palabras en la imagen.
    """
    # Cargar la imagen
    img = cv2.imread(ruta_imagen)
    if img is None:
        raise ValueError("No se pudo cargar la imagen desde la ruta especificada.")    
    
    resized_img = rescaleFrame(img)  # Redimensionar la imagen para mejorar el procesamiento

    # Convertir a escala de grises
    gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

    # Aplicar un umbral adaptativo para mejorar la visibilidad del texto
    _, thresh = cv2.threshold(gray, 240, 245, cv2.THRESH_BINARY_INV)
    
    # Aplicar dilatación para unir partes de texto que puedan estar separadas
    dilated = cv2.dilate(thresh, None, iterations=2)

    # Encontrar contornos
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Contar las palabras y dibujar rectángulos
    num_palabras = 0
    for cnt in contours:
        # Filtrar contornos pequeños que no corresponden a palabras
        if cv2.contourArea(cnt) > 500:  
            # Obtener el rectángulo delimitador de la palabra
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Dibujar el rectángulo alrededor de la palabra detectada
            cv2.rectangle(resized_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            num_palabras += 1

    # Definir la ruta de salida antes de usarla
    ruta_salida = 'uploads/palabras_detectadas.jpg'

    # Guardar la imagen procesada con palabras detectadas resaltadas
    cv2.imwrite(ruta_salida, resized_img)

    return num_palabras
