from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ToolViewSet, CategoryViewSet, TypeViewSet, HashtagViewSet, subscribe_user

router = DefaultRouter()
router.register(r'tools', ToolViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'types', TypeViewSet)
router.register(r'hashtags', HashtagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('subscribe/', subscribe_user, name='subscribe_user'),
]  
