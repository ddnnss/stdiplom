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
    path('', views.show_cart, name='show_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('delete_from_main_cart/', views.delete_from_main_cart, name='delete_from_main_cart'),
    path('use_promo/', views.use_promo, name='use_promo'),
    path('sort_filter/', views.sort_filter, name='sort_filter'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/', views.delete_from_cart, name='delete_from_cart'),
    path('wishlist_add/', views.wishlist_add, name='wishlist_add'),
    path('wishlist_delete/', views.wishlist_delete, name='wishlist_delete'),




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
