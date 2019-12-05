from django.contrib import admin

from candidate.models import Candidate, Answer

# admin.site.register(Candidate)
admin.site.register(Answer)
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_no', 'grade', 'is_active', 'interests', 'tech_interests', 'email_sent')
    list_filter = ('is_active', 'grade', 'interests', 'tech_interests', 'email_sent')
    search_fields = ('name', 'contact', 'reg_no', 'interests', 'tech_interests', 'grade', 'comment')