from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, Count

# Create your models here.
class Rater(models.Model):
    gender = models.CharField(max_length=1)
    age = models.IntegerField()
    occupation = models.IntegerField()
    zipcode = models.CharField(max_length=10)
    user = models.OneToOneField(User, null=True)

    @property
    def occupation_label(self):
        occupations_dict = {0:  "other or not specified",
                            1:  "academic/educator",
                            2:  "artist",
                            3:  "clerical/admin",
                            4:  "college/grad student",
                            5:  "customer service",
                            6:  "doctor/health care",
                            7:  "executive/managerial",
                            8:  "farmer",
                            9:  "homemaker",
                            10:  "K-12 student",
                            11:  "lawyer",
                            12:  "programmer",
                            13:  "retired",
                            14:  "sales/marketing",
                            15:  "scientist",
                            16:  "self-employed",
                            17:  "technician/engineer",
                            18:  "tradesman/craftsman",
                            19:  "unemployed",
                            20:  "writer"}
        return occupations_dict[self.occupation]

    def get_ratings(self):
        return self.rating_set.count()

    @property
    def get_average_rating(self):
        avg_rating = self.rating_set.all().aggregate(Avg('rating'))['rating__avg']
        if avg_rating is not None:
            return round(avg_rating, 2)
        else:
            return 0.0

    def top_unseen(self):
        rated = [rating.movie for rating in self.rating_set.all()]
        top_unrated = [movie for movie in Movie.top_movies() if movie not in rated]
        return top_unrated[:20]

    def __str__(self):
        return str(self.id)


#######################################################################################################################


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


#######################################################################################################################


class Movie(models.Model):
    title = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre)

    def get_ratings(self):
        return self.rating_set.count()

    @property
    def get_genres(self):
        all_genres = [genre.name for genre in self.genres.all()]
        return all_genres

    @property
    def get_average_rating(self):
        avg_rating = self.rating_set.all().aggregate(Avg('rating'))['rating__avg']
        if avg_rating is not None:
            return round(avg_rating, 2)
        else:
            return 0.0

    @classmethod
    def top_movies(cls):
        all_movies = Movie.objects.all()
        top_movies = sorted([movie for movie in all_movies if movie.get_ratings() > 9],
                            key=lambda x: x.get_average_rating,
                            reverse=True)
        # top_movies = Movie.objects.annotate(
        #     rating_count=Count("Rating"),
        #     average_rating=Avg("Rating__rating")
        # )
        return top_movies

    def __str__(self):
        return self.title


#######################################################################################################################


class Rating(models.Model):
    rater = models.ForeignKey(Rater)
    movie = models.ForeignKey(Movie)
    rating = models.IntegerField()

    def __str__(self):
        return "User: {}, Movie:{}, Rating:{}".format(self.rater, self.movie, self.rating)


#######################################################################################################################


def make_users():
    """Creates user objects for existing raters (development only, do not run)"""
    for rater in Rater.objects.all():
        user = User.objects.create_user(username="user{}".format(rater.id),
                                        email="user{}@example.ro".format(rater.id),
                                        password="batman")
        rater.user = user
        rater.save()
