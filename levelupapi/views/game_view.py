"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


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
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game_type = GameType.objects.get(pk=request.data["game_type"])

        game = Game.objects.create(
            game_title=request.data["game_title"],
            creator=request.data["creator"],
            gamer=gamer,
            game_type=game_type,
            number_of_players=request.data["number_of_players"],
            skill_level=request.data["skill_level"]
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.game_title = request.data["game_title"]
        game.creator = request.data["creator"]
        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]

        gamer = Gamer.objects.get(user=request.auth.user)
        game.gamer = gamer
        game_type = GameType.objects.get(pk=request.data["game_type"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
            

        

class GameCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ('id', 'full_name')  # Make sure you have the correct field name for the full name

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    gamer = GameCreatorSerializer(many=False)
    
    class Meta:
        model = Game
        fields = ('id', 'game_title', 'creator', 'gamer', 'game_type', 
                'number_of_players', 'skill_level', 'events')
