from django.db import models
from django.db.models.signals import post_save, post_delete
from customuser.models import User, Guest
from item.models import Item, PromoCode
from django.utils.safestring import mark_safe


class Order(models.Model):

    email = models.CharField('Email', max_length=100, blank=True, null=True)
    fio = models.CharField('ФИО', max_length=100, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=100, blank=True, null=True)
    comment = models.CharField('Комментарий', max_length=100, blank=True, null=True)
    total_price = models.IntegerField('Общая стоимость заказа', default=0)

    order_code = models.CharField('Код заказа', max_length=10, blank=True, null=True)
    is_complete = models.BooleanField('Заказ выполнен ?', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'Заказ № {self.id}. Создан : {self.created_at}. Сумма заказа : {self.total_price}'



    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def created_tag(self):
        return mark_safe('<strong>{}</strong>'.format(self.created_at.strftime('%d-%m-%Y, %H:%M:%S')))
    created_tag.short_description = mark_safe('<strong>Дaта заказа</strong>')



class ItemsInOrder(models.Model):
    order = models.ForeignKey(Order, blank=False, null=True, default=None, on_delete=models.CASCADE,
                              verbose_name='В заказе')
    item = models.ForeignKey(Item, blank=False, null=True, default=None, on_delete=models.CASCADE,
                              verbose_name='Товар')
    number = models.IntegerField('Кол-во', blank=True, null=True, default=0)
    current_price = models.IntegerField('Цена за ед.', default=0)
    total_price = models.IntegerField('Общая стоимость', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.item.discount > 0:
            self.current_price = self.item.price - (self.item.price * self.item.discount / 100)
        else:
            self.current_price = self.item.price
        self.total_price = self.number * self.current_price

        super(ItemsInOrder, self).save(*args, **kwargs)


    def __str__(self):
        return 'Товар : %s . В заказе № %s .' % (self.item.name, self.order.id)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def getfirstimage(self):
        url = None
        for img in self.item.itemimage_set.all():
            if img.is_main:
                url = img.image_small
        return url

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.getfirstimage():
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.getfirstimage()))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    def name_tag(self):
        name = self.item.name
        return name


    name_tag.short_description = 'Название товара'
    image_tag.short_description = 'Основная картинка'


def ItemsInOrder_post_save(sender,instance,**kwargs):
    try:
        order = instance.order
    except:
        order = None

    if order:
        order_total_price = 0
        all_items_in_order = ItemsInOrder.objects.filter(order=order)

        for item in all_items_in_order:
            order_total_price += item.total_price

        instance.order.total_price = order_total_price
        instance.order.save(force_update=True)


post_delete.connect(ItemsInOrder_post_save, sender=ItemsInOrder)
post_save.connect(ItemsInOrder_post_save, sender=ItemsInOrder)
