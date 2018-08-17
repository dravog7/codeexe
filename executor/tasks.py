# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import submission
from .lang import *
import os
from subprocess import Popen,PIPE
from datetime import datetime
import json
@shared_task
def execute(dbid):
    #save code to folder and file
    workingsub=submission.objects.filter(id=dbid)[0]
    os.chdir("execution")
    #set cwd to execution folder
    #setup
    setup(workingsub)
    #compile
    compile(workingsub)
    #execute
    execom=langexe["python3"]
    excom=securitycover(execom,workingsub.id,langt[workingsub.lang])
    #run execom
    os.chdir("{}".format(workingsub.id))
    out=[]
    data=[]
    for i in range(workingsub.q.testcases):
        subp=Popen(excom.format(i),stdout=PIPE,stderr=PIPE,shell=True)
        #get stdout and stderr
        out.append(subp.stdout.read().decode("UTF-8"))
        data.append(subp.stderr.read().decode("UTF-8"))
    #eval data
    data=separate(data)
    #assert output
    out=assertout(out)
    #combine data and out
    result=combine(data,out)
    workingsub.testresults=json.dumps(result)
    workingsub.done=True
    workingsub.save()
    #cleanup
    os.chdir("..")
    os.system("rm -rf {}".format(workingsub.id))
    #delete folder 1
    os.chdir("..")

def setup(wsub):
    #make folder id
    os.system("mkdir {}".format(wsub.id))
    #copy inputs and outputs from questions folder
    tests=wsub.q.testcases
    for i in range(0,tests):
        os.system("cat questions/{0}/input{1}.txt>{2}/input{1}.txt".format(wsub.q.id,i,wsub.id))
        os.system("cat questions/{0}/output{1}.txt>{2}/output{1}.txt".format(wsub.q.id,i,wsub.id))
    #write the code to soln.(extension)
    file=open("{}/soln.{}".format(wsub.id,langext[wsub.lang]),'w')
    file.write(wsub.code)
    file.close()

def compile(wsub):
    if(langcompile[wsub.lang]):
        a=langcompile[wsub.lang]()
    #run command
        subp=Popen(a,stdout=PIPE,stderr=PIPE)
        print(subp.stdout.read())
        print(subp.stderr.read())

def securitycover(exe,wid,wt):
    #private not working ISSUE (temporarily ignored)
    exe=("time firejail --quiet --net=none --private timeout {}s "+exe+"<").format(wt)
    exe+="input{}.txt"
    return exe

def separate(data):
    t=[]
    for i in range(len(data)):
        #time taken is written btw the words system and elapsed as min:sec.millsec format
        timetaken=data[i][(data[i].find("system")+6):(data[i].find("elapsed"))].strip()
        timetaken=datetime.strptime(timetaken,"%M:%S.%f")
        timetaken=timetaken.strftime("%M:%S.%f")
        t.append(timetaken)
    return t

def assertout(out):
    #check by reading and equate
    correct=[]
    for i in range(len(out)):
        f=open("output{}.txt".format(i),"r")
        correctout=f.read()
        f.close()
        if(correctout==out[i]):
            correct.append(True)
        else:
            correct.append(False)
    return correct


def combine(data,out):
    newarr=[]
    for i in range(len(data)):
        newarr.append((data[i],out[i]))
    return newarr