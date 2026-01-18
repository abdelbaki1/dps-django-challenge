from rest_framework import serializers
from .models import Player, Tournament, Game


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class GameSerializer(serializers.ModelSerializer):
    player1_name = serializers.CharField(source='player1.name', read_only=True)
    player2_name = serializers.CharField(source='player2.name', read_only=True)
    winner_name = serializers.CharField(source='winner.name', read_only=True, allow_null=True)

    class Meta:
        model = Game
        fields = ['id', 'tournament', 'player1', 'player2', 'player1_name', 'player2_name', 
                  'winner', 'winner_name', 'is_draw', 'played_at']
        read_only_fields = ['id', 'played_at']

    def validate(self, data):
        if data.get('player1') == data.get('player2'):
            raise serializers.ValidationError('A player cannot play against themselves.')
        
        tournament = data.get('tournament')
        player1 = data.get('player1')
        player2 = data.get('player2')
        
        if tournament and player1 and not tournament.players.filter(id=player1.id).exists():
            raise serializers.ValidationError(f'{player1.name} is not part of this tournament.')
        
        if tournament and player2 and not tournament.players.filter(id=player2.id).exists():
            raise serializers.ValidationError(f'{player2.name} is not part of this tournament.')
        
        winner = data.get('winner')
        is_draw = data.get('is_draw', False)
        
        if winner and is_draw:
            raise serializers.ValidationError('A game cannot have both a winner and be a draw.')
        
        if winner and winner not in [player1, player2]:
            raise serializers.ValidationError('Winner must be one of the players in the game.')
        
        if tournament and player1 and player2:
            existing_game_1 = Game.objects.filter(
                tournament=tournament,
                player1=player1,
                player2=player2
            )
            
            existing_game_2 = Game.objects.filter(
                tournament=tournament,
                player1=player2,
                player2=player1
            )
            
            if self.instance:
                existing_game_1 = existing_game_1.exclude(id=self.instance.id)
                existing_game_2 = existing_game_2.exclude(id=self.instance.id)
            
            if existing_game_1.exists() or existing_game_2.exists():
                raise serializers.ValidationError(
                    'These players have already played against each other in this tournament.'
                )
        
        return data


class TournamentSerializer(serializers.ModelSerializer):
    players_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tournament
        fields = ['id', 'name', 'status', 'players', 'players_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def get_players_count(self, obj):
        return obj.players.count()

    def validate_players(self, value):
        if len(value) > 5:
            raise serializers.ValidationError('A tournament can have a maximum of 5 participants.')
        return value


class AddPlayerToTournamentSerializer(serializers.Serializer):
    player_id = serializers.IntegerField()

    def validate_player_id(self, value):
        if not Player.objects.filter(id=value).exists():
            raise serializers.ValidationError('Player does not exist.')
        return value


class LeaderboardEntrySerializer(serializers.Serializer):
    player_id = serializers.IntegerField()
    player_name = serializers.CharField()
    points = serializers.IntegerField()
    wins = serializers.IntegerField()
    draws = serializers.IntegerField()
    losses = serializers.IntegerField()
    games_played = serializers.IntegerField()


class TournamentLeaderboardSerializer(serializers.Serializer):
    tournament_id = serializers.IntegerField()
    tournament_name = serializers.CharField()
    status = serializers.CharField()
    total_players = serializers.IntegerField()
    total_games_played = serializers.IntegerField()
    total_expected_games = serializers.IntegerField()
    leaderboard = LeaderboardEntrySerializer(many=True)
