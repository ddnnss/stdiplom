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
    path('', views.index, name='index'),
    path('category/<cat_slug>/', views.category, name='category'),
    path('category/<cat_slug>/<subcat_slug>/', views.subcategory, name='subcategory'),
    path('category/<cat_slug>/<item_slug>', views.item, name='item'),
    # path('subcategory/<subcat_slug>/', views.subcategory, name='subcategory'),
    path('collection/<collection_slug>/', views.collection, name='collection'),
    path('search/', views.search, name='search'),
    path('about_us/', views.about_us, name='about_us'),

    path('dostavka/', views.dostavka, name='dostavka'),
    path('new/', views.new, name='new'),

    path('check_email/', views.check_email, name='check_email'),
    path('order/<order_code>', views.order, name='order'),
    path('robots.txt', views.robots, name='robots'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('usloviya-pokupki/', views.usloviyapokupki, name='usloviyapokupki'),
    path('nashi-garantii/', views.nashigarantii, name='nashigarantii'),
    path('add2cart/<id>', views.add2cart, name='add2cart'),
    path('del4cart/<id>', views.del4cart, name='del4cart'),
    path('contacts/', views.contacts, name='contacts'),
    path('reviews/', views.reviews, name='reviews'),
    path('checkout/', views.checkout, name='checkout'),

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
