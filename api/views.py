from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from task.models import Task
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'status': 'success', 'message': 'Successfully logged out.'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)

