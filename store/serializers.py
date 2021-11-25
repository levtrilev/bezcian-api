
from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from store.models import Book, UserBookRelation, House, City, Person


class BookReaderSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', )


class BooksSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(source='owner.username', default="", read_only=True)
    # readers_some = BookReaderSerializer(many=True, source='readers') # если нужно иметь другое имя readers_some
    readers = BookReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name', 'likes_count', 'annotated_likes',
                  'rating', 'owner_name', 'readers')

    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')


class HousesSerializer(ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class CitiesSerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class PersonsSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'