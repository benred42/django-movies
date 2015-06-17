from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, Count

# Create your models here.

OCCUPATIONS = (
    (0, "Other or not specified"),
    (1, "Academic/educator"),
    (2, "Artist"),
    (3, "Clerical/admin"),
    (4, "College/grad student"),
    (5, "Customer service"),
    (6, "Doctor/health care"),
    (7, "Executive/managerial"),
    (8, "Farmer"),
    (9, "Homemaker"),
    (10, "K-12 student"),
    (11, "Lawyer"),
    (12, "Programmer"),
    (13, "Retired"),
    (14, "Sales/marketing"),
    (15, "Scientist"),
    (16, "Self-employed"),
    (17, "Technician/engineer"),
    (18, "Tradesman/craftsman"),
    (19, "Unemployed"),
    (20, "Writer")

)


class Rater(models.Model):
    gender = models.CharField(max_length=1, choices=(("M", "Male"), ("F", "Female")))
    age = models.IntegerField(choices=((1, "Under 18"), (18, "18-24"), (25, "25-34"), (35, "35-44"),
                                       (45, "45-49"), (50, "50-55"), (56, "56+")))
    occupation = models.IntegerField(choices=OCCUPATIONS)
    zipcode = models.CharField(max_length=10)
    user = models.OneToOneField(User, null=True)

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
        top_unrated = Movie.objects.exclude(rating__in=self.rating_set.all()).annotate(avg_rating=Avg("rating__rating"),
            num=Count("rating")).filter(
            num__gt=9).order_by("-avg_rating")
        # rated = [rating.movie for rating in self.rating_set.all()]
        # top_unrated = [movie for movie in Movie.top_movies() if movie not in rated]
        return top_unrated

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

    @property
    def get_genres(self):
        all_genres = [genre.name for genre in self.genres.all()]
        return all_genres

    @classmethod
    def top_movies(cls):
        top_movies = Movie.objects.annotate(avg_rating=Avg("rating__rating"), num=Count("rating")).filter(num__gt=9)
        return top_movies.order_by("-avg_rating")

    def __str__(self):
        return self.title


#######################################################################################################################
def validate_rating_in_range(value):
    if not 1 <= int(value) <= 5:
        raise ValidationError("Rating must be between 1 and 5")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

class Rating(models.Model):
    rater = models.ForeignKey(Rater)
    movie = models.ForeignKey(Movie)
    rating = models.IntegerField(validators=[validate_rating_in_range])
    timestamp = models.DateTimeField(null=True)
    review = models.TextField(null=True, blank=True)

    def __str__(self):
        return "User: {}, Movie:{}, Rating:{}".format(self.rater, self.movie, self.rating)

    class Meta:
        unique_together = (
            ("rater", "movie")
        )


#######################################################################################################################


def make_users():
    """Creates user objects for existing raters (development only, do not run)"""
    for rater in Rater.objects.all():
        user = User.objects.create_user(username="user{}".format(rater.id),
                                        email="user{}@example.ro".format(rater.id),
                                        password="batman")
        rater.user = user
        rater.save()
