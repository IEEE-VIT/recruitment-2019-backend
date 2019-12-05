from django.contrib import admin

from candidate.models import Candidate, Answer

# admin.site.register(Candidate)
admin.site.register(Answer)
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_no', 'interests', 'called')
    list_filter = ('called', 'round_1_call', 'room_number', 'is_active', 'times_snoozed', )
    search_fields = ('name', 'contact', 'reg_no', 'interests', 'grade', 'round_1_comment')