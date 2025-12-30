# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import time

from .serializers import VQARequestSerializer
from .model_loader import model_inference


class VQAPredictView(APIView):
    """POST: ảnh + câu hỏi -> câu trả lời"""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        # Validate input
        serializer = VQARequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        temp_path = None
        try:
            image_file = serializer.validated_data['image']
            question = serializer.validated_data['question']
            
            # Lưu ảnh tạm và predict
            temp_path = self._save_temp_image(image_file)
            answer, processing_time = self._predict(temp_path, question)
            
            # Response
            return Response({
                'question': question,
                'answer': answer,
                'processing_time': round(processing_time, 3)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            # Cleanup file tạm
            self._cleanup(temp_path)
    
    def _save_temp_image(self, image_file):
        """Lưu ảnh vào thư mục temp"""
        temp_path = default_storage.save(
            f'temp/{image_file.name}',
            ContentFile(image_file.read())
        )
        return os.path.join(default_storage.location, temp_path)
    
    def _predict(self, image_path, question):
        """Chạy model prediction"""
        start_time = time.time()
        answer = model_inference.predict(image_path, question)
        processing_time = time.time() - start_time
        return answer, processing_time
    
    def _cleanup(self, temp_path):
        """Xóa file tạm"""
        if temp_path:
            try:
                # Lấy relative path để delete
                relative_path = temp_path.replace(default_storage.location + os.sep, '')
                default_storage.delete(relative_path)
            except Exception:
                pass


class HealthCheckView(APIView):
    """GET: kiểm tra trạng thái model"""
    
    def get(self, request):
        is_loaded = model_inference.model is not None
        return Response({
            'status': 'ok' if is_loaded else 'not_ready',
            'model_loaded': is_loaded,
            'device': str(model_inference.device) if is_loaded else None
        })