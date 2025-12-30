# api/urls.py

from django.urls import path
from .views import VQAPredictView, HealthCheckView

urlpatterns = [
    path('predict/', VQAPredictView.as_view(), name='vqa_predict'),  # POST: ảnh + câu hỏi
    path('health/', HealthCheckView.as_view(), name='health_check'),  # GET: kiểm tra server
]