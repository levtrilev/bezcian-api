from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def test_ok(self):
        user = User.objects.create(username='test_username', first_name='user1 f_name', last_name='user1 l_name')
        user2 = User.objects.create(username='user2')
        # self.client.force_login(self.user)
        book_1 = Book.objects.create(name='test book 1', author_name='author_name', price=250.25, owner=user)
        book_2 = Book.objects.create(name='second test book 2', author_name='author_name', price=2250.20, owner=user)
        book1_relation1 = UserBookRelation.objects.create(user=user, book=book_1, like=True, rate=5)
        book1_relation1 = UserBookRelation.objects.create(user=user, book=book_2, like=True, rate=4)
        book1_relation1 = UserBookRelation.objects.create(user=user2, book=book_2, like=False, rate=5)
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
            ).order_by('id')
        # data = BooksSerializer([book_1, book_2], many=True).data
        data = BooksSerializer(books, many=True).data
        # print(data)
        expected_data = [
            {
                'id': book_1.id,
                'name': 'test book 1',
                'price': '250.25',
                'author_name': 'author_name',
                'likes_count': 1,
                'annotated_likes': 1,
                'rating': '5.00',
                'owner_name': 'test_username',
                'readers': [
                    {
                        'first_name': 'user1 f_name',
                        'last_name': 'user1 l_name'
                    }
                ]

            },
            {
                'id': book_2.id,
                'name': 'second test book 2',
                'price': '2250.20',
                'author_name': 'author_name',
                'likes_count': 1,
                'annotated_likes': 1,
                'rating': '4.50',
                'owner_name': 'test_username',
                'readers': [
                    {
                        'first_name': 'user1 f_name',
                        'last_name': 'user1 l_name'
                    },
                    {
                        'first_name': '',
                        'last_name': ''
                    }
                ]
            }
        ]
        # print(expected_data)
        # print()
        # print(data)
        self.assertEqual(expected_data, data)
