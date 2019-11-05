from django.contrib import admin

from candidate.models import Candidate, Answer

admin.site.register(Candidate)
admin.site.register(Answer)