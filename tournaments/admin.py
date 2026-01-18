from django.contrib import admin
from .models import Player, Tournament, Game


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name']
    filter_horizontal = ['players']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'tournament', 'player1', 'player2', 'winner', 'is_draw', 'played_at']
    list_filter = ['tournament', 'is_draw', 'played_at']
    search_fields = ['tournament__name', 'player1__name', 'player2__name']
