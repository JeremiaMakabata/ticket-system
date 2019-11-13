from .views import UserViewSet, UserProfileViewSet, TicketViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

app_name = 'tickets'
router = DefaultRouter()
router.register('tickets/profile/', UserProfileViewSet)
router.register('users/', UserViewSet)
router.register('ticket/', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
