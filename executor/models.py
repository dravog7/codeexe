from django.db import models

# Create your models here.
#questions table
#submissions table
class questions(models.Model):
    testcases=models.BigIntegerField()

class submissions(models.Model):
    cid=models.BigIntegerField() #0 if not yet assigned
    done=models.BooleanField()
    question=models.ForeignKey(questions,on_delete=models.CASCADE)
    subdate=models.DateTimeField()
    lang=models.CharField(max_length=200)
    code=models.TextField()
    customin=models.TextField()
    errors=models.TextField()
    testresults=models.TextField() #pairs of output result (WA/AC/TLE/CA) with time taken