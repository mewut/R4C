from django.shortcuts import render
from .models import Robot
from django.http import JsonResponse
import json
from datetime import datetime
from pydantic import BaseModel


# валидация с pydantic
class RobotModel(BaseModel):
    model: str
    version: str
    created: datetime

    
# получаем весь список роботов. 
# название get_all_robots не так сильно похоже на get_robot, поэтому я решила назвать так
def get_all_robots(request):
    robots = Robot.objects.all()
    robots_list = []
    for robot in robots:
        data = {
            'id': robot.id,
            'serial': robot.serial,
            'model': robot.model,
            'version': robot.version,
            'created': robot.created
        }
        robot = RobotModel(**data)
        robots_list.append(robot.dict())
    return JsonResponse({'robots': robots_list})


# получаем одного конкретного робота по его id
def get_robot(request, robot_id):
    try:
        robot = Robot.objects.get(id=robot_id)
        data = {
            'serial': robot.serial,
            'model': robot.model,
            'version': robot.version,
            'created': robot.created
        }
        robot = RobotModel(**data)
        return JsonResponse(robot.dict())
    except Robot.DoesNotExist:
        return JsonResponse({'error': 'Robot not found'})
