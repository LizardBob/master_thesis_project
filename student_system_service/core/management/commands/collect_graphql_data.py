from typing import Any, Optional

from django.core.management.base import BaseCommand

from ...data_collectors import CollectGraphQLApiData


class Command(BaseCommand):
    help = "Command just collecting data"

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write("\U0001F9E8 Starting command... \U0001F9E8")
        data = CollectGraphQLApiData()
        self.stdout.write(f"\n {data.GRAPHQL_API_REQUEST_DATA} \n")

        return self.stdout.write(self.style.SUCCESS("Finished ! " + "\U0001F389"))
