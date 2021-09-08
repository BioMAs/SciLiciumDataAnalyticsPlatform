from django.conf import settings
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from sdap.users.api.views import UserViewSet, UserActivationView
from sdap.projects.api.views import ProjectViewSet
from sdap.results.api.views import ResultViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("v1/projects", ProjectViewSet)
router.register("v1/results", ResultViewSet)


app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    url(r'^v1/', include('djoser.urls')),
    url(r'^v1/', include('djoser.urls.authtoken')),
]
