from pathlib import Path

from django.conf import settings
from django.shortcuts import render

# Create your views here.
def galeria_autos(request):
    carpeta_imagenes = settings.BASE_DIR.parent / 'Galeria' / 'static' / 'images'
    extensiones_validas = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    imagenes = sorted(
        imagen.name
        for imagen in Path(carpeta_imagenes).glob('*')
        if imagen.is_file() and imagen.suffix.lower() in extensiones_validas
    )
    return render(request, 'galeriaAutos.html', {'imagenes': imagenes})