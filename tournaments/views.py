from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Player, Tournament, Game
from .serializers import (
    PlayerSerializer, 
    TournamentSerializer, 
    GameSerializer,
    AddPlayerToTournamentSerializer,
    TournamentLeaderboardSerializer,
    LeaderboardEntrySerializer
)


class PlayerListView(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class TournamentListView(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer


class TournamentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer


class TournamentAddPlayerView(APIView):
    def post(self, request, pk):
        tournament = get_object_or_404(Tournament, pk=pk)
        serializer = AddPlayerToTournamentSerializer(data=request.data)
        
        if serializer.is_valid():
            player_id = serializer.validated_data['player_id']
            
            if tournament.players.count() >= 5:
                return Response(
                    {'error': 'Tournament already has the maximum of 5 participants.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            player = Player.objects.get(id=player_id)
            
            if tournament.players.filter(id=player_id).exists():
                return Response(
                    {'error': 'Player is already part of this tournament.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            tournament.players.add(player)
            tournament.update_status()
            
            return Response(
                {'message': f'Player {player.name} added to tournament {tournament.name}.'},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentRemovePlayerView(APIView):
    def delete(self, request, pk):
        tournament = get_object_or_404(Tournament, pk=pk)
        player_id = request.data.get('player_id')
        
        if not player_id:
            return Response(
                {'error': 'player_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return Response(
                {'error': 'Player does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not tournament.players.filter(id=player_id).exists():
            return Response(
                {'error': 'Player is not part of this tournament.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        has_games_as_player1 = Game.objects.filter(tournament=tournament, player1=player).exists()
        has_games_as_player2 = Game.objects.filter(tournament=tournament, player2=player).exists()
        
        if has_games_as_player1 or has_games_as_player2:
            return Response(
                {'error': 'Cannot remove player who has already played games in this tournament.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tournament.players.remove(player)
        tournament.update_status()
        
        return Response(
            {'message': f'Player {player.name} removed from tournament {tournament.name}.'},
            status=status.HTTP_200_OK
        )


class TournamentLeaderboardView(APIView):
    def get(self, request, pk):
        tournament = get_object_or_404(Tournament, pk=pk)
        
        leaderboard_data = []
        
        for player in tournament.players.all():
            wins = Game.objects.filter(
                tournament=tournament,
                winner=player
            ).count()
            
            draws_as_player1 = Game.objects.filter(
                tournament=tournament,
                is_draw=True,
                player1=player
            ).count()
            
            draws_as_player2 = Game.objects.filter(
                tournament=tournament,
                is_draw=True,
                player2=player
            ).count()
            
            draws = draws_as_player1 + draws_as_player2
            
            games_as_player1 = Game.objects.filter(
                tournament=tournament,
                player1=player
            ).exclude(winner__isnull=True, is_draw=False).count()
            
            games_as_player2 = Game.objects.filter(
                tournament=tournament,
                player2=player
            ).exclude(winner__isnull=True, is_draw=False).count()
            
            games_played = games_as_player1 + games_as_player2
            
            losses = games_played - wins - draws
            
            points = (wins * 2) + (draws * 1)
            
            leaderboard_data.append({
                'player_id': player.id,
                'player_name': player.name,
                'points': points,
                'wins': wins,
                'draws': draws,
                'losses': losses,
                'games_played': games_played
            })
        
        leaderboard_data.sort(key=lambda x: x['points'], reverse=True)
        
        response_data = {
            'tournament_id': tournament.id,
            'tournament_name': tournament.name,
            'status': tournament.status,
            'total_players': tournament.players.count(),
            'total_games_played': tournament.get_played_games_count(),
            'total_expected_games': tournament.get_total_expected_games(),
            'leaderboard': leaderboard_data
        }
        
        serializer = TournamentLeaderboardSerializer(response_data)
        return Response(serializer.data)


class GameListView(generics.ListCreateAPIView):
    serializer_class = GameSerializer
    
    def get_queryset(self):
        queryset = Game.objects.all()
        tournament_id = self.request.query_params.get('tournament', None)
        
        if tournament_id is not None:
            queryset = queryset.filter(tournament_id=tournament_id)
        
        return queryset


class GameDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
