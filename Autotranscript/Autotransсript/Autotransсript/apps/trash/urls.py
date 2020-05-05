from django.urls import path
from . import views

urlpatterns = [
    path('',views.output, name ="script"),
    path('', views.download, name = 'script2')

]
