from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_books')
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='books')

    def __str__(self):
        return f'Id {self.id}: {self.name}'


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'OK'),
        (2, 'Good'),
        (3, 'Fine'),
        (4, 'Amazing'),
        (5, 'Excellent'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)


    def __str__(self):
        return f'Id {self.id}: {self.user.username} - {self.book.name} - {self.rate} - {"like" if self.like else "no_like"}'


class City(models.Model):
    STATE_CHOICES = (
        ('Россия', 'Россия'),
        ('Турция', 'Турция'),
        ('Казахстан', 'Казахстан'),
        ('Белоруссия', 'Белоруссия'),
        ('Украина', 'Украина'),
    )
    name = models.CharField(max_length=255, null=False)
    state = models.CharField(max_length=100, choices=STATE_CHOICES, null=False)

    def __str__(self):
        return f'Id {self.id}: {self.name} - {self.state}'


class Person(models.Model):
    name = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=20, null=True)
    message_to = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'Id {self.id}: {self.name} - {self.phone} - {self.message_to}'

class House(models.Model):
    HOUSETYPE_CHOICES = (
        ('квартира', 'квартира'),
        ('дом', 'дом'),
        ('офис', 'офис'),
        ('гараж', 'гараж'),
        ('машиноместо', 'машиноместо'),
    )
    name = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    house_type = models.CharField(max_length=20, choices=HOUSETYPE_CHOICES, null=False)
    rooms = models.PositiveSmallIntegerField(default=1, null=False)
    sq_meters = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    owner = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, related_name='my_house')
    manager = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Id {self.id}: {self.name} - комн:{self.rooms} - {self.city.name} - {self.address}'
