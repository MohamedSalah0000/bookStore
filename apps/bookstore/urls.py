from django.urls import path
from .views import BookListView, BookDetailView, ReviewCreateView

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/<int:pk>/reviews/", ReviewCreateView.as_view(), name="review-create"),
]
