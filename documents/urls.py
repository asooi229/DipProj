from django.urls import path,include
from . import views
from django.conf.urls import url


 
urlpatterns = [
    path('', views.mainpg, name='mainpg'), 
    path('about_us/',views.about_us,name='about_us'),

]

