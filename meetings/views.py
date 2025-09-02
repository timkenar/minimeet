from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from ics import Calendar, Event
from datetime import datetime, timedelta
import urllib.parse
from .models import Meeting
from .serializers import MeetingSerializer, MeetingCreateSerializer, MeetingUpdateSerializer, AdminMeetingCreateSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def create_meeting(request):
    serializer = MeetingCreateSerializer(data=request.data)
    if serializer.is_valid():
        meeting = serializer.save()
        
        # Generate ICS file
        ics_content = generate_ics_file(meeting)
        
        # Generate Google Calendar link
        google_calendar_link = generate_google_calendar_link(meeting)
        
        return Response({
            'id': meeting.id,
            'ics_download_url': f'/meetings/{meeting.id}/ics/',
            'google_calendar_link': google_calendar_link
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeetingListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        meetings = Meeting.objects.all().order_by('-created_at')
        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data)


class MeetingUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        try:
            meeting = Meeting.objects.get(pk=pk)
        except Meeting.DoesNotExist:
            return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check for time conflicts if assigning a datetime
        if 'assigned_datetime' in request.data:
            assigned_datetime = request.data['assigned_datetime']
            # Check if another meeting is already scheduled at this time
            conflicting_meeting = Meeting.objects.filter(
                assigned_datetime=assigned_datetime,
                status='scheduled'
            ).exclude(pk=pk).first()
            
            if conflicting_meeting:
                return Response({
                    'error': 'Time slot already occupied',
                    'conflicting_meeting': {
                        'name': conflicting_meeting.name,
                        'organization': conflicting_meeting.organization
                    }
                }, status=status.HTTP_409_CONFLICT)
        
        serializer = MeetingUpdateSerializer(meeting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            meeting = Meeting.objects.get(pk=pk)
        except Meeting.DoesNotExist:
            return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)
        
        meeting.delete()
        return Response({'message': 'Meeting deleted successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def download_ics(request, pk):
    try:
        meeting = Meeting.objects.get(pk=pk)
    except Meeting.DoesNotExist:
        return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)
    
    ics_content = generate_ics_file(meeting)
    
    response = HttpResponse(ics_content, content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename="meeting_{meeting.id}.ics"'
    return response


def generate_ics_file(meeting):
    calendar = Calendar()
    event = Event()
    event.name = f"Meeting with {meeting.name}"
    
    # Use assigned_datetime if available, otherwise preferred_datetime, otherwise current time
    meeting_datetime = meeting.assigned_datetime or meeting.preferred_datetime
    if meeting_datetime is None:
        meeting_datetime = datetime.now()
    
    event.begin = meeting_datetime
    event.end = meeting_datetime + timedelta(hours=1)
    event.description = meeting.reason
    event.location = meeting.organization
    calendar.events.add(event)
    return str(calendar)


def generate_google_calendar_link(meeting):
    # Use assigned_datetime if available, otherwise preferred_datetime, otherwise current time
    meeting_datetime = meeting.assigned_datetime or meeting.preferred_datetime
    if meeting_datetime is None:
        meeting_datetime = datetime.now()
        
    start_time = meeting_datetime.strftime('%Y%m%dT%H%M%S')
    end_time = (meeting_datetime + timedelta(hours=1)).strftime('%Y%m%dT%H%M%S')
    
    params = {
        'action': 'TEMPLATE',
        'text': f'Meeting with {meeting.name}',
        'dates': f'{start_time}/{end_time}',
        'details': meeting.reason,
        'location': meeting.organization
    }
    
    base_url = 'https://calendar.google.com/calendar/render'
    return f"{base_url}?" + urllib.parse.urlencode(params)


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_logout(request):
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_create_meeting(request):
    serializer = AdminMeetingCreateSerializer(data=request.data)
    if serializer.is_valid():
        meeting = serializer.save()
        
        # Generate ICS file
        ics_content = generate_ics_file(meeting)
        
        # Generate Google Calendar link
        google_calendar_link = generate_google_calendar_link(meeting)
        
        return Response({
            'id': meeting.id,
            'message': 'Meeting created successfully by admin',
            'ics_download_url': f'/meetings/{meeting.id}/ics/',
            'google_calendar_link': google_calendar_link,
            'meeting_details': MeetingSerializer(meeting).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
