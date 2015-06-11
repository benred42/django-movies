from django.shortcuts import render
from .models import Movie, Rater

# Create your views here.
def top_20(request):
    top_movies = Movie.top_movies()
    return render(request,
                  "Movies/top20.html",
                  {"top_movies": top_movies[:20]})


def show_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    ratings = movie.rating_set.all()
    return render(request,
                  "Movies/movie.html",
                  {"movie": movie,
                   "ratings": ratings})

def show_rater(request, rater_id):
    rater = Rater.objects.get(pk=rater_id)
    ratings = rater.rating_set.all()
    return render(request,
                  "Movies/rater.html",
                  {"rater": rater,
                   "ratings": ratings})