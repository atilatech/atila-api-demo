from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

import applications.views
import scholarship.views
import scholarship.views_scholarship
import userprofile.views
from dante import views

router = routers.DefaultRouter()
router.register(r'', scholarship.views.ScholarshipViewSet)
router.register(r'applications', applications.views.ApplicationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# todo access urls from root api/
# todo read about best practices for api url naming conventions

urlpatterns = []
