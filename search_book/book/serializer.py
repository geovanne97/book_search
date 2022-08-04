from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    """Serializer to books."""
    title = serializers.CharField(required=True)

class ReviewSerializer(serializers.Serializer):
    """Serializer reviews."""
    review = serializers.CharField(required=True)
    rating = serializers.IntegerField(required=True)
    book = serializers.CharField(required=True)