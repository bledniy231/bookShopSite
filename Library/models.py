from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import post_save

class Books(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор записи', blank=True, null=True)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return f'Название книги: {self.name}'

    def get_absolute_url(self):
        return f'/'

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Books, blank=True)

    def __str__(self):
        return self.user.username


def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_profile_create, sender=User)