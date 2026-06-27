"""
Script para cargar la lista de ambulatorios extraídos de las imágenes.
Ejecutar con:  python manage.py shell < cargar_ambulatorios.py
"""
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenda_project.settings')
django.setup()

from agenda.models import Ambulatorio

# ── Lista completa extraída de las imágenes ────────────────────────────────
# Municipio Maracaibo (1–49)
ambulatorios = [
    # Municipio Maracaibo
    "Amparo",
    "Cañada Honda",
    "CDI 18 de Octubre",
    "CDI Amparo",
    "CDI Cerros de Marín",
    "CDI Corito",
    "CDI La Chamarreta",
    "CDI La Macandona",
    "CDI La Pastora",
    "CDI La Paz",
    "CDI La Rinconada",
    "CDI La Victoria",
    "CDI Los Mangos",
    "CDI Lago Azul",
    "CDI San Jacinto",
    "CDI Santa Rosalía",
    "CDI Valle Frío",
    "CDI Zapara",
    "Cerros de Marín",
    "Corito I",
    "Corito II",
    "Cuatricentenario",
    "Cuijicito",
    "Francisco Gómez Padrón",
    "Fundación del Niño",
    "IVSS Centro Norte",
    "IVSS Sabaneta",
    "IVSS Veritas",
    "La Misión",
    "La Rinconada",
    "La Rotaria",
    "La Victoria",
    "Los Claveles",
    "Los Olivos",
    "Monte Claro",
    "Panamericano",
    "Pedregal",
    "Platejas Kleber Ramírez",
    "Primero de Mayo",
    "Puerto Rico",
    "Sabaneta",
    "SAMAS Mcbo Oeste",
    "SAMAS Maracaibo Norte",
    "SAMAS Terminal",
    "SAMAS Vereda del Lago",
    "San Jacinto",
    "San Miguel",
    "Simón Bolívar",
    "Ziruma",
    # Municipio San Francisco
    "CDI El Manzanillo",
    "CDI Los Cortijos",
    "El Silencio",
    "IMSASUR",
    "San Felipe",
    "San Francisco",
    "Sierra Maestra",
    "Villa Bolivariana",
    # Municipio Cabimas
    "Carretera H",
    "El Lucero",
    "Federación",
    "Nueva Cabimas",
    # Municipio Lagunillas
    "I.V.S.S. Ciudad Ojeda",
    "Las Morochas",
    "Libertad",
    "Paraíso",
    "Unión",
    # Municipio Mara
    "Cuatro Bocas",
    "Las Cabimas",
    "Santa Cruz",
    # Municipio Jesús E. Lossada
    "I.V.S.S. La Conc.",
    "La Paz",
    # Municipio La Cañada de Urdaneta
    "CDI Concepción",
    "El Carmelo",
    # Municipio Santa Rita
    "I.V.S.S. Sta. Rita",
    "Punta Iguana",
]

# ── Inserción con get_or_create (evita duplicados) ─────────────────────────
creados = 0
existentes = 0

for nombre in ambulatorios:
    obj, created = Ambulatorio.objects.get_or_create(nombre=nombre)
    if created:
        creados += 1
        print(f"  ✅ Creado: {nombre}")
    else:
        existentes += 1
        print(f"  ⏭  Ya existe: {nombre}")

print(f"\n{'─'*50}")
print(f"  Total creados:    {creados}")
print(f"  Ya existían:      {existentes}")
print(f"  Total en tabla:   {Ambulatorio.objects.count()}")
print(f"{'─'*50}")
