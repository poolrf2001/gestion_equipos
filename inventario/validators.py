import magic
from django.core.exceptions import ValidationError

def validate_image_file(file):
    # Lista de tipos MIME válidos
    valid_mime_types = ['image/jpeg', 'image/png', 'image/heic', 'image/heif']
    mime = magic.Magic(mime=True)
    
    # Leer los primeros bytes del archivo para determinar su tipo
    file_mime = mime.from_buffer(file.read(1024))

    if file_mime not in valid_mime_types:
        raise ValidationError('El archivo adjunto no es una imagen válida.')

    # Reiniciar el puntero del archivo para evitar problemas posteriores
    file.seek(0)
