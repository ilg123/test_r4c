import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Robot
from django.utils.dateparse import parse_datetime

@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            production_date = parse_datetime(data['created'])
            if production_date is None:
                return JsonResponse({'Ошибка': 'Не верная дата'},)
            
            try:
                robot_model = Robot.objects.get(serial = data['serial'], model=data['model'], version=data['version'])
                robot_version = Robot.objects.get(version=data['version'])
            except Robot.DoesNotExist as e:
                return JsonResponse({'Ошибка': str(e)}, status=400)

            robot = Robot(model = robot_model, version = robot_version,  created = production_date)
            robot.save()
            return JsonResponse({'Сообщение': 'Запись создана успешно'}, status=201)

        except (KeyError, ValueError, json.JSONDecodeError) as e:
            return JsonResponse({'Ошибка': str(e)}, status=400)

    else:
        return JsonResponse({'Ошибка': 'Доступен только POST-method'}, status=400)
