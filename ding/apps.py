from django.apps import AppConfig
from ding.tasks import every_five_mins

class DingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ding'

        # pass
