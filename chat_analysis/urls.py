from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet)
router.register(r'reports', views.AnalysisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]