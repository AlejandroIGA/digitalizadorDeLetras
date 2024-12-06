from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import zipfile
import io
from app.procesar_imagen import procesar_imagen
from app.separarPalabras import contar_palabras

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
                num_palabras = contar_palabras(filepath)
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
                
                # Mensaje de éxito
                mensaje = f'¡Archivo subido exitosamente! La imagen contiene {num_palabras} palabras.'
                
                # Enviar el archivo ZIP al navegador
                response = send_file(
                zip_stream,
                as_attachment=True,
                download_name='processed_images.zip',
                mimetype='application/zip'
                )
                response.headers['X-Success-Message'] = mensaje  # Añadir el mensaje como encabezado
                return response

            except ValueError as e:
                return str(e)
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
