from rest_framework import viewsets
from .serializers import DescriptionSerializer
from .models import Description


class DescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer