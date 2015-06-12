from django import forms
from Movies.models import Rating, Movie


class RatingForm(forms.ModelForm):
    movie = forms.ModelChoiceField(Movie.objects.all(), to_field_name="title")
    rating = forms.ChoiceField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))

    class Meta:
        model = Rating
        fields = ("movie", "rating",)
