from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from userprofile.views import UserProfileViewSet

router = routers.DefaultRouter()
router.register(r'', UserProfileViewSet)
# router.register(r'applications', applications.views.ApplicationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    url(r'^', include(router.urls)),  # moved to bottom to use longest prefix matching for url (Nov 3 2017)
]
