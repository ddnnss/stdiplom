from django.db import models
from django.utils import timezone
from pytils.translit import slugify
from PIL import Image
from django.db.models.signals import post_save
import uuid
from random import choices
import string
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.utils.safestring import mark_safe


import os


def format_number(num):
    if num % 1 == 0:
        return int(num)
    else:
        return num

class Category(models.Model):
    subcat = models.ForeignKey('self',blank=True,null=True, on_delete=models.SET_NULL,verbose_name='Относится к категории',related_name='subcats')
    name = models.CharField('Название категории', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    page_h1 = models.CharField('Тег H1', max_length=255, blank=True, null=True)
    page_title = models.CharField('Название страницы', max_length=255, blank=True, null=True)
    page_description = models.CharField('Описание страницы', max_length=255, blank=True, null=True)
    page_keywords = models.TextField('Keywords', blank=True, null=True)
    description = RichTextUploadingField('Описание категории', blank=True, null=True)
    old_id = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    isMain = models.BooleanField('Основная категория?', default=True)
    isActive = models.BooleanField('Отображать категорию?', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.name_slug:
            slug = slugify(self.name)
            testSlug = Category.objects.filter(name_slug=slug)
            if testSlug:
                slugRandom = ''
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
                self.name_slug = slug + slugRandom
            else:
                self.name_slug = slug
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        if self.isMain:
            return '{} Основная категория : {} '.format(self.old_id,self.name)
        else:
            return '{} Покатегория {} '.format(self.old_id,self.name)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.SET_NULL, verbose_name='Категория')
    name = models.CharField('Название подкатегории', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    page_h1 = models.CharField('Тег H1', max_length=255, blank=True, null=True)
    page_title = models.CharField('Название страницы', max_length=255, blank=True, null=True)
    page_description = models.CharField('Описание страницы', max_length=255, blank=True, null=True)
    page_keywords = models.TextField('Keywords', blank=True, null=True)
    description = RichTextUploadingField('Описание подкатегории', blank=True, null=True)
    views = models.IntegerField(default=0)
    old_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.name_slug:
            slug = slugify(self.name)
            testSlug = SubCategory.objects.filter(name_slug=slug)
            if testSlug:
                slugRandom = ''
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
                self.name_slug = slug + slugRandom
            else:
                self.name_slug = slug
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return 'id :%s , %s ' % (self.id, self.name)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"



class Item(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='Категория',
                                    on_delete=models.SET_NULL, db_index=True)
    image = models.ImageField('Основное изображение ', upload_to='image', blank=False)
    name = models.CharField('Название ', max_length=255, blank=True, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True,default='')
    name_slug = models.CharField(max_length=255, blank=True, null=True,db_index=True)
    price = models.IntegerField('Цена', blank=True, default=0, db_index=True)
    discount = models.IntegerField('Скидка %', blank=True, default=0, db_index=True)
    page_h1 = models.CharField('Тег H1', max_length=255, blank=True, null=True)
    page_title = models.CharField('Название страницы', max_length=255, blank=True, null=True)
    page_description = models.TextField('Описание страницы',  blank=True, null=True)
    page_keywords = models.TextField('Keywords', blank=True, null=True)
    description = RichTextUploadingField('Описание', blank=True, null=True)
    description_main = RichTextUploadingField('Описание краткое', blank=True, null=True)
    description_demo = RichTextUploadingField('Описание для демо', blank=True, null=True)
    chertezh_list = RichTextUploadingField('Информация о проекте', blank=True, null=True)
    comment = models.TextField('Комментарий', blank=True, null=True)
    model = models.CharField('Model', max_length=15, blank=True, null=True)
    sku = models.CharField('SKU', max_length=15, blank=True, null=True)
    file = models.FileField('Файл',  upload_to='files', blank=True, null=True)
    old_id = models.IntegerField(default=0)
    is_active = models.BooleanField('Отображать товар ?', default=True, db_index=True)
    buys = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_num = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        self.name_lower = self.name.lower()
        super(Item, self).save(*args, **kwargs)



    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.image.url:
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.image.url))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    image_tag.short_description = 'Основная картинка'



    @property
    def discount_value(self):
        if self.discount > 0:
            dis_val = self.price - (self.price * self.discount / 100)
        else:
            dis_val = 0
        return (format_number(dis_val))


    def __str__(self):
        return 'id:%s %s' % (self.id, self.name)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"



class ItemImage(models.Model):
    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Товар')
    image = models.ImageField('Изображение', upload_to='image', blank=False)
    image_descr = models.TextField('Описание',  blank=True, null=True)
    old_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s Изображение для товара : %s ' % (self.id, self.item.name)

    class Meta:
        verbose_name = "Изображение для товара"
        verbose_name_plural = "Изображения для товара"

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.image:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    image_tag.short_description = 'Картинка'





class PromoCode(models.Model):
    promo_code = models.CharField('Промокод (для создания рандомного значения оставить пустым)', max_length=255, blank=True, null=True)
    promo_discount = models.IntegerField('Скидка на заказ', blank=False, default=0)
    use_counts = models.IntegerField('Кол-во использований', blank=True, default=1)
    is_unlimited = models.BooleanField('Неограниченное кол-во использований', default=False)
    is_active = models.BooleanField('Активен?', default=True)
    expiry = models.DateTimeField('Срок действия безлимитного кода', blank=True, null=True)

    def __str__(self):
        if self.is_unlimited:
            return 'Неограниченный промокод со скидкой : %s . Срок действия до : %s' % (self.promo_discount, self.expiry)
        else:
            return 'Ограниченный промокод со скидкой : %s . Оставшееся кол-во использований : %s' % (self.promo_discount, self.use_counts)

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def save(self, *args, **kwargs):
        if self.is_unlimited:
            if not self.promo_code:
                self.promo_code = "LM-"+''.join(choices(string.ascii_uppercase + string.digits, k=5))
                self.use_counts = 0
        else:
            if not self.promo_code:
                self.promo_code = "LM-" + ''.join(choices(string.ascii_uppercase + string.digits, k=5))


        super(PromoCode, self).save(*args, **kwargs)




