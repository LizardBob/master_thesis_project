from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from student_system_service.courses.api.views import FacultyViewSet
from student_system_service.students.api.views import StudentViewSet
from student_system_service.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("students", StudentViewSet)
router.register("faculty", FacultyViewSet)


app_name = "api"
urlpatterns = router.urls
