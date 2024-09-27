from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from task.models import Task
from .serializers import TaskSerializer
from django.utils import timezone
from django.db.models import Q
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_summary(request):
    user = request.user
    tasks = Task.objects.filter(creator=user)
    open_task=tasks.filter(Q(status="To do") | Q(status="Ongoing")).count()
    delayed_task=tasks.filter(Q(status="To do") | Q(status="Ongoing"))
    now = timezone.now()
    delayed_task=delayed_task.filter(Q(exp_end_date__lt=now)).count()
    data={"task_summary":{"open_task":open_task,"delayed_task":delayed_task}}
    return Response({'tasks': data})
