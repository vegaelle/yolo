from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from learning.models import (
    Promotion, ObjectiveAttribution, CourseAttribution, DayAttribution,
    Formation, Objective, Tag, Member
)
from .serializers import (
    PromotionSerializer, ObjectiveSerializer, FormationSerializer,
    TagSerializer, DayAttributionSerializer, MemberSerializer
)
from . import permissions


class MemberViewSet(viewsets.ModelViewSet):
    model = Member
    serializer_class = MemberSerializer
    queryset = Member.objects.all()


class TagViewSet(viewsets.ModelViewSet):
    model = Tag
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class ObjectiveViewSet(viewsets.ModelViewSet):
    model = Objective
    serializer_class = ObjectiveSerializer
    queryset = Objective.objects.all()


class FormationViewSet(viewsets.ModelViewSet):
    model = Formation
    serializer_class = FormationSerializer
    queryset = Formation.objects.all()


class PromotionViewSet(viewsets.ModelViewSet):
    model = Promotion
    serializer_class = PromotionSerializer
    queryset = Promotion.objects.all()


class DayAttributionViewset(viewsets.ModelViewSet):
    model = DayAttribution
    serializer_class = DayAttributionSerializer
    queryset = DayAttribution.objects.all()
