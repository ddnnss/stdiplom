"""untitled1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from . import views

urlpatterns = [
    path('quick_view/', views.quick_view, name='quick_view'),
    path('<item_slug>/', views.item_page, name='item_page'),



    # path('login/', views.login, name='login'),
    # path('logout/', views.logout_page, name='logout'),
    # path('profile/<nickname_req>', views.profile, name='profile'),
    # path('del_message/', views.del_message, name='del_message'),
    # path('bonus_pack/', views.bonus_pack, name='bonus_pack'),
    # path('about_us/', views.about_us, name='about_us'),
    # path('rules/', views.rules, name='rules'),
    # path('add_to_player_balance/', views.add_to_player_balance, name='add_to_player_balance'),
    # path('about_bonus_pack/', views.about_bonus_pack, name='about_bonus_pack'),




    # path('statistic/', views.statistic, name='statistic'),

]
