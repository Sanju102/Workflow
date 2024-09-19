from django.urls import path
from .views import save_notes

urlpatterns = [
    # ... existing url patterns ...
    path('save-notes/<int:task_id>/', save_notes, name='save-notes'),
]