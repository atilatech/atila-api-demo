# Create your views here.

from rest_framework import viewsets

from scholarship.models import Scholarship
from scholarship.serializers import ScholarshipSerializer


class ScholarshipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Scholarship.objects.all()  # .order_by('-date_joined')
    serializer_class = ScholarshipSerializer
