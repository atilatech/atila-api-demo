from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from scholarship.views import ScholarshipViewSet

router = routers.DefaultRouter()
router.register(r'', ScholarshipViewSet)
# router.register(r'applications', applications.views.ApplicationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# todo access urls from root api/
# todo read about best practices for api url naming conventions

urlpatterns = [
    url(r'^', include(router.urls)),  # moved to bottom to use longest prefix matching for url (Nov 3 2017)
]
