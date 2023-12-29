from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from django.db.models import Avg

# Create your views here.

@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = DirectorSerializer(director)
        return Response(data=serializer.data)
    elif request.method == 'PUT':
        director.name = request.data.get('name')
        return Response(data=DirectorSerializer(director).data)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def director_list_view(request):
    if request.method == 'GET':
        # Step 1. Collect directors from DB
        directors = Director.objects.all()
        # Step 2. Serialize directors
        serializer = DirectorSerializer(directors, many=True)
        # Step 3. Return serialized directors
        return Response(data=serializer.data)
    elif request.method == 'POST':
        name = request.data.get('name')
        director = Director.objects.create(name=name)
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movies = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MovieSerializer(movies)
        return Response(data=serializer.data)
    elif request.method == 'PUT':
        movies.title = request.data.get('title')
        movies.description = request.data.get('description')
        movies.duration = request.data.get('duration')
        movies.director_id = request.data.get('director_id')
        return Response(data=MovieSerializer(movies).data)
    elif request.method == 'DELETE':
        movies.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        # Step 1. Collect directors from DB
        movies = Movie.objects.all()
        # Step 2. Serialize movie
        serializer = MovieSerializer(movies, many=True)
        # Step 3. Return serialized movies
        return Response(data=serializer.data)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')
        movie = Movie.objects.create(title=title, description=description, duration=duration, director_id=director_id)
        return Response(data=MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        reviews = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReviewSerializer(reviews)
        return Response(data=serializer.data)
    elif request.method == 'PUT':
        reviews.text = request.data.get('text')
        reviews.movie_id = request.data.get('movie_id')
        reviews.rating = request.data.get('rating')
        return Response(data=ReviewSerializer(reviews).data)
    elif request.method == 'DELETE':
        reviews.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list_view(request):
    if request.method == 'GET':
        # Step 1. Collect directors from DB
        reviews = Review.objects.all()
        # Step 2. Serialize movie
        serializer = ReviewSerializer(reviews, many=True)
        # Step 3. Return serialized movies
        return Response(data=serializer.data)
    elif request.method == 'POST':
        movie_id = request.data.get('movie_id')
        text = request.data.get('text')
        rating = request.data.get('rating')
        review = Review.objects.create(text=text, movie_id=movie_id, rating=rating)
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


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


