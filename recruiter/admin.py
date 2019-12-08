from django.contrib import admin

from .models import User, AvailableRoom

# admin.site.register(User)
admin.site.register(AvailableRoom)
@admin.register(User)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('username', 'room_no')
    list_filter = ('username', 'room_no')
    search_fields = ('username', 'room_no')
