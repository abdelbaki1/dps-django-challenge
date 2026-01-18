  
  ## How I Have Addressed the Challenge Requirements
  
 The project was designed to fully address the Challenge requirements:
  
  ### 1. **Tournament Management**
  - **Create tournaments**: `POST /api/tournaments/` allows creating new tournaments
  - **Add players to tournaments**: `POST /api/tournaments/{id}/add_player/` enables adding up to 5 players per tournament
  - **Tournament constraints**: The system enforces the maximum of 5 participants per tournament
  
  ### 2. **Player Management**
  - **Create players**: `POST /api/players/` creates new player profiles
  - **Player assignment**: Players can be added to multiple tournaments
  - **Player tracking**: Each player's performance is tracked across all their games
  
  ### 3. **Game Results**
  - **Record game results**: `POST /api/games/` allows entering game outcomes
  - **Points system implementation**:
    - Win: 2 points (when `winner` is specified)
    - Draw: 1 point each (when `is_draw` is true)
    - Loss: 0 points (automatically calculated)
  - **Round-robin validation**: Ensures each pair of players plays exactly once per tournament
  
  ### 4. **Special Leaderboard Endpoint** (Main Requirement)
  The `GET /api/tournaments/{id}/leaderboard/` endpoint provides:
  
  **Tournament Status:**
  - **Planning**: Tournament has less than 2 players or no games played
  - **Started**: At least one game played but tournament not complete
  - **Finished**: All required round-robin games completed (everyone played everyone)
  
  **Leaderboard Data:**
  - List of all tournament participants
  - Points sorted in descending order
  - Detailed statistics: wins, draws, losses, games played
  - Real-time updates as games are recorded
  

# API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Endpoints

### Players

#### 1. List All Players
```
GET /api/players/
```
**Response:**
```json
[
  {
    "id": 1,
    "name": "Player 1",
    "created_at": "2024-01-17T12:00:00Z"
  }
]
```

#### 2. Create a Player
```
POST /api/players/
```
**Request Body:**
```json
{
  "name": "Player 1"
}
```
**Response:**
```json
{
  "id": 1,
  "name": "Player 1",
  "created_at": "2024-01-17T12:00:00Z"
}
```

#### 3. Get Player Details
```
GET /api/players/{id}/
```

#### 4. Update Player
```
PUT /api/players/{id}/
PATCH /api/players/{id}/
```

#### 5. Delete Player
```
DELETE /api/players/{id}/
```

---

### Tournaments

#### 1. List All Tournaments
```
GET /api/tournaments/
```
**Response:**
```json
[
  {
    "id": 1,
    "name": "Summer Championship",
    "status": "planning",
    "players": [1, 2, 3],
    "players_count": 3,
    "created_at": "2024-01-17T12:00:00Z",
    "updated_at": "2024-01-17T12:00:00Z"
  }
]
```

#### 2. Create a Tournament
```
POST /api/tournaments/
```
**Request Body:**
```json
{
  "name": "Summer Championship",
  "players": []
}
```
**Response:**
```json
{
  "id": 1,
  "name": "Summer Championship",
  "status": "planning",
  "players": [],
  "players_count": 0,
  "created_at": "2024-01-17T12:00:00Z",
  "updated_at": "2024-01-17T12:00:00Z"
}
```

#### 3. Get Tournament Details
```
GET /api/tournaments/{id}/
```

#### 4. Update Tournament
```
PUT /api/tournaments/{id}/
PATCH /api/tournaments/{id}/
```

#### 5. Delete Tournament
```
DELETE /api/tournaments/{id}/
```

#### 6. Add Player to Tournament
```
POST /api/tournaments/{id}/add_player/
```
**Request Body:**
```json
{
  "player_id": 1
}
```
**Response:**
```json
{
  "message": "Player Player 1 added to tournament Summer Championship."
}
```

#### 7. Remove Player from Tournament
```
DELETE /api/tournaments/{id}/remove_player/
```
**Request Body:**
```json
{
  "player_id": 1
}
```
**Response:**
```json
{
  "message": "Player Player 1 removed from tournament Summer Championship."
}
```

#### 8. Get Tournament Leaderboard (Special Endpoint)
```
GET /api/tournaments/{id}/leaderboard/
```
**Response:**
```json
{
  "tournament_id": 1,
  "tournament_name": "Summer Championship",
  "status": "started",
  "total_players": 4,
  "total_games_played": 3,
  "total_expected_games": 6,
  "leaderboard": [
    {
      "player_id": 1,
      "player_name": "Player 1",
      "points": 6,
      "wins": 3,
      "draws": 0,
      "losses": 0,
      "games_played": 3
    },
    {
      "player_id": 2,
      "player_name": "Player 2",
      "points": 4,
      "wins": 2,
      "draws": 0,
      "losses": 1,
      "games_played": 3
    }
  ]
}
```

**Status Values:**
- `planning`: Tournament has less than 2 players or no games have been played
- `started`: At least one game has been played but not all games are complete
- `finished`: All required games have been played (everyone played everyone)

---

### Games

#### 1. List All Games
```
GET /api/games/
```
**Query Parameters:**
- `tournament`: Filter by tournament ID

**Response:**
```json
[
  {
    "id": 1,
    "tournament": 1,
    "player1": 1,
    "player2": 2,
    "player1_name": "Player 1",
    "player2_name": "Player 2",
    "winner": 1,
    "winner_name": "Player 1",
    "is_draw": false,
    "played_at": "2024-01-17T12:00:00Z"
  }
]
```

#### 2. Create a Game (Record Game Result)
```
POST /api/games/
```
**Request Body (Win):**
```json
{
  "tournament": 1,
  "player1": 1,
  "player2": 2,
  "winner": 1,
  "is_draw": false
}
```

**Request Body (Draw):**
```json
{
  "tournament": 1,
  "player1": 1,
  "player2": 2,
  "winner": null,
  "is_draw": true
}
```

**Response:**
```json
{
  "id": 1,
  "tournament": 1,
  "player1": 1,
  "player2": 2,
  "player1_name": "Player 1",
  "player2_name": "Player 2",
  "winner": 1,
  "winner_name": "Player 1",
  "is_draw": false,
  "played_at": "2024-01-17T12:00:00Z"
}
```

#### 3. Get Game Details
```
GET /api/games/{id}/
```

#### 4. Update Game
```
PUT /api/games/{id}/
PATCH /api/games/{id}/
```

#### 5. Delete Game
```
DELETE /api/games/{id}/
```

---

## Example Workflow

### 1. Create Players
```bash
curl -X POST http://localhost:8000/api/players/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'

curl -X POST http://localhost:8000/api/players/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob"}'

curl -X POST http://localhost:8000/api/players/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Charlie"}'
```

### 2. Create Tournament
```bash
curl -X POST http://localhost:8000/api/tournaments/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Spring Tournament", "players": []}'
```

### 3. Add Players to Tournament
```bash
curl -X POST http://localhost:8000/api/tournaments/1/add_player/ \
  -H "Content-Type: application/json" \
  -d '{"player_id": 1}'

curl -X POST http://localhost:8000/api/tournaments/1/add_player/ \
  -H "Content-Type: application/json" \
  -d '{"player_id": 2}'

curl -X POST http://localhost:8000/api/tournaments/1/add_player/ \
  -H "Content-Type: application/json" \
  -d '{"player_id": 3}'
```

### 4. Record Game Results
```bash
# Alice beats Bob
curl -X POST http://localhost:8000/api/games/ \
  -H "Content-Type: application/json" \
  -d '{"tournament": 1, "player1": 1, "player2": 2, "winner": 1, "is_draw": false}'

# Alice draws with Charlie
curl -X POST http://localhost:8000/api/games/ \
  -H "Content-Type: application/json" \
  -d '{"tournament": 1, "player1": 1, "player2": 3, "winner": null, "is_draw": true}'

# Bob beats Charlie
curl -X POST http://localhost:8000/api/games/ \
  -H "Content-Type: application/json" \
  -d '{"tournament": 1, "player1": 2, "player2": 3, "winner": 2, "is_draw": false}'
```

### 5. Get Leaderboard
```bash
curl http://localhost:8000/api/tournaments/1/leaderboard/
```

---

## Validation Rules

### Tournament
- Maximum 5 players per tournament
- Status is automatically updated based on games played

### Game
- Players must be part of the tournament
- A player cannot play against themselves
- Each pair of players can only play once per tournament
- A game must have either a winner OR be a draw (not both)
- Winner must be one of the two players in the game

### Points System
- Win: 2 points
- Draw: 1 point
- Loss: 0 points

---

## Error Responses

All error responses follow this format:
```json
{
  "error": "Error message description"
}
```

Or for validation errors:
```json
{
  "field_name": ["Error message for this field"]
}
```

Common HTTP Status Codes:
- `200 OK`: Successful GET, PUT, PATCH, DELETE
- `201 Created`: Successful POST
- `400 Bad Request`: Validation error
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
