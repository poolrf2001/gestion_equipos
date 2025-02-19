import pyheif
from PIL import Image
import os
from django.core.files.base import ContentFile

def convert_heic_to_jpg(file):
    """
    Convierte un archivo HEIC a JPG y retorna un archivo JPG compatible con Django.
    """
    heif_file = pyheif.read(file.read())
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )

    # Guardar la imagen convertida en memoria como JPG
    converted_image = ContentFile(b"")
    image.save(converted_image, format="JPEG")
    converted_image.seek(0)  # Reinicia el puntero del archivo

    return converted_image
