# Panoramas en Santiago

Proyecto del ramo **IWG400 Proyecto Inicial** (USM). Equipo 2 "End Game".

Página web hecha con Django para encontrar **panoramas gratis o baratos dentro de Santiago**, con un mapa interactivo y filtros. Se parte eligiendo una comuna y una categoría, para que el mapa no se llene de cientos de pines.

**Integrantes:** [Benjamin Contreras, Ramiro Salvat, Natacha Cespedes, Manuel Cordova, Tomas Catalan]

## Qué puedes hacer

- **Elegir tu panorama en 3 pasos:** comuna → categoría → mapa con los lugares.
- **Mapa interactivo** con marcadores agrupados y un emoji por categoría. Al tocar un pin aparece una tarjeta con el lugar y un botón para ver su ficha.
- **Filtros** en el mapa: comuna, categoría, costo (Gratis / De pago) y accesibilidad.
- **Ficha de cada lugar:** categoría, dirección, horario, botón para ver su ubicación en Google Maps y botón para más información (su sitio web, o una búsqueda en Google si no tiene).
- **🎲 Sorpréndeme:** eliges las comunas que te interesan y la página te sugiere un panorama al azar.
- **Cuentas de usuario:** registro, inicio y cierre de sesión. Con cuenta puedes guardar panoramas y dejar reseñas con valoración de 1 a 5.
- **Mis guardados:** tus panoramas guardados quedan ligados a tu cuenta.
- **Panel de administración** en `/admin/`.

Categorías: Aire libre, Cultura, Comida, Entretención, Deporte, Turismo, Compras y ferias, Mundo nocturno, Recreativo y Cerros y trekking.

## Tecnologías

- Python 3.14 y Django 6.1.2
- SQLite
- HTML, JavaScript y Tailwind CSS (por CDN)
- Leaflet, Leaflet.markercluster y mapas de OpenStreetMap
- Git y GitHub

## Cómo ejecutar el proyecto

Requisitos: Python y Git instalados. La página necesita internet (mapa y estilos se cargan desde la red).

1. Descargar el proyecto:

   ```powershell
   git clone https://github.com/benjad4/iwg400-proyecto.git
   cd iwg400-proyecto
   ```

2. Crear y activar el ambiente virtual, e instalar Django:

   ```powershell
   python -m venv env
   env\Scripts\Activate.ps1
   pip install django
   ```

3. Preparar la base de datos y cargar los lugares:

   ```powershell
   python manage.py migrate
   python -X utf8 manage.py loaddata datos_prueba
   ```

4. (Opcional) Crear una cuenta de administrador:

   ```powershell
   python manage.py createsuperuser
   ```

5. Levantar el servidor y abrir en Chrome <http://127.0.0.1:8000/>:

   ```powershell
   python manage.py runserver
   ```

La base de datos (`db.sqlite3`) no se sube a Git: cada persona tiene la suya, y los lugares viajan en el archivo `panoramas/fixtures/datos_prueba.json`. Las cuentas, los guardados y las reseñas que crees quedan solo en tu computador.

## Datos

Los lugares se importaron desde **OpenStreetMap** (Overpass API) para las 32 comunas de la provincia de Santiago más Puente Alto y San Bernardo, con este comando:

```powershell
python -X utf8 manage.py importar_osm --comunas "Providencia" "Ñuñoa" --categorias Comida Cultura --limite 40
```

Es seguro repetirlo: no duplica lugares (se identifican por nombre y comuna). Solo se aceptan lugares dentro de Santiago.

Mapas y datos: © Colaboradores de OpenStreetMap.

### Sobre los costos

OpenStreetMap no informa precios, así que cada lugar se muestra como **Gratis** o **De pago**, sin monto. En los de pago, la ficha lleva a su sitio web o a una búsqueda en Google para ver los precios. Los parques, miradores, cerros, ferias y galerías se marcaron como gratis, y los museos, restaurantes, cines, bares y centros deportivos, como de pago.

## Estructura del proyecto

```
config/                  Configuración de Django (settings.py, urls.py)
panoramas/
  models.py              Panorama, Resena y Guardado
  views.py               Vistas (comunas, categorías, mapa, ficha, cuentas, sorpresa)
  urls.py                Rutas
  forms.py               Formulario de reseñas
  admin.py               Panel de administración
  migrations/            Cambios de la base de datos
  fixtures/              datos_prueba.json (lugares)
  management/commands/   importar_osm.py (importador desde OpenStreetMap)
  templates/panoramas/   Plantillas HTML
```

## Rutas principales

| Ruta | Pantalla |
|---|---|
| `/` | Elegir comuna |
| `/categorias/?comuna=...` | Elegir categoría |
| `/mapa/?comuna=...&categoria=...` | Mapa con filtros |
| `/panorama/<id>/` | Ficha del lugar |
| `/sorpresa/` | Panorama al azar |
| `/guardados/` | Mis guardados (requiere cuenta) |
| `/entrar/`, `/registro/`, `/salir/` | Cuentas |
| `/admin/` | Administración |

## Casos de prueba

Los filtros se prueban en `/mapa/`, después de elegir comuna y categoría desde las pantallas iniciales.

| Caso | Pasos | Resultado