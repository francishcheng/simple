from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


from ding.models import DingGroup

from ding.serializers import DingGroupSerializer
class DingGroupViewSets(viewsets.ModelViewSet):
    queryset = DingGroup.objects.all()
    serializer_class = DingGroupSerializer

