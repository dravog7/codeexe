# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import submission
from .lang import *
import os
from subprocess import Popen,PIPE
from datetime import datetime
import json
from django.conf import settings

@shared_task
def execute(dbid):
    #save code to folder and file
    workingsub=submission.objects.filter(id=dbid)[0]
    if(workingsub.done)or(workingsub.cid!=0):
        return
    workingsub.cid=settings.CID
    workingsub.save()
    os.chdir("execution")
    #set cwd to execution folder
    #setup
    setup(workingsub)
    #execute
    execom=langexe[workingsub.lang]
    excom=securitycover(execom,workingsub.id,langt[workingsub.lang])
    #run execom
    os.chdir("{}".format(workingsub.id))
    #compile
    err=compile(workingsub)
    if(err):
        workingsub.errors=json.dumps([err])
        workingsub.done=True
        workingsub.save()
        os.chdir("..")
        os.system("rm -rf {}".format(workingsub.id))
        os.chdir("..")
        return
    out=[]
    data=[]
    for i in range(workingsub.q.testcases):
        subp=Popen(excom.format(i),stdout=PIPE,stderr=PIPE,shell=True)
        #get stdout and stderr
        out.append(subp.stdout.read().decode("UTF-8")) #output is byte string so conversion to UTF-8
        data.append(subp.stderr.read().decode("UTF-8"))
    #print("out: ",out)
    #print("err: ",data)
    #moving outputs to folder after execution to prevent access to answer
    for i in range(0,workingsub.q.testcases):
        os.system("cat ../questions/{0}/output{1}.txt>output{1}.txt".format(workingsub.q.id,i,workingsub.id))
    #eval data
    err=geterr(data) #get error msgs
    data=separate(data)
    #assert output
    outp=out[0]
    out=assertout(out)
    #combine data and out
    result=combine(data,out,err)
    if(workingsub.customin):
        result[0][1]=outp
    workingsub.testresults=json.dumps(result)
    workingsub.errors=json.dumps(err)
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
    #if customin
    if(wsub.customin):
        file=open("{}/input0.txt".format(wsub.id),'w')
        file.write(wsub.customin)
        file.close()
    #write the code to soln.(extension)
    file=open("{}/{}".format(wsub.id,langfile[wsub.lang]),'w')
    file.write(wsub.code)
    file.close()

def compile(wsub):
    if(langcompile[wsub.lang]):
        a=langcompile[wsub.lang]()
    #run command
        subp=Popen(a,stdout=PIPE,stderr=PIPE)
        err=(subp.stderr.read().decode("UTF-8"))
        return err

def securitycover(exe,wid,wt):
    #private not working ISSUE (temporarily ignored)
    exe=("time firejail --quiet --net=none --private=$(pwd) timeout {}s "+exe+"<").format(wt)
    exe+="input{}.txt"
    return exe


def geterr(data):
    e=[]
    for i in range(len(data)):
        #remove the last 2 sentences
        lines=data[i].split("\n")
        err="\n".join(lines[:len(lines)-3])
        e.append(err)
    return e

def separate(data):
    t=[]
    for i in range(len(data)):
        #time taken is written btw the words system and elapsed as min:sec.millsec format
        lines=data[i].split("\n")[-3]
        timetaken=lines[(lines.find("system")+6):(lines.find("elapsed"))].strip()
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


def combine(data,out,err):
    newarr=[]
    for i in range(len(data)):
        newarr.append([data[i],out[i]])
    return newarr