from typing import Any, Optional

from django.core.management.base import BaseCommand

from student_system_service.core.chars_generator import CharGenerator


class Command(BaseCommand):
    help = "Soon ..."

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--before_opt",
            action="store_true",
            help="",
        )
        parser.add_argument(
            "--after_opt",
            action="store_true",
            help="",
        )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write("Start")
        if options.get("after_opt"):
            CharGenerator().start(is_before_opt=False)
        else:
            CharGenerator().start(is_before_opt=True)
        self.stdout.write("End !")
