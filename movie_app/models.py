from django.db import models
from django.db.models import Avg
# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    # def count_movies(self):
    #     return self.movies.count()




class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    duration = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')

    def __str__(self):
        return self.title




STAR_CHOICES = (
                (i, '*' * i) for i in range(1, 6)
            )

class Review(models.Model):
    text = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=STAR_CHOICES)

    def __str__(self):
      return self.text