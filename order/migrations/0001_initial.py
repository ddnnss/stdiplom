# Generated by Django 3.0 on 2019-12-30 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customuser', '0001_initial'),
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Вариант оплаты заказа')),
            ],
            options={
                'verbose_name': 'Вариант оплаты заказа',
                'verbose_name_plural': 'Варианты оплаты заказов',
            },
        ),
        migrations.CreateModel(
            name='OrderShipping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Вариант доставки заказа')),
            ],
            options={
                'verbose_name': 'Вариант доставки заказа',
                'verbose_name_plural': 'Варианты доставки заказов',
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Статус для заказа')),
            ],
            options={
                'verbose_name': 'Статус для заказа',
                'verbose_name_plural': 'Статусы для заказов',
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='item.Item', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Закладка клиента',
                'verbose_name_plural': 'Закладки клиентов',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.IntegerField(default=0, verbose_name='Общая стоимость заказа')),
                ('total_price_with_code', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Общая стоимость заказа с учетом промо-кода')),
                ('track_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Трек код')),
                ('order_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Код заказа')),
                ('is_complete', models.BooleanField(default=False, verbose_name='Заказ выполнен ?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Заказ клиента')),
                ('guest', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='customuser.Guest', verbose_name='Заказ гостя')),
                ('payment', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.OrderPayment', verbose_name='Оплата заказа')),
                ('promo_code', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='item.PromoCode', verbose_name='Использованный промо-код')),
                ('shipping', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.OrderShipping', verbose_name='Доставка заказа')),
                ('status', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.OrderStatus', verbose_name='Статус заказа')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='ItemsInOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, default=0, null=True, verbose_name='Кол-во')),
                ('current_price', models.IntegerField(default=0, verbose_name='Цена за ед.')),
                ('total_price', models.IntegerField(default=0, verbose_name='Общая стоимость')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='item.Item', verbose_name='Товар')),
                ('order', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.Order', verbose_name='В заказе')),
            ],
            options={
                'verbose_name': 'Товар в заказе',
                'verbose_name_plural': 'Товары в заказе',
            },
        ),
    ]
