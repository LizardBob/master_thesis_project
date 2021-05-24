from typing import Iterable, Optional

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, Manager, QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class LecturerManager(Manager):
    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .only(
                "id",
                "index_code",
                "email",
                "username",
                "name",
            )
        )


class User(AbstractUser):
    """Default user for Student System Service."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Lecturer(User):
    # TODO add  maybe faculty
    PATTERN_CODE = "lec"

    index_code = CharField(
        max_length=255, help_text="Lecturer university's id.", blank=True, null=False
    )
    objects = LecturerManager()

    class Meta:
        verbose_name = "Lecturer"
        verbose_name_plural = "Lecturers"

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None,
    ) -> None:
        lecturers_objects: QuerySet[Lecturer] = self.__class__.objects.order_by("id")
        last_id = (
            lecturers_objects.last().index_code.split(self.PATTERN_CODE)[-1]
            if lecturers_objects
            else 0
        )
        self.index_code = f"{self.PATTERN_CODE}{int(last_id) + 1}"
        super().save(force_insert, force_update, using, update_fields)
