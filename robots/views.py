from django.shortcuts import render
from .models import Robot
from django.http import JsonResponse, HttpResponse
import json
from datetime import datetime
from pydantic import BaseModel
from openpyxl import Workbook
from collections import defaultdict


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
            'created': robot.created,
            'quantity': robot.quantity
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


# качаем Exel
def download_excel(request):
    # получаем данные из базы данных и сгруппировываем их по модели и версии
    robots = Robot.objects.all()
    data = defaultdict(list)

    for robot in robots:
        data[robot.model, robot.version].append(robot)

    # создаем новый файл Excel
    wb = Workbook()

    # создаем листы в файле Excel, по одному на каждую модель
    for model, version in data:
        ws = wb.create_sheet(f'{model} {version}')
        ws.append(['Модель', 'Версия', 'Количество за неделю'])
        for robot in data[model, version]:
            ws.append([robot.model, robot.version, robot.quantity])

    # сохраняем файл Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=my_excel_file.xlsx'
    wb.save(response)

    return response
