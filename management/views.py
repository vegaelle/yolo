from django.shortcuts import render, get_object_or_404
from learning.decorators import manager
from learning.models import Promotion


@manager
def home(request):
    promotions = Promotion.objects.all()
    return render(request, 'management/home.html', {'promotions': promotions})


@manager
def planning(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    return render(request, 'management/planning.html',
                  {'promotion': promotion})
