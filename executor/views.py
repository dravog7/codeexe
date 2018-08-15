from django.shortcuts import render
from django.http import HttpResponse
from . import tasks
# Create your views here.
# root intro page
# /submit submit a submission object in db for execution
# /result to view submission object in db

def index(request):
    return HttpResponse("HEllo world")

def submit(request,dbid):
    tasks.execute(dbid)
    return HttpResponse("1")

def result(request,dbid):
    return dbid