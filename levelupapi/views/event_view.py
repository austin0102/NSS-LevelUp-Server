"""View module for handling requests about event"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game


class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all event

        Returns:
            Response -- JSON serialized list of event
        """
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)


class EventOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ('id', 'full_name')

class EventGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'game_title', 'creator', 'game_type',
                'number_of_players', 'skill_level')

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for event
    """
    organizer = EventOrganizerSerializer(many=False)
    game = EventGameSerializer(many=False)
    class Meta:
        model = Event
        fields = ('id', 'event_title', 'date_time', 'organizer',
                'game', 'location',)
