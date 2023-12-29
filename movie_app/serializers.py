from rest_framework import serializers
from .models import Director, Movie, Review
from django.db.models import Avg

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = 'name movies_count'.split()

    def get_movies_count(self, obj):
        return obj.movies.count()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'movie text rating'.split()


class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()  # Use SerializerMethodField

    class Meta:
        model = Movie
        fields = '__all__'
        # fields = ['title', 'reviews', 'average_rating']

    def get_average_rating(self, obj):
        # Calculate and return the average rating for the movie
        reviews = obj.reviews.all()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        return round(average_rating, 2) if average_rating is not None else 0.0
