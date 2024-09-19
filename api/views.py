from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from task.models import Task
import json

@csrf_exempt
def save_notes(request, task_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        notes = data.get('notes', '')
        try:
            task = Task.objects.get(id=task_id)
            task.notes = notes
            task.save()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
