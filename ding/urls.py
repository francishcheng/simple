from django.urls import path
from rest_framework import routers

from ding.viewsets import DingGroupViewSets



router = routers.SimpleRouter(trailing_slash=False)
router.register("dinggroup", DingGroupViewSets)


urlpatterns = [
] + router.urls


# every_five_mins()
