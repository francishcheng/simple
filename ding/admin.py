from django.contrib import admin
from ding.models import DingGroup
# Register your models here.
@admin.register(DingGroup)
class DingGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "access_token", "secret"]
    search_fields = ["name"]
    # list_filter = ["is_selected"]
    list_per_page = 15
