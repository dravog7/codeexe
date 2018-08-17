from django.contrib import admin
from .models import *
# Register your models here.
class questionAdmin(admin.ModelAdmin):
    fields = ['testcases']

class submissionAdmin(admin.ModelAdmin):
    fields=['cid','done','q','lang','code','customin','errors','testresults']
admin.site.register(question, questionAdmin)
admin.site.register(submission,submissionAdmin)