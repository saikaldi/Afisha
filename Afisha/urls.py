from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('movie_app.urls')),
    # path('api/v1/movies/', include('movie_app.urls')),
    # path('api/v1/reviews/', include('movie_app.urls')),
]