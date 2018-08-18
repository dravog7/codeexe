from django.db import models

# Create your models here.
#questions table
#submissions table
class question(models.Model):
    testcases=models.BigIntegerField()

class submission(models.Model):
    cid=models.BigIntegerField(default=0,blank=True,null=True) #0 if not yet assigned
    done=models.BooleanField(default=False,blank=True)
    q=models.ForeignKey(question,on_delete=models.CASCADE)
    subdate=models.DateTimeField(auto_now_add=True,blank=True)
    lang=models.CharField(max_length=200)
    code=models.TextField()
    customin=models.TextField(default=None,blank=True,null=True)
    errors=models.TextField(default=None,blank=True,null=True)
    testresults=models.TextField(default=None,blank=True,null=True) #pairs of output result (WA/AC/TLE/CA) with time taken