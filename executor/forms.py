from django.forms import ModelForm
from .models import *

class questionsForm(ModelForm):
    class Meta:
        model=questions
        fields=['qid', 'testcases']

class submissionsForm(ModelForm):
    class Meta:
        model=submissions
        fields=['dbid','cid','done','question','subdate','lang','code','customin','errors','testresults']