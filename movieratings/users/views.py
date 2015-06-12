from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from users.forms import RaterForm, UserForm

# Create your views here.
def register_rater(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        rater_form = RaterForm(request.POST)
        if user_form.is_valid() and rater_form.is_valid():
            user = user_form.save()

            rater = rater_form.save(commit=False)
            rater.user = user
            rater.save()

            password = user.password
            user.set_password(password)
            user.save()

            user = authenticate(username=user.username,
                                password=password)

            login(request, user)

            messages.add_message(
                request,
                messages.SUCCESS,
                "Welcome, {}. You have successfully created an account and are now logged in".format(user.username))

            return redirect('top20')
    else:
        user_form = UserForm()
        rater_form = RaterForm()
    return render(request, "users/register.html", {'user_form': user_form,
                                                   'rater_form': rater_form})
