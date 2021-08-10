from rest_framework import serializers
from ding.models import DingGroup
class DingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DingGroup
        exclude = []
