from rest_framework import serializers
from .models import Director, Movie, Review
from django.db.models import Avg
from rest_framework.exceptions import ValidationError

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = 'id name movies_count'.split()

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


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField()

class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    duration = serializers.IntegerField()
    director_id = serializers.IntegerField()

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director doesnt exists')
        return director_id


class ReviewValidateSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()
    text = serializers.CharField()
    rating = serializers.IntegerField()

    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise ValidationError('Movie doesnt exists')
        return movie_id