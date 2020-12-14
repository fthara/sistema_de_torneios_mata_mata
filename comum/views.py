from django.shortcuts import render


# Create your views here.
def comum_view(request, *args, **kwargs):
    return render(request, "home.html", {})
