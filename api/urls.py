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

urlpatterns = [
    url('^(?P<version>v\d+)/', include(router.urls)),
]
