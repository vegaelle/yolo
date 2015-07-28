from django.shortcuts import render
from learning.decorators import student


@student
def home(request):
    promotion = request.user.groups.first().promotion
    return render(request, 'student/home.html', {'promotion': promotion})
