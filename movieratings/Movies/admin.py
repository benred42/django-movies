from django.contrib import admin
from .models import Rater, Movie, Rating

class RaterAdmin(admin.ModelAdmin):
    list_display = ["id", "gender", "age", "occupation", "occupation_label", "get_ratings", "get_average_rating",
                    "top_unseen"]


class MovieAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "genre", "get_ratings", "get_average_rating"]


class RatingAdmin(admin.ModelAdmin):
    list_display = ["rater", "movie", "rating", "timestamp"]

# Register your models here.
admin.site.register(Rater, RaterAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating, RatingAdmin)