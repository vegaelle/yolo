from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('members', views.MemberViewSet, base_name='member')
router.register('tags', views.TagViewSet, base_name='tag')
router.register('objectives', views.ObjectiveViewSet, base_name='objective')
router.register('formations', views.FormationViewSet, base_name='formation')
router.register('promotions', views.PromotionViewSet, base_name='promotion')
router.register('dayattributions', views.DayAttributionViewset,
                base_name='dayattribution')
router.register('courseattributions', views.CourseAttributionViewSet,
                base_name='courseattribution')
router.register('objectiveattributions', views.ObjectiveAttributionViewSet,
                base_name='objectiveattribution')
router.register('courses', views.CourseViewSet,
                base_name='course')
router.register('lecturecourses', views.LectureCourseViewSet,
                base_name='lecturecourse')
router.register('practicecourses', views.PracticeCourseViewSet,
                base_name='practicecourse')


urlpatterns = [
    url('^(?P<version>v\d+)/', include(router.urls)),
]
