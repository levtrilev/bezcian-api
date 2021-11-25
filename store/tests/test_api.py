import json
from decimal import Decimal, Context

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book_1 = Book.objects.create(name='test book 1', author_name='author_name', price=250.25,
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='second test book 2', author_name='author_name', price=2250.20)
        self.book_3 = Book.objects.create(name='test book 3', author_name='author and book 1', price=3250.20)

    def test_get(self):
        url = reverse('book-list')
        # print(url)
        response = self.client.get(url)
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        serializer_data = BooksSerializer(books, many=True).data
        # print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)  # status.HTTP_200_OK
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'book 1'})
        books = Book.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        serializer_data = BooksSerializer(books, many=True).data
        # print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)  # status.HTTP_200_OK
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': '-price'})
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('-price')
        serializer_data = BooksSerializer(books, many=True).data  # [self.book_3, self.book_2, self.book_1]
        # print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)  # status.HTTP_200_OK
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        url = reverse('book-list')
        data = {
            'name': 'Мартин Иден',
            'price': '500.05',
            'author_name': 'Джек Лондон'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)  # status.HTTP_200_OK
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            'name': self.book_1.name,
            'price': 1500.00,
            'author_name': self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)  # status.HTTP_200_OK
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()
        self.assertEqual(1500, self.book_1.price)

    def test_update_not_owner(self):
        url = reverse('book-detail', args=(self.book_2.id,))
        self.user2 = User.objects.create(username='test_username2')
        data = {
            'name': self.book_2.name,
            'price': 1500.00,
            'author_name': self.book_2.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book_2.refresh_from_db()
        self.assertEqual('2250.20', str(self.book_2.price))

    def test_update_not_owner_but_staff(self):
        url = reverse('book-detail', args=(self.book_2.id,))
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        data = {
            'name': self.book_2.name,
            'price': 1500.00,
            'author_name': self.book_2.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_2.refresh_from_db()
        self.assertEqual('1500.00', str(self.book_2.price))

    def test_delete(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)  # status.HTTP_200_OK
        # self.assertEqual(1500, self.book_1.price)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete_not_owner(self):
        url = reverse('book-detail', args=(self.book_2.id,))
        self.user2 = User.objects.create(username='test_username2')
        self.client.force_login(self.user2)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class BooksRelationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.book_1 = Book.objects.create(name='test book 1', author_name='author_name', price=250.25,
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='second test book 2', author_name='author_name', price=2250.20)
        self.book_3 = Book.objects.create(name='test book 3', author_name='author and book 1', price=3250.20)

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            'like': True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book_1)
        self.assertTrue(relation.like)

    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            'rate': 3,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book_1)
        self.assertTrue(relation.rate)
