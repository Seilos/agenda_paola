"""
Django Management Command para crear los usuarios de los profesores.
Uso: python manage.py crear_profesores
"""
from django.core.management.base import BaseCommand
from agenda.models import Usuario


PROFESORES = [
    {
        "username": "nsanguinetti",
        "first_name": "Nelson",
        "last_name": "Sanguinetti",
        "password": "N2015T",
    },
    {
        "username": "fcudde",
        "first_name": "Florenzo",
        "last_name": "Cudde",
        "password": "Z357C",
    },
]


class Command(BaseCommand):
    help = "Crea los usuarios de los profesores con rol PROFESOR."

    def handle(self, *args, **kwargs):
        for datos in PROFESORES:
            if Usuario.objects.filter(username=datos["username"]).exists():
                self.stdout.write(f"  [--] Ya existe: {datos['username']}")
                continue

            user = Usuario.objects.create_user(
                username=datos["username"],
                first_name=datos["first_name"],
                last_name=datos["last_name"],
                password=datos["password"],
                rol="PROFESOR",
                is_active=True,
                recien_registrado=False,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"  [OK] Creado: {user.get_full_name()} "
                    f"(usuario: {user.username}, rol: {user.rol})"
                )
            )

        self.stdout.write("\nListo.")
