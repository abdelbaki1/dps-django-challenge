from django.urls import path
from .views import (
    PlayerListView,
    PlayerDetailView,
    TournamentListView,
    TournamentDetailView,
    TournamentAddPlayerView,
    TournamentRemovePlayerView,
    TournamentLeaderboardView,
    GameListView,
    GameDetailView,
)

urlpatterns = [
    path('players/', PlayerListView.as_view(), name='player-list'),
    path('players/<int:pk>/', PlayerDetailView.as_view(), name='player-detail'),
    
    path('tournaments/', TournamentListView.as_view(), name='tournament-list'),
    path('tournaments/<int:pk>/', TournamentDetailView.as_view(), name='tournament-detail'),
    path('tournaments/<int:pk>/add_player/', TournamentAddPlayerView.as_view(), name='tournament-add-player'),
    path('tournaments/<int:pk>/remove_player/', TournamentRemovePlayerView.as_view(), name='tournament-remove-player'),
    path('tournaments/<int:pk>/leaderboard/', TournamentLeaderboardView.as_view(), name='tournament-leaderboard'),
    
    path('games/', GameListView.as_view(), name='game-list'),
    path('games/<int:pk>/', GameDetailView.as_view(), name='game-detail'),
]
