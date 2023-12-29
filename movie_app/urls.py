from django.urls import path, include
from . import views
urlpatterns = [
    path('directors/', views.director_list_view),
    path('directors/<int:id>/', views.director_detail_api_view),

    path('movies/', views.movie_list_view),
    path('movies/<int:id>/', views.movie_detail_api_view),

    path('movies/reviews/', views.review_list_view),
    path('movies/reviews/<int:id>/', views.review_detail_api_view),


]
# review_list_view,movie_list_with_avg_rating