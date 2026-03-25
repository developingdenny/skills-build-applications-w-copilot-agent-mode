"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TeamViewSet, ActivityViewSet, WorkoutViewSet, LeaderboardViewSet, api_root
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Custom API root to return URLs with $CODESPACE_NAME if set
CODESPACE_NAME = os.environ.get('CODESPACE_NAME')
def get_api_base(request):
    host = request.get_host()
    if CODESPACE_NAME:
        host = f"{CODESPACE_NAME}-8000.app.github.dev"
    scheme = 'https' if host.endswith('.app.github.dev') else 'http'
    return f"{scheme}://{host}/api/"

@api_view(['GET'])
def custom_api_root(request, format=None):
    api_base = get_api_base(request)
    return Response({
        'users': api_base + 'users/',
        'teams': api_base + 'teams/',
        'activities': api_base + 'activities/',
        'workouts': api_base + 'workouts/',
        'leaderboard': api_base + 'leaderboard/',
    })


# Router must be defined before urlpatterns
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'workouts', WorkoutViewSet, basename='workout')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', custom_api_root, name='api-root'),
    path('', custom_api_root),
]
