from django.db import models
from django.core.exceptions import ValidationError


class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Tournament(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('started', 'Started'),
        ('finished', 'Finished'),
    ]

    name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    players = models.ManyToManyField(Player, related_name='tournaments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.players.count() > 5:
            raise ValidationError('A tournament can have a maximum of 5 participants.')

    def get_total_expected_games(self):
        n = self.players.count()
        return (n * (n - 1)) // 2

    def get_played_games_count(self):
        return self.games.filter(winner__isnull=False).count() + self.games.filter(is_draw=True).count()

    def update_status(self):
        players_count = self.players.count()
        
        if players_count < 2:
            self.status = 'planning'
        else:
            played_games = self.get_played_games_count()
            total_expected_games = self.get_total_expected_games()
            
            if played_games == 0:
                self.status = 'planning'
            elif played_games >= total_expected_games:
                self.status = 'finished'
            else:
                self.status = 'started'
        
        self.save()

    class Meta:
        ordering = ['-created_at']


class Game(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='games')
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='games_as_player1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='games_as_player2')
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='won_games', null=True, blank=True)
    is_draw = models.BooleanField(default=False)
    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tournament.name}: {self.player1.name} vs {self.player2.name}"

    def clean(self):
        if self.player1 == self.player2:
            raise ValidationError('A player cannot play against themselves.')
        
        if not self.tournament.players.filter(id=self.player1.id).exists():
            raise ValidationError(f'{self.player1.name} is not part of this tournament.')
        
        if not self.tournament.players.filter(id=self.player2.id).exists():
            raise ValidationError(f'{self.player2.name} is not part of this tournament.')
        
        if self.winner and self.is_draw:
            raise ValidationError('A game cannot have both a winner and be a draw.')
        
        if self.winner and self.winner not in [self.player1, self.player2]:
            raise ValidationError('Winner must be one of the players in the game.')
        
        existing_game_1 = Game.objects.filter(
            tournament=self.tournament,
            player1=self.player1,
            player2=self.player2
        ).exclude(id=self.id if self.id else 0)
        
        existing_game_2 = Game.objects.filter(
            tournament=self.tournament,
            player1=self.player2,
            player2=self.player1
        ).exclude(id=self.id if self.id else 0)
        
        if existing_game_1.exists() or existing_game_2.exists():
            raise ValidationError('These players have already played against each other in this tournament.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.tournament.update_status()

    class Meta:
        ordering = ['-played_at']
        unique_together = []
