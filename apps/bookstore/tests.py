from django.test import TestCase
from django.contrib.auth.models import User
from apps.bookstore.models import Book, Review
from apps.bookstore.serializers import BookSerializer, ReviewSerializer
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


class BookTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            published_date="2023-01-01",
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")

    def test_review_creation(self):
        review = Review.objects.create(
            book=self.book, user=self.user, rating=5, comment="Great book!"
        )
        self.assertEqual(review.comment, "Great book!")


class BookViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            published_date="2023-01-01",
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def get_authenticated_client(self):
        client = self.client
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        return client

    def test_list_books(self):
        Book.objects.create(
            title="Another Book",
            author="Another Author",
            description="Another Description",
            published_date="2023-01-01",
        )
        Book.objects.create(
            title="Yet Another Book",
            author="Yet Another Author",
            description="Yet Another Description",
            published_date="2023-01-01",
        )

        url = reverse("book-list")
        response = self.get_authenticated_client().get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if isinstance(response.data, dict):
            books = response.data.get("results", [])
            self.assertGreaterEqual(len(books), 1)
            book_titles = [book.get("title") for book in books]
            self.assertIn("Test Book", book_titles)
        else:
            self.fail(
                f"Expected a dictionary with 'results' key but got {type(response.data)}"
            )

    def test_create_review(self):
        url = reverse("review-create", kwargs={"pk": self.book.id})
        data = {
            "rating": 5,
            "comment": "Great book!",
        }
        response = self.get_authenticated_client().post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["comment"], "Great book!")


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            published_date="2023-01-01",
        )

    def test_book_serializer(self):
        serializer = BookSerializer(self.book)
        data = serializer.data
        self.assertEqual(data["title"], "Test Book")
        self.assertEqual(data["author"], "Test Author")
        self.assertEqual(data["description"], "Test Description")
        self.assertEqual(data["published_date"], "2023-01-01")
        self.assertEqual(data["reviews"], [])


class ReviewSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            published_date="2023-01-01",
        )
        self.review = Review.objects.create(
            book=self.book, user=self.user, rating=5, comment="Great book!"
        )

    def test_review_serializer(self):
        serializer = ReviewSerializer(self.review)
        data = serializer.data
        self.assertEqual(data["comment"], "Great book!")
        self.assertEqual(data["rating"], 5)
        self.assertEqual(data["user"]["username"], self.user.username)
        self.assertEqual(data["user"]["email"], self.user.email)
