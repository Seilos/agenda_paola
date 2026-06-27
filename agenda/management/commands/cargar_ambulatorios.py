"""
Script de Django Management Command para cargar ambulatorios.
Uso: python manage.py cargar_ambulatorios
"""
from django.core.management.base import BaseCommand
from agenda.models import Ambulatorio


AMBULATORIOS = [
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


class Command(BaseCommand):
    help = "Carga la lista inicial de ambulatorios en la base de datos."

    def handle(self, *args, **kwargs):
        creados = 0
        existentes = 0

        for nombre in AMBULATORIOS:
            _, created = Ambulatorio.objects.get_or_create(nombre=nombre)
            if created:
                creados += 1
                self.stdout.write(self.style.SUCCESS(f"  [OK] Creado: {nombre}"))
            else:
                existentes += 1
                self.stdout.write(f"  [--] Ya existe: {nombre}")

        self.stdout.write("\n" + "-" * 50)
        self.stdout.write(self.style.SUCCESS(f"  Total creados:  {creados}"))
        self.stdout.write(f"  Ya existian:    {existentes}")
        self.stdout.write(f"  Total en tabla: {Ambulatorio.objects.count()}")
        self.stdout.write("-" * 50)
