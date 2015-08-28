from django.forms import ValidationError
from rest_framework import serializers

from learning.models import (
    Promotion, ObjectiveAttribution, CourseAttribution, DayAttribution,
    Formation, Objective, Tag, Member
)


class MemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Member
        fields = ('url', 'username', 'type', 'avatar', 'tags', )


class ObjectiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Objective
        fields = ('url', 'name', 'points', 'description', )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('url', 'name', 'color', )


class FormationSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    objectives = serializers\
        .HyperlinkedRelatedField(many=True, view_name='objective-detail',
                                 queryset=Objective.objects.all())

    class Meta:
        model = Formation
        fields = ('url', 'name', 'description', 'days_count', 'objectives',
                  'tags', )


class PromotionSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()
    formation_type = serializers\
        .HyperlinkedRelatedField(view_name='formation-detail',
                                 queryset=Formation.objects.all())

    class Meta:
        model = Promotion
        fields = ('url', 'name', 'group', 'image', 'formation_type', )


class DayAttributionSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField()
    promotion = serializers\
        .HyperlinkedRelatedField(view_name='promotion-detail',
                                 queryset=Promotion.objects.all())
    assigned = serializers\
        .HyperlinkedRelatedField(view_name='member-detail',
                                 queryset=Member.objects.filter(type='teacher')
                                 )

    class Meta:
        model = DayAttribution
        fields = ('url', 'promotion', 'assigned', 'day', 'tag')
