from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import \
    Member, Tag, Formation, Objective, Course, LectureCourse,\
    LectureFile, QuestionCourse, Question, Answer, PracticeCourse, Promotion,\
    DayAttribution, CourseAttribution, ObjectiveAttribution

admin.site.unregister(User)


class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = (MemberInline, )


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     pass


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    filter_horizontal = ('objectives', 'tags')


@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    pass


class LectureFileInline(admin.TabularInline):
    model = LectureFile


@admin.register(LectureCourse)
class LectureCourseAdmin(admin.ModelAdmin):
    inlines = (LectureFileInline,)


class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(QuestionCourse)
class QuestionCourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerInline,)


@admin.register(PracticeCourse)
class PracticeCourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    pass


@admin.register(DayAttribution)
class DayAttributionAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseAttribution)
class CourseAttributionAdmin(admin.ModelAdmin):
    pass


@admin.register(ObjectiveAttribution)
class ObjectiveAttributionAdmin(admin.ModelAdmin):
    pass
