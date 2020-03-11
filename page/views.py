from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import Banner
from item.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from customuser.forms import SignUpForm, UpdateForm
from order.models import *
from cart.models import Cart
from customuser.models import User, Guest
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import Http404


from openpyxl import load_workbook



def create_password():
    from random import choices
    import string
    password = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
    return password

def is_email(string):

    from django.core.exceptions import ValidationError
    from django.core.validators import EmailValidator

    validator = EmailValidator()
    try:
        validator(string)
    except ValidationError:
        return False

    return True

def check_email(request):
    return_dict = {}
    email = request.POST.get('email')
    print(email)
    email_error = ''
    if is_email(email):
        email_is_valid = True
    else:
        email_is_valid = False
        email_error = 'Указанный адрес почты не верный'

    try:
        user = User.objects.get(email=email)
    except:
        user = None

    if user:
        email_is_valid = False
        email_error = 'Указанный адрес почты уже зарегистрирован'

    return_dict['result'] = email_is_valid
    return_dict['email_error'] = email_error
    return JsonResponse(return_dict)


def order(request, order_code):
    try:
        order = Order.objects.get(order_code=order_code)
    except:
        order=None

    if order:
        return render(request, 'page/order_complete.html', locals())
    else:
        raise Http404
        # return render(request, '404.html', locals())

def about_us(request):
    title = 'О НАС'
    show_tags = True
    if request.GET.get('sendmail') == '1':
        users = User.objects.all()
        for user in users:
            msg_html = render_to_string('email/sendmail.html')
            send_mail('Летняя скидка -15% в Лакшми888', None, 'info@lakshmi888.ru', [user.email],
                  fail_silently=False, html_message=msg_html)
    return render(request, 'page/about_us.html', locals())


def robots(request):

    return render(request, 'page/robots.txt')

def sitemap(request):
    return render(request, 'page/sitemap.xml', content_type = "application/xhtml+xml")

def usloviyapokupki(request):

    title = 'Условия покупки дипломного проекта'
    return render(request, 'page/usloviyapokupki.html', locals())

def nashigarantii(request):
    title = 'Наши гарантии при покупке дипломного проекта. возможность покупать проект по частям'
    return render(request, 'page/nashi-garantii.html', locals())

def add2cart(request,id):
    s_key = request.session.session_key
    if request.user.is_authenticated:
        print('User is_authenticated')
        addtocart, created = Cart.objects.get_or_create(client=request.user,
                                                        item_id=id, defaults={'number': 1})
        if not created:
            addtocart.number += 1
            addtocart.save(force_update=True)

    else:
        print('User is_not authenticated')
        try:
            guest = Guest.objects.get(session=s_key)
            print('Guest already created')
        except:
            guest = None

        if not guest:
            guest = Guest.objects.create(session=s_key)
            guest.save()
            print('Guest created')

        addtocart, created = Cart.objects.get_or_create(guest=guest,
                                                        item_id=id, defaults={'number': 1})
        if not created:
            addtocart.number += 1
            addtocart.save(force_update=True)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def del4cart(request,id):
    s_key = request.session.session_key

    if request.user.is_authenticated:
        print('User is_authenticated')
        Cart.objects.filter(client=request.user, item_id=id).delete()

    else:
        print('User is_not authenticated')

        guest = Guest.objects.get(session=s_key)
        Cart.objects.filter(guest=guest, item_id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def contacts(request):
    show_tags = True
    title = 'Связаться с нами'
    return render(request, 'page/contacts.html', locals())

def reviews(request):
    show_tags = True
    title = 'Отзывы покупателей'
    return render(request, 'page/reviews.html', locals())
def dostavka(request):
    show_tags = True
    title = 'ИНФОРМАЦИЯ О ДОСТАВКЕ'
    return render(request, 'page/dostavka.html', locals())


def new(request):
    all_items = Item.objects.filter(is_new=True, is_active=True, is_present=True).order_by('-created_at')
    not_present = Item.objects.filter(is_new=True, is_active=True, is_present=False)
    data = request.GET
    print(request.GET)
    search = data.get('search')
    filter = data.get('filter')
    order = data.get('order')
    count = data.get('count')
    page = request.GET.get('page')
    search_qs = None
    filter_sq = None
    if search:
        items = all_items.filter(name_lower__contains=search.lower())
        if not items:
            items = all_items.filter(article__contains=search)
        search_qs = items

        param_search = search

    if filter == 'new':
        print('Поиск по фильтру туц')
        if search_qs:
            items = search_qs.filter(is_new=True)
            filter_sq = items
            param_filter = filter
        else:
            items = all_items.filter(is_new=True)
            filter_sq = items
            param_filter = filter

        param_filter = 'new'

    if filter and filter != 'new':
        print('Поиск по фильтру')

        if search_qs:
            items = search_qs.filter(filter__name_slug=filter)
            filter_sq = items
            param_filter = filter
        else:
            items = all_items.filter(filter__name_slug=filter)
            filter_sq = items
            param_filter = filter

    if order:
        if search_qs and filter_sq:
            items = filter_sq.order_by(order)
        elif filter_sq:
            items = filter_sq.order_by(order)
        elif search_qs:
            items = search_qs.order_by(order)
        else:
            items = all_items.order_by(order)
        param_order = order

    if not search and not order and not filter:
        items = all_items
        # subcat.views = subcat.views + 1
        # subcat.save()
        param_order = '-created_at'

    if count:
        items_paginator = Paginator(items, int(count))
        param_count = count
    else:
        items_paginator = Paginator(items, 12)

    if page:
        canonical_link = '/new/'

    try:
        items = items_paginator.get_page(page)
    except PageNotAnInteger:
        items = items_paginator.page(1)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)
    show_tags = False
    return render(request, 'page/new.html', locals())




def checkout(request):
    show_tags = True
    if request.POST:
        fio = request.POST.get('fio')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        comment = request.POST.get('comment')
        order_code = create_password()
        order = Order.objects.create(fio=fio,email=email,phone=phone,comment=comment,order_code=order_code)

        s_key = request.session.session_key
        guest = Guest.objects.get(session=s_key)
        all_cart_items = Cart.objects.filter(guest=guest)
        for item in all_cart_items:
            ItemsInOrder.objects.create(order_id=order.id, item_id=item.item.id, number=item.number,
                                        current_price=item.item.price)
            item.item.buys = item.item.buys + 1
            item.item.save(force_update=True)
        all_cart_items.delete()

        new_order = Order.objects.get(id=order.id)
        # msg_html = render_to_string('email/new_order.html', {'order': new_order})
        # send_mail('Заказ успешно размещен', None, 'info@lakshmi888.ru', [email],
        #           fail_silently=False, html_message=msg_html)
        # send_mail('Новый заказ', None, 'norply@lakshmi888.ru', ['info@lakshmi888.ru'],
        #           fail_silently=False, html_message=msg_html)
        print('Email sent')
        return HttpResponseRedirect('/order/{}'.format(new_order.order_code))


#-------------------------------------------------------------------------------GET request

    return render(request, 'page/checkout.html', locals())




def index(request):
    allCategories = Category.objects.filter(isActive = True, isMain = True).order_by('-id')
    allSubCat = Category.objects.filter(isActive = True, isMain = False).order_by('-id')
    recomended = Item.objects.all().order_by('-views')[:10]

    for i in allSubCat:
        print(i)


    # show_tags = True
    # title = 'Лакшми888 - Магазин Фен Шуй'
    # description = 'Интернет Магазин фен шуй товаров: у нас вы можете купить фен шуй товары по выгодным ценам. Доставка во все регионы.'
    # keywords = ''
    # banners = Banner.objects.filter(is_active=True).order_by('order')
    #
    # main_category = Category.objects.all()
    return render(request, 'page/index.html', locals())


# def category(request, cat_slug):
#     try:
#         cat = Category.objects.get(name_slug=cat_slug)
#         # cat.views += 1
#         # cat.save()
#         title = cat.page_title
#         description = cat.page_description
#         keywords = cat.page_keywords
#         subcats = SubCategory.objects.filter(category=cat)
#     except:
#         raise Http404
#         # return render(request, '404.html', locals())
#     show_tags = True
#
#     return render(request, 'page/category.html', locals())

def item(request, cat_slug, item_slug):
    allCategories = Category.objects.filter(isActive=True, isMain=True).order_by('-id')
    allSubCat = Category.objects.filter(isActive=True, isMain=False).order_by('-id')
    item = Item.objects.get(name_slug=item_slug)
    name = item.name.split(' ')
    print(name)
    simlar = Item.objects.filter(name__contains=name[0])
    other = Item.objects.filter(category__name_slug=cat_slug)[:5]
    item.views += 1
    item.save()
    return render(request, 'page/item.html', locals())

def category(request, cat_slug):
    # it = Item.objects.all()
    # for i in it:
    #     i.description = i.description.replace('<p>&nbsp;</p>', '').replace('<p>&amp;</p>', '')
    #     i.description_main = i.description_main.replace('<p>&nbsp;</p>', '').replace('<p>&amp;</p>', '')
    #     try:
    #         i.description_demo = i.description_demo.replace('<p>&nbsp;</p>', '').replace('<p>&amp;</p>', '')
    #     except:
    #         pass
    #
    #     try:
    #         i.chertezh_list = i.chertezh_list.replace('<p>&nbsp;</p>', '').replace('<p>&amp;</p>', '')
    #     except:
    #         pass
    #
    #     i.save()
    #     print(i.id)
    # it = Category.objects.all()
    # for i in it:
    #     try:
    #         i.description = i.description.replace('&lt;!--noindex--&gt;', '').replace('&lt;!--/noindex--&gt;', '').replace(
    #             '&lt;', '<').replace('&gt;', '>')
    #         i.save()
    #     except:
    #         pass

    try:

        cat = Category.objects.get(name_slug=cat_slug)
        all_items = Item.objects.filter(category=cat, is_active=True).order_by('-created_at')
        allCategories = Category.objects.filter(isActive=True, isMain=True).order_by('-id')
        allSubCat = Category.objects.filter(isActive=True, isMain=False).order_by('-id')
        print(all_items)
        title = cat.page_title
        description = cat.page_description
        keywords = cat.page_keywords
    except:
        raise Http404
        # return render(request, '404.html', locals())
    data = request.GET
    print(request.GET)
    search = data.get('search')
    filter = data.get('filter')
    order = data.get('order')
    count = data.get('count')
    page = request.GET.get('page')
    search_qs = None
    filter_sq = None
    np_search_qs = None
    np_filter_sq = None
    if search:
        items = all_items.filter(name_lower__contains=search.lower())


        if not items:
            items = all_items.filter(article__contains=search)

        search_qs = items

        param_search = search

    if filter == 'new':
        print('Поиск по фильтру туц')
        if search_qs:
            items = search_qs.filter(is_new=True)

            filter_sq = items

            param_filter = filter
        else:
            items = all_items.filter(is_new=True)

            filter_sq = items

            param_filter = filter

        param_filter = 'new'

    if filter and filter != 'new':
        print('Поиск по фильтру')

        if search_qs:
            items = search_qs.filter(filter__name_slug=filter)

            filter_sq = items

            param_filter = filter
        else:
            items = all_items.filter(filter__name_slug=filter)

            filter_sq = items

            param_filter = filter

    if order:
        if search_qs and filter_sq:
            items = filter_sq.order_by(order)
        elif filter_sq:
            items = filter_sq.order_by(order)
        elif search_qs:
            items = search_qs.order_by(order)
        else:
            items = all_items.order_by(order)
        param_order = order

    if not search and not order and not filter:
        items = all_items

        # subcat.views = subcat.views + 1
        # subcat.save()
        param_order = '-created_at'

    if count:
        items_paginator = Paginator(items, int(count))
        param_count = count
    else:
        items_paginator = Paginator(items, 15)



    try:
        items = items_paginator.get_page(page)
        show_tags = False
    except PageNotAnInteger:
        items = items_paginator.page(1)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)

    return render(request, 'page/category.html', locals())

def subcategory(request, cat_slug,subcat_slug):
    # it = Item.objects.all()
    # for i in it:
    #     i.description = i.description.replace('<p>&nbsp;</p>', '').replace('<p>&amp;</p>', '')
    #     i.description_main = i.description_main.replace('<p>&nbsp;</p>', '').replace('<p>&amp;</p>', '')
    #     try:
    #         i.description_demo = i.description_demo.replace('<p>&nbsp;</p>', '').replace('<p>&amp;</p>', '')
    #     except:
    #         pass
    #
    #     try:
    #         i.chertezh_list = i.chertezh_list.replace('<p>&nbsp;</p>', '').replace('<p>&amp;</p>', '')
    #     except:
    #         pass
    #
    #     i.save()
    #     print(i.id)
    # it = Category.objects.all()
    # for i in it:
    #     try:
    #         i.description = i.description.replace('&lt;!--noindex--&gt;', '').replace('&lt;!--/noindex--&gt;', '').replace(
    #             '&lt;', '<').replace('&gt;', '>')
    #         i.save()
    #     except:
    #         pass

    try:

        cat = Category.objects.get(name_slug=subcat_slug)
        all_items = Item.objects.filter(category=cat, is_active=True).order_by('-created_at')
        print(all_items)
        allCategories = Category.objects.filter(isActive=True, isMain=True).order_by('-id')
        allSubCat = Category.objects.filter(isActive=True, isMain=False).order_by('-id')
        print(allSubCat)
        title = cat.page_title
        description = cat.page_description
        keywords = cat.page_keywords
    except:
        raise Http404
        # return render(request, '404.html', locals())
    data = request.GET
    print(request.GET)
    search = data.get('search')
    filter = data.get('filter')
    order = data.get('order')
    count = data.get('count')
    page = request.GET.get('page')
    search_qs = None
    filter_sq = None
    np_search_qs = None
    np_filter_sq = None
    if search:
        items = all_items.filter(name_lower__contains=search.lower())


        if not items:
            items = all_items.filter(article__contains=search)

        search_qs = items

        param_search = search

    if filter == 'new':
        print('Поиск по фильтру туц')
        if search_qs:
            items = search_qs.filter(is_new=True)

            filter_sq = items

            param_filter = filter
        else:
            items = all_items.filter(is_new=True)

            filter_sq = items

            param_filter = filter

        param_filter = 'new'

    if filter and filter != 'new':
        print('Поиск по фильтру')

        if search_qs:
            items = search_qs.filter(filter__name_slug=filter)

            filter_sq = items

            param_filter = filter
        else:
            items = all_items.filter(filter__name_slug=filter)

            filter_sq = items

            param_filter = filter

    if order:
        if search_qs and filter_sq:
            items = filter_sq.order_by(order)
        elif filter_sq:
            items = filter_sq.order_by(order)
        elif search_qs:
            items = search_qs.order_by(order)
        else:
            items = all_items.order_by(order)
        param_order = order

    if not search and not order and not filter:
        items = all_items

        # subcat.views = subcat.views + 1
        # subcat.save()
        param_order = '-created_at'

    if count:
        items_paginator = Paginator(items, int(count))
        param_count = count
    else:
        items_paginator = Paginator(items, 12)

    print(items)

    try:
        items = items_paginator.get_page(page)
        show_tags = False
    except PageNotAnInteger:
        items = items_paginator.page(1)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)

    return render(request, 'page/category.html', locals())

def collection(request, collection_slug):
    try:
        collection = Collection.objects.get(name_slug=collection_slug)
        all_items = collection.item_set.filter(is_active=True, is_present=True).order_by('-created_at')
        not_present = collection.item_set.filter(is_active=True, is_present=False)
        title = collection.page_title
        description = collection.page_description
        keywords = collection.page_keywords
       # all_items = Item.objects.filter(collection__name_slug=collection_slug)
    except:
        return render(request, '404.html', locals())
    data = request.GET
    print(request.GET)
    search = data.get('search')
    filter = data.get('filter')
    order = data.get('order')
    count = data.get('count')
    page = request.GET.get('page')
    search_qs = None
    filter_sq = None
    if search:
        items = all_items.filter(name_lower__contains=search.lower())

        if not items:
            items = all_items.filter(article__contains=search)
        search_qs = items

        param_search = search

    if filter == 'new':
        print('Поиск по фильтру туц')
        if search_qs:
            items = search_qs.filter(is_new=True)
            filter_sq = items
            param_filter = filter
        else:
            items = all_items.filter(is_new=True)
            filter_sq = items
            param_filter = filter

        param_filter = 'new'

    if filter and filter != 'new':
        print('Поиск по фильтру')

        if search_qs:
            items = search_qs.filter(filter__name_slug=filter)
            filter_sq = items
            param_filter = filter
        else:
            items = all_items.filter(filter__name_slug=filter)
            filter_sq = items
            param_filter = filter

    if order:
        if search_qs and filter_sq:
            items = filter_sq.order_by(order)
        elif filter_sq:
            items = filter_sq.order_by(order)
        elif search_qs:
            items = search_qs.order_by(order)
        else:
            items = all_items.order_by(order)
        param_order = order

    if not search and not order and not filter:
        items = all_items
        # subcat.views = subcat.views + 1
        # subcat.save()
        param_order = '-created_at'

    if count:
        items_paginator = Paginator(items, int(count))
        param_count = count
    else:
        items_paginator = Paginator(items, 12)

    if page:
        canonical_link = '/collection/' + collection.name_slug

    try:
        items = items_paginator.get_page(page)
    except PageNotAnInteger:
        items = items_paginator.page(1)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)
    show_tags = False
    return render(request, 'page/collection.html', locals())


def search(request):
    show_tags = False
    search_string = request.GET.get('search')
    page = request.GET.get('page')
    param_search = search_string
    try:
        items = Item.objects.filter(name_lower__contains=search_string.lower(), is_active=True)
    except:
        return render(request, '404.html', locals())
    if not items:
        items = Item.objects.filter(name_lower__contains=search_string.lower()[:-1], is_active=True)
    if not items:
        items = Item.objects.filter(article__contains=search_string)
    items_paginator = Paginator(items, 12)
    try:
        items = items_paginator.get_page(page)
    except PageNotAnInteger:
        items = items_paginator.page(1)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)

    return render(request, 'page/search.html', locals())


