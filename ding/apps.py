from django.apps import AppConfig
from ding.tasks import every_five_mins

class DingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ding'

    def ready():
        print('ready')
        from ding.models import DingGroup

        # from ding.models import DingGroup
