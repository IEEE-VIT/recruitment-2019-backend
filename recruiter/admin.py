from django.contrib import admin

from .models import User

# admin.site.register(User)
@admin.register(User)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('username', 'room_no')
    list_filter = ('username', 'room_no')
    search_fields = ('username', 'room_no')
