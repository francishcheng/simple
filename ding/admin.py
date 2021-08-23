from django.contrib import admin
from ding.models import DingGroup, Location
from ding.forms import DingGroupForm
# Register your models here.
@admin.register(DingGroup)
class DingGroupAdmin(admin.ModelAdmin):
    form = DingGroupForm
    list_display = ["name", "access_token", "secret",]
    search_fields = ["name"]
    # list_filter = ["is_selected"]
    list_per_page = 15

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['location']
    search_fields = ['location']
    list_per_page = 15

