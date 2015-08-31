from rest_framework import serializers

from learning.models import (
    Promotion, ObjectiveAttribution, CourseAttribution, DayAttribution,
    Formation, Objective, Tag, Member, Course, LectureCourse, LectureFile,
    PracticeCourse, QuestionCourse, Question, Answer
)


class PolymorphicHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):

    def use_pk_only_optimization(self):
        return False

    def get_url(self, obj, view_name, request, format):
        view_name = view_name[obj.__class__.__name__]
        return super().get_url(obj, view_name, request, format)


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


class CourseRelatedField(serializers.HyperlinkedRelatedField):

    def to_internal_value(self, obj):
        import ipdb
        ipdb.set_trace()
        if isinstance(obj, LectureCourse):
            return LectureCourseSerializer(obj, context=self.context)\
                .to_internal_value(obj)
        elif isinstance(obj, PracticeCourse):
            return PracticeCourseSerializer(obj, context=self.context)\
                .to_internal_value(obj)
        elif isinstance(obj, QuestionCourse):
            return QuestionCourseSerializer(obj, context=self.context)\
                .to_internal_value(obj)
        return super().to_internal_value(obj)

    def to_representation(self, obj):
        import ipdb
        ipdb.set_trace()
        if isinstance(obj, LectureCourse):
            return LectureCourseSerializer(obj, context=self.context)\
                .to_representation(obj)
        elif isinstance(obj, PracticeCourse):
            return PracticeCourseSerializer(obj, context=self.context)\
                .to_representation(obj)
        elif isinstance(obj, QuestionCourse):
            return QuestionCourseSerializer(obj, context=self.context)\
                .to_representation(obj)
        return super().to_representation(obj)


class CourseAttributionSerializer(serializers.ModelSerializer):
    course = PolymorphicHyperlinkedRelatedField(
        view_name={'LectureCourse': 'lecturecourse-detail',
                   'PracticeCourse': 'practicecourse-detail',
                   'QuestionCourse': 'questioncourse-detail',
                   },
        queryset=Course.objects.all())

    class Meta:
        model = CourseAttribution
        fields = ('url', 'promotion', 'course', 'begin', 'end', )


class ObjectiveAttributionSerializer(serializers.ModelSerializer):
    objective = serializers.HyperlinkedRelatedField(
        view_name='objective-detail',
        queryset=Objective.objects.all())

    class Meta:
        model = ObjectiveAttribution
        fields = ('url', 'promotion', 'objective', 'day', )


class CourseSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField()
    objectives = ObjectiveSerializer(many=True)

    class Meta:
        model = Course
        fields = ('url',  'name', 'description', 'standard_duration',
                  'objectives', 'tag', )

    def to_internal_value(self, obj):
        if isinstance(obj, LectureCourse):
            return LectureCourseSerializer(obj, context=self.context)\
                .to_internal_value(obj)
        elif isinstance(obj, PracticeCourse):
            return PracticeCourseSerializer(obj, context=self.context)\
                .to_internal_value(obj)
        elif isinstance(obj, QuestionCourse):
            return QuestionCourseSerializer(obj, context=self.context)\
                .to_internal_value(obj)
        return super().to_internal_value(obj)

    def to_representation(self, obj):
        if isinstance(obj, LectureCourse):
            return LectureCourseSerializer(obj, context=self.context)\
                .to_representation(obj)
        elif isinstance(obj, PracticeCourse):
            return PracticeCourseSerializer(obj, context=self.context)\
                .to_representation(obj)
        elif isinstance(obj, QuestionCourse):
            return QuestionCourseSerializer(obj, context=self.context)\
                .to_representation(obj)
        return super().to_representation(obj)


class LectureFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = LectureFile
        fields = ('file', 'type', )


class LectureCourseSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField()
    objectives = ObjectiveSerializer(many=True)
    files = LectureFileSerializer(many=True)

    class Meta:
        model = LectureCourse
        fields = ('url',  'name', 'description', 'standard_duration',
                  'objectives', 'tag', 'content', 'files', 'course_type', )


class PracticeCourseSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField()
    objectives = ObjectiveSerializer(many=True)

    class Meta:
        model = PracticeCourse
        fields = ('url', 'name', 'description', 'standard_duration',
                  'objectives', 'tag', 'instructions', 'repository',
                  'course_type', )


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.HyperlinkedRelatedField(
        view_name='question-detail',
        queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = ('url', 'question', 'label', 'order', 'valid', )


class QuestionSerializer(serializers.ModelSerializer):
    course = serializers.HyperlinkedRelatedField(
        view_name='questioncourse-detail',
        queryset=Course.objects.all())
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('url', 'course', 'label', 'order', 'question_type',
                  'answers', )


class QuestionCourseSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField()
    objectives = ObjectiveSerializer(many=True)
    questions = QuestionSerializer(many=True)

    class Meta:
        model = QuestionCourse
        fields = ('url', 'name', 'description', 'standard_duration',
                  'objectives', 'tag', 'questions', 'course_type', )
