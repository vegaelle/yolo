from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from learning.models import (
    Promotion, ObjectiveAttribution, CourseAttribution, DayAttribution,
    Formation, Objective, Tag, Member, LectureCourse, LectureFile,
    PracticeCourse, QuestionCourse, Question, Answer, Course
)
from .serializers import (
    PromotionSerializer, ObjectiveSerializer, FormationSerializer,
    TagSerializer, DayAttributionSerializer, MemberSerializer,
    CourseAttributionSerializer, ObjectiveAttributionSerializer,
    LectureCourseSerializer, LectureFileSerializer, PracticeCourseSerializer,
    QuestionCourseSerializer, QuestionSerializer, AnswerSerializer,
    CourseSerializer
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


class CourseAttributionViewSet(viewsets.ModelViewSet):
    model = CourseAttribution
    serializer_class = CourseAttributionSerializer
    queryset = CourseAttribution.objects.all()


class ObjectiveAttributionViewSet(viewsets.ModelViewSet):
    model = ObjectiveAttribution
    serializer_class = ObjectiveAttributionSerializer
    queryset = ObjectiveAttribution.objects.all()


class CourseViewSet(viewsets.ModelViewSet):
    model = Course
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LectureCourseViewSet(viewsets.ModelViewSet):
    model = LectureCourse
    serializer_class = LectureCourseSerializer
    queryset = LectureCourse.objects.all()


class PracticeCourseViewSet(viewsets.ModelViewSet):
    model = PracticeCourse
    serializer_class = PracticeCourseSerializer
    queryset = PracticeCourse.objects.all()


class QuestionCourseViewSet(viewsets.ModelViewSet):
    model = QuestionCourse
    serializer_class = QuestionCourseSerializer
    queryset = QuestionCourse.objects.all()
