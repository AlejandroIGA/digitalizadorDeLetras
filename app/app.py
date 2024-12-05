from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import procesar_imagen
import separarPalabras  

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB

# Crear la carpeta de subida si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    # Verificar si el archivo tiene una extensión permitida.
    allowed_extensions = {'jpg', 'jpeg'}
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions:
        return True
    return False

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Sin parte del archivo'
        file = request.files['file']
        if file.filename == '':
            return 'Archivo no seleccionado'
        if not allowed_file(file.filename):
            return 'Formato no permitido. Solo se permiten archivos JPG y JPEG.'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Verificar el número de palabras en la imagen
                num_palabras = separarPalabras.contar_palabras(filepath)
                if num_palabras > 100:
                    os.remove(filepath)  # Eliminar la imagen si excede el límite
                    return f'La imagen contiene {num_palabras} palabras y no será procesada, cambie la imagen con texto menor a 100 palabras.'
                
                # Si tiene menos de 100 palabras, procesar la imagen
                procesar_imagen.procesar_imagen(filepath)
                return f'¡Archivo subido exitosamente! La imagen contiene {num_palabras} palabras.'
            except ValueError as e:
                return str(e)  # Devuelve el mensaje de error si no se pudo procesar la imagen
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)
