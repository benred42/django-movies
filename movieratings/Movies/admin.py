from django.contrib import admin
from .models import Rater, Movie, Rating

class RaterAdmin(admin.ModelAdmin):
    list_display = ["raterID", "gender", "age", "occupation", "occupation_label", "get_ratings"]


class MovieAdmin(admin.ModelAdmin):
    list_display = ["movieID", "title", "genre", "get_ratings"]


class RatingAdmin(admin.ModelAdmin):
    list_display = ["raterID", "movieID", "rating", "timestamp"]

# Register your models here.
admin.site.register(Rater, RaterAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating, RatingAdmin)