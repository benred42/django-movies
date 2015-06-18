from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Count, Avg
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Movies.forms import RatingForm
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, TemplateView, UpdateView
from .models import Movie, Rater, Rating, Genre

# Create your views here.
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class Top20ListView(ListView):
    model = Movie
    paginate_by = 20
    context_object_name = "top_movies"
    template_name = "Movies/top20.html"
    queryset = Movie.objects.annotate(avg_rating=Avg("rating__rating"), num=Count("rating")).filter(num__gt=9).order_by(
        "-avg_rating")


class Top20ByNumber(Top20ListView):
    queryset = Movie.objects.annotate(num=Count("rating")).order_by("-num")
    template_name = "Movies/top20_num_ratings.html"


class GenresList(ListView):
    model = Genre
    context_object_name = "genres"
    template_name = "Movies/genres.html"
    queryset = Genre.objects.all().order_by("name")


class MovieList(ListView):
    model = Rating
    context_object_name = "ratings"
    template_name = "Movies/movie.html"
    paginate_by = 20

    def get_queryset(self):
        movie_id = self.kwargs["movie_id"]
        return Rating.objects.filter(movie=get_object_or_404(Movie, pk=movie_id)).select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_id = self.kwargs["movie_id"]
        movie = get_object_or_404(Movie, pk=movie_id)
        avg_rating = movie.rating_set.aggregate(Avg("rating"))['rating__avg']
        context['movie'] = movie
        context['avg_rating'] = avg_rating
        return context


class RaterList(ListView):
    model = Rating
    context_object_name = "ratings"
    template_name = "Movies/rater.html"
    paginate_by = 20

    def get_queryset(self):
        rater_id = self.kwargs["rater_id"]
        return Rating.objects.filter(rater=get_object_or_404(Rater, pk=rater_id)).select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rater_id = self.kwargs["rater_id"]
        rater = get_object_or_404(Rater, pk=rater_id)
        context['rater'] = rater
        return context


class ProfileListView(ListView):
    model = Rating
    context_object_name = "ratings"
    template_name = "Movies/profile.html"
    paginate_by = 10

    def get_queryset(self):
        rater_id = self.request.user.rater.id
        return Rating.objects.filter(rater=get_object_or_404(Rater, pk=rater_id)).select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rater_id = self.request.user.rater.id
        rater = get_object_or_404(Rater, pk=rater_id)
        unseen = Movie.objects.exclude(rating__in=rater.rating_set.all()).annotate(avg_rating=Avg("rating__rating"),
                                                                                   num=Count("rating")).filter(
            num__gt=9).order_by("-avg_rating")[:20]
        context['rater'] = rater
        context['unseen'] = unseen
        return context


class GenreList(ListView):
    model = Movie
    context_object_name = "movies"
    template_name = "Movies/genre.html"
    paginate_by = 20

    def get_queryset(self):
        genre_id = self.kwargs["genre_id"]
        return Movie.objects.filter(genres__exact=genre_id).annotate(
            avg_rating=Avg("rating__rating"),
            num=Count("rating")).filter(num__gt=0).order_by("-avg_rating")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_id = self.kwargs["genre_id"]
        genre = get_object_or_404(Genre, pk=genre_id)
        context['genre'] = genre
        return context


class ShowReview(TemplateView):
    template_name = "Movies/review.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rating_id = self.kwargs["rating_id"]
        rating = get_object_or_404(Rating, pk=rating_id)
        context["rating"] = rating
        context["reviewer"] = rating.rater.user
        return context


class NewRating(LoginRequiredMixin, View):
    def get(self, request, movie_id):
        if movie_id:
            rating_form = RatingForm(initial={"movie": Movie.objects.get(pk=movie_id)})
        else:
            rating_form = RatingForm()
        return render(request, "Movies/rate.html", {'rating_form': rating_form})

    def post(self, request, movie_id):
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
        return render(request, "Movies/rate.html", {'rating_form': rating_form})


class Search(View):
    def post(self, request):
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


# def top_20(request):
#     top_movies = Movie.top_movies()[:20]
#     return render(request,
#                   "Movies/top20.html",
#                   {"top_movies": top_movies})
#
#
# def top_20_by_number(request):
#     top_movies = Movie.objects.annotate(num=Count("rating")).order_by("-num")
#     return render(request,
#                   "Movies/top20_num_ratings.html",
#                   {"top_movies": top_movies[:20]})
#
#
# def show_all_genres(request):
#     genres = Genre.objects.all().order_by("name")
#     return render(request,
#                   "Movies/genres.html",
#                   {"genres": genres})
#
#
# def show_movie(request, movie_id):
#     movie = get_object_or_404(Movie, pk=movie_id)
#     avg_rating = movie.rating_set.aggregate(Avg("rating"))['rating__avg']
#     ratings = Rating.objects.filter(movie=get_object_or_404(Movie, pk=movie_id)).select_related()
#     return render(request,
#                   "Movies/movie.html",
#                   {"movie": movie,
#                    "ratings": ratings,
#                    "avg_rating": avg_rating})
#
#
# def show_rater(request, rater_id):
#     rater = get_object_or_404(Rater, pk=rater_id)
#     ratings = Rating.objects.filter(rater=get_object_or_404(Rater, pk=rater_id)).select_related()
#     return render(request,
#                   "Movies/rater.html",
#                   {"rater": rater,
#                    "ratings": ratings})
#
#
# def rater_profile(request):
#     rater = get_object_or_404(Rater, pk=request.user.rater.id)
#     unseen = Movie.objects.exclude(rating__in=rater.rating_set.all()).annotate(avg_rating=Avg("rating__rating"),
#                                                                                num=Count("rating")).filter(
#         num__gt=9).order_by("-avg_rating")[:20]
#     ratings = rater.rating_set.all().select_related()
#     return render(request,
#                   "Movies/profile.html",
#                   {"rater": rater,
#                    "ratings": ratings,
#                    "unseen": unseen})
#
#
# def show_genre(request, genre_id):
#     page = request.GET.get('page', 1)
#     genre = get_object_or_404(Genre, pk=genre_id)
#     movies = Movie.objects.filter(genres__exact=genre.id).annotate(
#         avg_rating=Avg("rating__rating"),
#         num=Count("rating")).filter(num__gt=0).order_by("-avg_rating")
#     movie_paginator = Paginator(movies, 20)
#     return render(request,
#                   "Movies/genre.html",
#                   {"genre": genre,
#                    "movies": movie_paginator.page(page)})
#
#
# def show_review(request, rating_id):
#     rating = get_object_or_404(Rating, pk=rating_id)
#     reviewer = rating.rater.user
#     return render(request,
#                   "Movies/review.html",
#                   {"rating": rating,
#                    "reviewer": reviewer})
#
#
# @login_required
# def new_rating(request, movie_id):
#     if request.method == "POST":
#         rating_form = RatingForm(request.POST)
#         if rating_form.is_valid():
#             rating = rating_form.save(commit=False)
#             rating.rater = request.user.rater
#             try:
#                 rating.validate_unique(exclude="rating")
#                 rating.save()
#
#                 messages.add_message(
#                     request,
#                     messages.SUCCESS,
#                     "You have successfully rated {}".format(rating.movie))
#
#                 return redirect('rater_profile')
#             except ValidationError:
#                 messages.add_message(
#                     request,
#                     messages.ERROR,
#                     "You have already rated {}!".format(rating.movie))
#     else:
#         if movie_id:
#             rating_form = RatingForm(initial={"movie": Movie.objects.get(pk=movie_id)})
#         else:
#             rating_form = RatingForm()
#     return render(request, "Movies/rate.html", {'rating_form': rating_form})
#
#
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


class EditRating(LoginRequiredMixin, UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = "Movies/edit.html"

    def get_queryset(self):
        movie_id = self.kwargs["pk"]
        return Rating.objects.filter(movie=get_object_or_404(Movie, pk=movie_id)).filter(rater=self.request.user.rater)


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


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib

matplotlib.style.use('ggplot')


def movie_chart(request, movie_id):
    ratings = Rating.objects.filter(movie__id=movie_id)
    df = pd.DataFrame(model_to_dict(rating) for rating in ratings)
    df.index = df['timestamp']
    counts = df['rating']
    counts = counts.sort_index()
    series = pd.expanding_mean(counts).resample('M', how=np.max, fill_method='pad')
    response = HttpResponse(content_type='image/png')

    fig = plt.figure(figsize=(6, 4), facecolor="#272b30")
    plt.xticks(color="white")
    plt.yticks(color="white")
    series.plot()
    plt.title("Average Rating over Time", color="white")
    plt.xlabel("")
    canvas = FigureCanvas(fig)
    canvas.print_png(response)
    return response
