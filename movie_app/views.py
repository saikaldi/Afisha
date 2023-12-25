from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from django.db.models import Avg
# Create your views here.

@api_view(['GET'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not found'},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = DirectorSerializer(director)
    return Response(data=serializer.data)

@api_view(['GET'])
def director_list_view(request):
    # Step 1. Collect directors from DB
    directors = Director.objects.all()
    # Step 2. Serialize directors
    serializer = DirectorSerializer(directors, many=True)
    # Step 3. Return serialized directors
    return Response(data=serializer.data)

@api_view(['GET'])
def movie_detail_api_view(request, id):
    try:
        movies = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found'},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = MovieSerializer(movies)
    return Response(data=serializer.data)

@api_view(['GET'])
def movie_list_view(request):
    # Step 1. Collect directors from DB
    movies = Movie.objects.all()
    # Step 2. Serialize movie
    serializer = MovieSerializer(movies, many=True)
    # Step 3. Return serialized movies
    return Response(data=serializer.data)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        reviews = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = ReviewSerializer(reviews)
    return Response(data=serializer.data)

@api_view(['GET'])
def review_list_view(request):
    # Step 1. Collect directors from DB
    reviews = Review.objects.all()
    print(reviews)
    # Step 2. Serialize movie
    serializer = ReviewSerializer(reviews, many=True)
    # Step 3. Return serialized movies
    print(serializer)
    return Response(data=serializer.data)


@api_view(['GET'])
def movie_list_with_avg_rating(request):
    movies = Movie.objects.values('title').annotate(average_rating=Avg('reviews__rating'))
    movie_data_list = []
    for movie in movies:
        movie_data = {
            'title': movie['title'],
            'average_rating': round(movie['average_rating'], 2) if movie['average_rating'] is not None else 0.0
        }
        movie_data_list.append(movie_data)
    return Response(data=movie_data_list)