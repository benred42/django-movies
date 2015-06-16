from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Count, Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Movies.forms import RatingForm
from .models import Movie, Rater, Rating, Genre

# Create your views here.
def top_20(request):
    top_movies = Movie.top_movies()[:20]
    return render(request,
                  "Movies/top20.html",
                  {"top_movies": top_movies})


def top_20_by_number(request):
    top_movies = Movie.objects.annotate(num=Count("rating")).order_by("-num")
    return render(request,
                  "Movies/top20_num_ratings.html",
                  {"top_movies": top_movies[:20]})


def show_all_genres(request):
    genres = Genre.objects.all().order_by("name")
    return render(request,
                  "Movies/genres.html",
                  {"genres": genres})


def show_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    avg_rating = movie.rating_set.aggregate(Avg("rating"))['rating__avg']
    ratings = Rating.objects.filter(movie=get_object_or_404(Movie, pk=movie_id)).select_related()
    return render(request,
                  "Movies/movie.html",
                  {"movie": movie,
                   "ratings": ratings,
                   "avg_rating": avg_rating})


def show_rater(request, rater_id):
    rater = get_object_or_404(Rater, pk=rater_id)
    ratings = Rating.objects.filter(rater=get_object_or_404(Rater, pk=rater_id)).select_related()
    return render(request,
                  "Movies/rater.html",
                  {"rater": rater,
                   "ratings": ratings})


def show_genre(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = Movie.objects.filter(genres__exact=genre.id).annotate(
        avg_rating=Avg("rating__rating"),
        num=Count("rating")).filter(num__gt=0).order_by("-avg_rating")
    return render(request,
                  "Movies/genre.html",
                  {"genre": genre,
                   "movies": movies})


def show_review(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    reviewer = rating.rater.user
    return render(request,
                  "Movies/review.html",
                  {"rating": rating,
                   "reviewer": reviewer})


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
            except ValidationError:
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
    old_rating = Rating.objects.filter(movie=get_object_or_404(Movie, pk=movie_id)).get(rater=request.user.rater)
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


@login_required
def delete_rating(request, movie_id):
    old_rating = Rating.objects.filter(movie=get_object_or_404(Movie, pk=movie_id)).get(rater=request.user.rater)
    if request.method == "POST":
        old_rating.delete()
        messages.add_message(request,
                             messages.SUCCESS,
                             "You have successfully deleted your rating.")

        return redirect('rater_profile')

    return render(request, "Movies/delete.html", {"movie_id": movie_id})


def rater_profile(request):
    rater = get_object_or_404(Rater, pk=request.user.rater.id)
    unseen = rater.top_unseen()[:20]
    ratings = rater.rating_set.all()
    return render(request,
                  "Movies/profile.html",
                  {"rater": rater,
                   "ratings": ratings,
                   "unseen": unseen})


def search(request):
    if request.method == "POST":
        search_input = request.POST.get('search')
        results = Movie.objects.all()
        if search:
            results = results.filter(title__icontains=search_input)
            return render(request,
                          'Movies/search.html',
                          {'results': results})
    return render(request,
                  'Movies/search.html',
                  {'results': None})
