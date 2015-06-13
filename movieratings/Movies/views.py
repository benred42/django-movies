from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from Movies.forms import RatingForm
from .models import Movie, Rater, Rating

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


@login_required
def new_rating(request, movie_id):
    if request.method == "POST":
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.rater = request.user.rater
            try:
                rating.validate_unique(exclude="rating")
                rating.save()

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "You have successfully rated {}".format(rating.movie))

                return redirect('rater_profile')
            except:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "You have already rated {}!".format(rating.movie))
    else:
        if movie_id:
            rating_form = RatingForm(initial={"movie": Movie.objects.get(pk=movie_id)})
        else:
            rating_form = RatingForm()
    return render(request, "Movies/rate.html", {'rating_form': rating_form})


@login_required
def edit_rating(request, movie_id):
    old_rating = Rating.objects.filter(movie=Movie.objects.get(pk=movie_id)).get(rater=request.user.rater)
    if request.method == "POST":
        rating_form = RatingForm(request.POST, instance=old_rating)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.rater = request.user.rater
            rating.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                "You have successfully edited your rating of {}".format(rating.movie))

            return redirect('rater_profile')

    else:
        rating_form = RatingForm(initial={"movie": Movie.objects.get(pk=movie_id)}, instance=old_rating)
    return render(request, "Movies/edit.html", {'rating_form': rating_form, "movie_id": movie_id})


def rater_profile(request):
        rater = Rater.objects.get(pk=request.user.rater.id)
        unseen = rater.top_unseen()[:20]
        ratings = rater.rating_set.all()
        return render(request,
                      "Movies/profile.html",
                      {"rater": rater,
                       "ratings": ratings,
                       "unseen": unseen})
