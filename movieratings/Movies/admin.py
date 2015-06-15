from django.contrib import admin
from .models import Rater, Movie, Rating, Genre

class RaterAdmin(admin.ModelAdmin):
    list_display = ["id", "gender", "age", "occupation", "get_occupation_display", "get_ratings", "get_average_rating"]


class MovieAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "get_genres", "get_ratings", "get_average_rating"]


class RatingAdmin(admin.ModelAdmin):
    list_display = ["rater", "movie", "rating", "review", "timestamp"]

# Register your models here.
admin.site.register(Rater, RaterAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Genre)
