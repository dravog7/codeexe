from django.contrib import admin
from .models import *
# Register your models here.
class questionsAdmin(admin.ModelAdmin):
    fields = ['qid', 'testcases']

class submissionsAdmin(admin.ModelAdmin):
    fields=['dbid','cid','done','question','subdate','lang','code','customin','errors','testresults']
admin.site.register(questions, questionsAdmin)
admin.site.register(submissions,submissionsAdmin)