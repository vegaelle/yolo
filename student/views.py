from django.shortcuts import render
from learning.decorators import student


@student
def home(request):
    promotion = request.user.groups.filter(promotion__isnull=False)\
        .first().promotion
    return render(request, 'student/home.html', {'promotion': promotion})


def example(request):
    return render(request, 'student/example.html', {})
