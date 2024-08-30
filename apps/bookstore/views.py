from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.prefetch_related("reviews").all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def get_book(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Book, pk=pk)

    def perform_create(self, serializer):
        book = self.get_book()
        serializer.save(user=self.request.user, book=book)
