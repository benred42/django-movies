from django import forms
from Movies.models import Rating, Movie
from datetime import datetime


class RatingForm(forms.ModelForm):
    movie = forms.ModelChoiceField(Movie.objects.order_by("title"), to_field_name="title")
    rating = forms.ChoiceField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))
    review = forms.CharField(widget=forms.Textarea, required=False)
    timestamp = forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.now())

    class Meta:
        model = Rating
        fields = ("movie", "rating", "review", "timestamp")
