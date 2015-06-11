import csv
import json

print("Converting users...")
users = []
with open("data/ml-1m/users.dat") as infile:
    reader = csv.reader((line.replace("::", ";") for line in infile),
                        delimiter=";")
    for row in reader:
        users.append({"model": "Movies.Rater",
                      "pk": row[0],
                      "fields": {
                          "gender": row[1],
                          "age": row[2],
                          "occupation": row[3],
                          "zipcode": row[4]
                      }})

with open("movieratings/fixtures/users.json", "w") as outfile:
    outfile.write(json.dumps(users))


print("Converting genres...")
unique_genres = set()
genres = []
genre_dict = {}
with open("data/ml-1m/movies.dat", encoding="windows-1252") as infile:
    reader = csv.reader((line.replace("::", "_") for line in infile),
                        delimiter="_")
    for row in reader:
        unique_genres.update(row[2].split("|"))
    for idx, genre in enumerate(sorted(unique_genres)):
        genre_dict[genre] = idx
    for genre, idx in genre_dict.items():
        genres.append({"model": "Movies.Genre",
                       "pk": idx + 1,
                       "fields": {
                           "name": genre
                       }})

with open("movieratings/fixtures/genres.json", "w") as outfile:
    outfile.write(json.dumps(genres))


print("Converting movies...")
movies = []
with open("data/ml-1m/movies.dat", encoding="windows-1252") as infile:
    reader = csv.reader((line.replace("::", "_") for line in infile),
                        delimiter="_")
    for row in reader:
        movies.append({"model": "Movies.Movie",
                       "pk": row[0],
                       "fields": {
                           "title": row[1],
                           "genres": [genre_dict[genre]-1 for genre in row[2].split("|")]
                       }})

with open("movieratings/fixtures/movies.json", "w") as outfile:
    outfile.write(json.dumps(movies))


print("Converting ratings...")
ratings = []
with open("data/ml-1m/ratings.dat") as infile:
    reader = csv.reader((line.replace("::", ";") for line in infile),
                        delimiter=";")
    for idx, row in enumerate(reader):
        ratings.append({"model": "Movies.Rating",
                        "pk": idx + 1,
                        "fields": {
                            "rater": row[0],
                            "movie": row[1],
                            "rating": row[2]
                        }})

with open("movieratings/fixtures/ratings.json", "w") as outfile:
    outfile.write(json.dumps(ratings))
