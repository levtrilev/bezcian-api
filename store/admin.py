from django.contrib import admin
from django.contrib.admin import ModelAdmin
from store.models import Book, UserBookRelation, House, Person, City


# Register your models here.
@admin.register(Book)
class BookAdmin(ModelAdmin):
    pass


@admin.register(UserBookRelation)
class UserBookRelationAdmin(ModelAdmin):
    pass


@admin.register(House)
class HouseAdmin(ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(ModelAdmin):
    pass