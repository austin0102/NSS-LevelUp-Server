from django.db import models

class Game(models.Model):
    game_title = models.CharField(max_length=55)
    creator = models.CharField(max_length=55)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name="created_games")
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name="games")
    number_of_players = models.IntegerField(2)
    skill_level = models.CharField(max_length=20)