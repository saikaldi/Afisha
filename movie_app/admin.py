from django.contrib import admin

# Register your models here.

from .models import Director,Movie, Review

admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Review)