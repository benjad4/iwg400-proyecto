# Panoramas en Santiago

Aplicación web en Django para buscar panoramas en Santiago con un mapa y filtros. Proyecto de IWG400 (USM).

## Cómo ejecutarla

Necesitas Python 3.12 o superior y Git. Luego, en una terminal de PowerShell:

```
git clone https://github.com/benjad4/iwg400-proyecto.git
cd iwg400-proyecto
python -m venv env
env\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python -X utf8 manage.py loaddata datos_prueba
python manage.py runserver
```

Abrir http://127.0.0.1:8000/ en el navegador.

## Cómo probarla

Con los datos de prueba cargados:

- Comida + Tarjeta + Acepta JUNAEB: aparecen Mercado Central y Café en Barrio Italia.
- Cultura + Acepta JUNAEB: no aparece ningún resultado.