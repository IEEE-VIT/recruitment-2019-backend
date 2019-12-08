from django.contrib import admin

from candidate.models import Candidate, ProjectTemplate
from django.contrib.admin import SimpleListFilter

admin.site.register(ProjectTemplate)


class InterestFilter(SimpleListFilter):
    title = 'InterestFilter'
    parameter_name = 'interests'
    interests = ['ML', 'WebDev', 'AppDev', 'Electronics', 'CyberSec', 'CompetitiveCoding', 'SponsorshipAndFinance',
                 'Outreach', 'SocialMediaAndMarketing', 'Documentation', 'Relations', 'UI', 'VFX', 'Poster']

    def lookups(self, request, model_admin):
        return ((interest, interest) for interest in self.interests)

    def queryset(self, request, queryset):
        for interest in self.interests:
            if self.value() == interest:
                return queryset.filter(interests__contains=interest)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_no', 'interests', 'called')
    list_filter = (
        InterestFilter, 'called', 'round_1_call', 'room_number', 'is_active', 'times_snoozed', 'round_1_call',
        'round_2_project_template', 'round_2_call')
    search_fields = ('name', 'contact', 'reg_no', 'interests', 'grade', 'round_1_comment')
