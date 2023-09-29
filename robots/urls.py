from django.urls import path
from .views import get_robot, get_all_robots, download_excel


urlpatterns = [
    path('api/get_robot/<int:robot_id>/', get_robot),
    path('api/get_all_robots/', get_all_robots),
    path('download_excel/', download_excel),
]
