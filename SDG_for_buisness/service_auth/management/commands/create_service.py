from django.core.management.base import BaseCommand
from service_auth.models import ServiceClient


class Command(BaseCommand):
    help = "Create service client with API key"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str)
        parser.add_argument(
            "--scopes",
            nargs="+",
            type=str,
            default=[],
            help="List of scopes",
        )
        parser.add_argument(
            "--inactive",
            action="store_true",
            help="Mark service as inactive (default is active)",
        )

    def handle(self, *args, **options):
        name = options["name"]
        scopes = options["scopes"]

        is_active = not options["inactive"]  # 👈 по умолчанию True

        service, created = ServiceClient.objects.get_or_create(
            name=name,
            defaults={
                "scopes": scopes,
                "is_active": is_active,
            },
        )

        if not created:
            self.stdout.write(
                self.style.WARNING(f"Service '{name}' already exists")
            )
            return

        self.stdout.write(self.style.SUCCESS("Service created successfully"))
        self.stdout.write(f"Name: {service.name}")
        self.stdout.write(f"API KEY: {service.api_key}")
        self.stdout.write(f"Scopes: {service.scopes}")
        self.stdout.write(f"Active: {service.is_active}")