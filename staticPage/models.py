from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class UserProfile(models.Model):
    pass

class Category(models.Model):
    pass


class SubCategory(models.Model):
    category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.SET_NULL, verbose_name='Категория')
    pass


class Item(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Категория')
    subcategory = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Подкатегория')
    pass



class Order(models.Model):
    pass

class Comment(models.Model):
    pass

class ItemImage(models.Model):
    pass


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()