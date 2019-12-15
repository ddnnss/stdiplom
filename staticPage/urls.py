from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [

   path('', views.index, name='index'),
   path('index.html', RedirectView.as_view(url='/', permanent=False), name='index1'),
   path('index.php', RedirectView.as_view(url='/', permanent=False), name='index2'),
   # # path('posts/', views.allPosts, name='allposts'),
   path('nashi-garantii/', views.nashi_garantii, name='nashi_garantii'),
   path('usloviya-pokupki/', views.usloviya_pokupki, name='usloviya_pokupki-pokupki'),

   path('testimonial/', views.testimonial, name='testimonial'),
   path('zakaz/', views.zakaz, name='zakaz'),
   path('contact-us/', views.contact_us, name='contact_us'),
   # path('robots.txt', views.robots, name='robots'),



]
