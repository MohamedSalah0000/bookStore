from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["rating", "comment", "user", "created_at"]

    def validate_rating(self, value):
        """Ensure the rating is between 1 and 5"""
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_comment(self, value):
        """Ensure the comment does not contain SQL-like patterns"""
        if any(
            keyword in value.lower()
            for keyword in [
                "select ",
                "insert ",
                "update ",
                "delete ",
                "drop ",
                "alter ",
                "--",
                ";",
            ]
        ):
            raise serializers.ValidationError("Invalid input detected.")
        return value


class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "description", "published_date", "reviews"]
