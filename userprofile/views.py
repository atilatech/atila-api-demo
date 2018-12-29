# Create your views here.
from rest_framework import viewsets

from userprofile.models import UserProfile
from userprofile.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all()  # .order_by('-date_joined')
    serializer_class = UserProfileSerializer
