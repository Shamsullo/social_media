from django.contrib import admin

from .models import RequestTracking


@admin.register(RequestTracking)
class RequestTrackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp')
    search_fields = ('user', 'timestamp',)
    list_display_links = ('user',)
