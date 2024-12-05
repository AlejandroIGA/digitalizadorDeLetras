from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import zipfile
import procesar_imagen
import separarPalabras  

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    allowed_extensions = {'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

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
                num_palabras = separarPalabras.contar_palabras(filepath)
                if num_palabras > 100:
                    os.remove(filepath)
                    return f'La imagen contiene {num_palabras} palabras y no será procesada. Cambie la imagen con texto menor a 100 palabras.'
                
                # Procesar la imagen y obtener rutas de las imágenes procesadas
                image_paths = procesar_imagen.procesar_imagen(filepath)
                
                # Crear un archivo ZIP
                zip_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_images.zip')
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for img_path in image_paths:
                        zipf.write(img_path, os.path.basename(img_path))
                
                # Enviar el archivo ZIP al navegador
                return send_file(zip_path, as_attachment=True)
            except ValueError as e:
                return str(e)
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
