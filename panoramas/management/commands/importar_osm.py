import json
import time
import urllib.error
import urllib.parse
import urllib.request

from django.core.management.base import BaseCommand

from panoramas.models import Panorama

URL = "https://overpass-api.de/api/interpreter"

# Solo se aceptan lugares dentro de Santiago (descarta resultados de otros países)
LAT_MIN, LAT_MAX = -33.65, -33.30
LON_MIN, LON_MAX = -70.85, -70.45

CATEGORIAS = {
    "Aire libre": '["leisure"="park"]',
    "Cultura": '[~"^(tourism|amenity)$"~"^(museum|gallery|library)$"]',
    "Comida": '["amenity"~"^(restaurant|cafe|fast_food)$"]',
    "Entretención": '["amenity"~"^(cinema|theatre|arts_centre)$"]',
    "Deporte": '["leisure"~"^(sports_centre|swimming_pool|fitness_centre|skatepark)$"]',
    "Turismo": '["tourism"~"^(viewpoint|attraction|zoo)$"]',
    "Compras y ferias": '["amenity"="marketplace"]',
    "Mundo nocturno": '["amenity"~"^(nightclub|pub|bar|biergarten)$"]',
    "Recreativo": '[~"^(leisure|amenity|sport)$"~"^(bowling_alley|miniature_golf|escape_game|amusement_arcade|billiards)$"]',
    "Cerros y trekking": '["natural"="peak"]',
}


def consultar(comuna, filtro, limite):
    consulta = (
        "[out:json][timeout:60];"
        f'area["boundary"="administrative"]["admin_level"="8"]["name"="{comuna}"]->.a;'
        f'nwr(area.a)["name"]{filtro};'
        f"out center tags {limite};"
    )
    datos = urllib.parse.urlencode({"data": consulta}).encode()
    pedido = urllib.request.Request(
        URL, data=datos,
        headers={"User-Agent": "panoramas-santiago-proyecto-usm/1.0"},
    )
    for intento in range(3):
        try:
            with urllib.request.urlopen(pedido, timeout=90) as respuesta:
                return json.loads(respuesta.read().decode("utf-8"))["elements"]
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as error:
            print(f"  Intento {intento + 1} falló: {error}")
            time.sleep(10)
    return []


class Command(BaseCommand):
    help = "Importa panoramas desde OpenStreetMap (Overpass API)"

    def add_arguments(self, parser):
        parser.add_argument("--comunas", nargs="+",
                            default=["Santiago", "Providencia", "Ñuñoa"])
        parser.add_argument("--limite", type=int, default=10)
        parser.add_argument("--categorias", nargs="+", default=list(CATEGORIAS.keys()))

    def handle(self, *args, **opciones):
        creados = 0
        for comuna in opciones["comunas"]:
            for categoria in opciones["categorias"]:
                filtro = CATEGORIAS[categoria]
                self.stdout.write(f"{comuna} - {categoria}...")
                for elemento in consultar(comuna, filtro, opciones["limite"]):
                    if self.guardar(elemento, comuna, categoria):
                        creados += 1
                time.sleep(2)  # pausa para no saturar la API
        self.stdout.write(self.style.SUCCESS(f"Listo: {creados} panoramas nuevos."))

    def guardar(self, elemento, comuna, categoria):
        tags = elemento.get("tags", {})
        nombre = tags.get("name", "").strip()[:150]
        punto = elemento.get("center") or elemento
        lat, lon = punto.get("lat"), punto.get("lon")
        if not nombre or lat is None or lon is None:
            return False
        if not (LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX):
            return False

        calle = tags.get("addr:street", "")
        numero = tags.get("addr:housenumber", "")
        direccion = f"{calle} {numero}".strip() or "Dirección por completar"

        gratis = (
            categoria in ("Aire libre", "Turismo", "Cerros y trekking")
            or tags.get("fee") == "no"
            or tags.get("amenity") == "library"
        )
        cocina = ""
        if categoria == "Comida":
            cocina = tags.get("cuisine", "").split(";")[0].replace("_", " ").capitalize()

        sitio = (tags.get("website") or tags.get("contact:website") or "").strip()
        if sitio and not sitio.startswith("http"):
            sitio = "https://" + sitio

        panorama, creado = Panorama.objects.get_or_create(
            nombre=nombre,
            comuna=comuna,
            defaults={
                "categoria": categoria,
                "direccion": direccion[:200],
                "latitud": lat,
                "longitud": lon,
                "costo": 0 if gratis else 5000,
                "descripcion": "" if gratis else "[Por completar] Costo, horario y JUNAEB sin verificar.",
                "horario": tags.get("opening_hours", "")[:100],
                "sitio_web": sitio[:300],
                "tipo_cocina": cocina[:60],
                "accesible": tags.get("wheelchair") == "yes",
            },
        )
        if not creado and sitio and not panorama.sitio_web:
            panorama.sitio_web = sitio[:300]
            panorama.save(update_fields=["sitio_web"])
        return creado