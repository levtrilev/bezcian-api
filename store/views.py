from django.db.models import Count, Case, When, Avg
from django.shortcuts import render
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from store.models import Book, UserBookRelation, House, City, Person
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BooksSerializer, UserBookRelationSerializer, HousesSerializer, CitiesSerializer, \
    PersonsSerializer
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class CitiesViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitiesSerializer


class PersonsViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonsSerializer


class HousesViewSet(ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HousesSerializer


class BooksViewSet(ModelViewSet):
    queryset = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).select_related('owner').prefetch_related('readers').order_by('id')
    serializer_class = BooksSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]  # IsAuthenticatedOrReadOnly
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['price']  # http://127.0.0.1:8000/book/?price=500
    search_fields = ['name', 'author_name']  # http://127.0.0.1:8000/book/?search=Petrov
    ordering_fields = ['price',
                       'author_name']  # http://127.0.0.1:8000/book/?ordering=price  (-price)(author_name,price)

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBooksRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])
        return obj


def auth(request):
    return render(request, 'oauth.html')
