# Generated by Django 3.0 on 2020-03-11 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='client',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='item',
        ),
        migrations.RemoveField(
            model_name='order',
            name='client',
        ),
        migrations.RemoveField(
            model_name='order',
            name='guest',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='order',
            name='promo_code',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price_with_code',
        ),
        migrations.RemoveField(
            model_name='order',
            name='track_code',
        ),
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='order',
            name='fio',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='ФИО'),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Телефон'),
        ),
        migrations.DeleteModel(
            name='OrderPayment',
        ),
        migrations.DeleteModel(
            name='OrderShipping',
        ),
        migrations.DeleteModel(
            name='OrderStatus',
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
