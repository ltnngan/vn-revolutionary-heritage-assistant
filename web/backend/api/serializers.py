# api/serializers.py

from rest_framework import serializers


class VQARequestSerializer(serializers.Serializer):
    """Validate request: ảnh + câu hỏi"""
    image = serializers.ImageField(required=True)
    question = serializers.CharField(required=True, max_length=500)
    
    def validate_question(self, value):
        """Câu hỏi phải >= 3 ký tự"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Câu hỏi quá ngắn")
        return value


class VQAResponseSerializer(serializers.Serializer):
    """Format response: câu hỏi + câu trả lời + metadata"""
    question = serializers.CharField()
    answer = serializers.CharField()
    confidence = serializers.FloatField(required=False)
    processing_time = serializers.FloatField(required=False)