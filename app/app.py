from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import zipfile
import io
from app import procesar_imagen, separarPalabras

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB

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
            filepath = os.path.join('/tmp', filename)  # Guardar temporalmente en memoria
            file.save(filepath)
            
            try:
                num_palabras = separarPalabras.contar_palabras(filepath)
                if num_palabras > 100:
                    os.remove(filepath)
                    return f'La imagen contiene {num_palabras} palabras y no será procesada. Cambie la imagen con texto menor a 100 palabras.'
                
                # Procesar la imagen y obtener datos de las imágenes procesadas
                images_data = procesar_imagen(filepath)
                
                # Crear un archivo ZIP en memoria
                zip_stream = io.BytesIO()
                with zipfile.ZipFile(zip_stream, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for name, data in images_data:
                        zipf.writestr(name, data)
                
                zip_stream.seek(0)
                os.remove(filepath)  # Eliminar el archivo temporal después de usarlo
                
                # Enviar el archivo ZIP al navegador
                return send_file(
                    zip_stream,
                    as_attachment=True,
                    download_name='processed_images.zip',
                    mimetype='application/zip'
                )
            except ValueError as e:
                return str(e)
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
