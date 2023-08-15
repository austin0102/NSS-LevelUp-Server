"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer


class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        game_type = Game.objects.get(pk=pk)
        serializer = GameSerializer(game_type)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        game = Game.objects.all()
        serializer = GameSerializer(game, many=True)
        return Response(serializer.data)
    

class GameCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ('id', 'full_name')  # Make sure you have the correct field name for the full name

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    creator = GameCreatorSerializer(many=False)
    
    class Meta:
        model = Game
        fields = ('id', 'game_title', 'creator', 'game_type', 
                'number_of_players', 'skill_level', 'events')
