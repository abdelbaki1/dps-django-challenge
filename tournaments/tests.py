from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Player, Tournament, Game


class PlayerModelTest(TestCase):
    def test_create_player(self):
        player = Player.objects.create(name="Test Player")
        self.assertEqual(player.name, "Test Player")
        self.assertIsNotNone(player.created_at)


class TournamentModelTest(TestCase):
    def setUp(self):
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.player3 = Player.objects.create(name="Player 3")
        self.tournament = Tournament.objects.create(name="Test Tournament")

    def test_tournament_status_planning_with_no_players(self):
        self.tournament.update_status()
        self.assertEqual(self.tournament.status, 'planning')

    def test_tournament_status_planning_with_players_no_games(self):
        self.tournament.players.add(self.player1, self.player2)
        self.tournament.update_status()
        self.assertEqual(self.tournament.status, 'planning')

    def test_total_expected_games_calculation(self):
        self.tournament.players.add(self.player1, self.player2, self.player3)
        self.assertEqual(self.tournament.get_total_expected_games(), 3)


class GameModelTest(TestCase):
    def setUp(self):
        self.player1 = Player.objects.create(name="Player 1")
        self.player2 = Player.objects.create(name="Player 2")
        self.tournament = Tournament.objects.create(name="Test Tournament")
        self.tournament.players.add(self.player1, self.player2)

    def test_create_game_with_winner(self):
        game = Game.objects.create(
            tournament=self.tournament,
            player1=self.player1,
            player2=self.player2,
            winner=self.player1
        )
        self.assertEqual(game.winner, self.player1)
        self.assertFalse(game.is_draw)

    def test_create_game_with_draw(self):
        game = Game.objects.create(
            tournament=self.tournament,
            player1=self.player1,
            player2=self.player2,
            is_draw=True
        )
        self.assertTrue(game.is_draw)
        self.assertIsNone(game.winner)


class TournamentAPITest(APITestCase):
    def setUp(self):
        self.player1 = Player.objects.create(name="Alice")
        self.player2 = Player.objects.create(name="Bob")
        self.player3 = Player.objects.create(name="Charlie")

    def test_create_tournament(self):
        url = '/api/tournaments/'
        data = {'name': 'Spring Tournament', 'players': []}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tournament.objects.count(), 1)

    def test_add_player_to_tournament(self):
        tournament = Tournament.objects.create(name="Test Tournament")
        url = f'/api/tournaments/{tournament.id}/add_player/'
        data = {'player_id': self.player1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(tournament.players.filter(id=self.player1.id).exists())

    def test_leaderboard_endpoint(self):
        tournament = Tournament.objects.create(name="Test Tournament")
        tournament.players.add(self.player1, self.player2, self.player3)
        
        Game.objects.create(
            tournament=tournament,
            player1=self.player1,
            player2=self.player2,
            winner=self.player1
        )
        
        url = f'/api/tournaments/{tournament.id}/leaderboard/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('leaderboard', response.data)
        self.assertEqual(response.data['status'], 'started')
