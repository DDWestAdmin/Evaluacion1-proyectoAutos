import os
import re
import unicodedata

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

# Create your views here.
def formulario_autos(request):
    if request.method == 'POST':
        imagen = request.FILES.get('imagen')
        if not imagen:
            return JsonResponse({'error': 'Debes seleccionar una imagen.'}, status=400)

        datos = {
            'marca': request.POST.get('marca', '').strip(),
            'modelo': request.POST.get('modelo', '').strip(),
            'anio': request.POST.get('anio', '').strip(),
            'descripcion': request.POST.get('descripcion', '').strip(),
        }

        limites = {'marca': 50, 'modelo': 100, 'anio': 4, 'descripcion': 250}
        if any(len(datos[campo]) > limite for campo, limite in limites.items()):
            return JsonResponse({'error': 'Uno de los campos supera su longitud máxima.'}, status=400)

        extension = os.path.splitext(imagen.name)[1].lower()
        extensiones_validas = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        if extension not in extensiones_validas:
            return JsonResponse({'error': 'La imagen debe ser JPG, PNG, GIF o WEBP.'}, status=400)

        carpeta_imagenes = settings.BASE_DIR.parent / 'Galeria' / 'static' / 'images'
        carpeta_imagenes.mkdir(parents=True, exist_ok=True)
        partes_nombre = []
        for campo in ('modelo', 'marca', 'anio'):
            texto = unicodedata.normalize('NFKD', datos[campo]).encode('ascii', 'ignore').decode('ascii')
            texto = re.sub(r'[^a-zA-Z0-9]+', '-', texto).strip('-').lower()
            partes_nombre.append(texto)

        nombre_imagen = f"{'-'.join(partes_nombre)}{extension}"
        ruta_imagen = carpeta_imagenes / nombre_imagen

        with ruta_imagen.open('wb+') as archivo_destino:
            for bloque in imagen.chunks():
                archivo_destino.write(bloque)

        datos['imagen'] = f'/static/images/{nombre_imagen}'
        return JsonResponse(datos, status=201)

    return render(request, 'formularioAutos.html')