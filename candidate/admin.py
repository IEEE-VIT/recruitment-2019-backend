from django.contrib import admin

from candidate.models import Candidate, ProjectTemplate

# admin.site.register(Candidate)
admin.site.register(ProjectTemplate)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_no', 'interests', 'called')
    list_filter = ('interests', 'called', 'round_1_call', 'room_number', 'is_active', 'times_snoozed', 'round_1_call',
                   'round_2_project_template', 'round_2_call')
    search_fields = ('name', 'contact', 'reg_no', 'interests', 'grade', 'round_1_comment')
