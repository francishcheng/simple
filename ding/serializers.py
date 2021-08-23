from rest_framework import serializers
from ding.models import DingGroup
class DingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DingGroup
        exclude = []
        # def validate_name(self, value):
        #     if 'django' not in value.lower():
        #         raise serializers.ValidationError("Blog post is not about Django")
        #     return value
