from django.db import models

# Create your models here.
class Rater(models.Model):
    raterID = models.IntegerField()
    gender = models.CharField(max_length=300)
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

    def __str__(self):
        return self.raterID

class Movie(models.Model):
    movieID = models.IntegerField()
    title = models.CharField(max_length=300)
    genre = models.CharField(max_length=300)

    def get_ratings(self):
        return self.rating_set.count()

    def __str__(self):
        return self.movieID


class Rating(models.Model):
    raterID = models.ForeignKey(Rater)
    movieID = models.ForeignKey(Movie)
    rating = models.IntegerField()
    timestamp = models.IntegerField()

    def __str__(self):
        return "User: {}, Movie:{}, Rating:{}".format(self.raterID, self.movieID, self.rating)

