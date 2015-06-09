from django.db import models

# Create your models here.
class Rater(models.Model):
    gender = models.CharField(max_length=1)
    age = models.IntegerField()
    occupation = models.IntegerField()
    zipcode = models.CharField(max_length=300)

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

    def get_average_rating(self):
        ratings = self.rating_set.all()
        all_ratings = [rating.rating for rating in ratings]
        if all_ratings:
            return sum(all_ratings) / len(all_ratings)
        else:
            return "No ratings"

    def top_unseen(self):
        rated = [rating.movie.title for rating in self.rating_set.all()]
        top_unrated = [movie for movie in Movie.top_movies() if movie[0] not in rated]
        return top_unrated[:10]

    def __str__(self):
        return str(self.id)

class Movie(models.Model):
    title = models.CharField(max_length=300)
    genre = models.CharField(max_length=300)
    movies = models.Manager()

    def get_ratings(self):
        return self.rating_set.count()

    @property
    def get_average_rating(self):
        ratings = self.rating_set.all()
        all_ratings = [rating.rating for rating in ratings]
        if all_ratings:
            return sum(all_ratings) / len(all_ratings)
        else:
            return "Not rated"

    @classmethod
    def top_movies(cls):
        all_movies = Movie.movies.all()
        top_movies = sorted([(movie.title, movie.get_average_rating) for movie in all_movies], key=lambda x: x[1],
                            reverse=True)
        return top_movies

    def __str__(self):
        return self.title


class Rating(models.Model):
    rater = models.ForeignKey(Rater)
    movie = models.ForeignKey(Movie)
    rating = models.IntegerField()
    timestamp = models.IntegerField()

    def __str__(self):
        return "User: {}, Movie:{}, Rating:{}".format(self.rater, self.movie, self.rating)

