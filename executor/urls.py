from django.urls import path

from . import views

urlpatterns = [
    # /
    path('', views.index, name='index'),
    path('<int:dbid>/',views.submit,name='submit'),
    path('<int:dbid>/result/',views.result,name='result'),
]
