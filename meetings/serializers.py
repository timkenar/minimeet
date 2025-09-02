from rest_framework import serializers
from .models import Meeting


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = ['created_at']


class MeetingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['name', 'organization', 'reason', 'email', 'phone', 'signature']


class MeetingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['comment', 'signature', 'status', 'assigned_datetime']


class AdminMeetingCreateSerializer(serializers.Serializer):
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    name = serializers.CharField(max_length=255)
    organization = serializers.CharField(max_length=255)
    reason = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time")
        return data
    
    def create(self, validated_data):
        from datetime import datetime, time
        
        # Combine date and start_time to create assigned_datetime
        date = validated_data.pop('date')
        start_time = validated_data.pop('start_time')
        end_time = validated_data.pop('end_time')  # Remove end_time as we don't store it
        
        assigned_datetime = datetime.combine(date, start_time)
        
        meeting = Meeting.objects.create(
            assigned_datetime=assigned_datetime,
            status='scheduled',
            **validated_data
        )
        return meeting