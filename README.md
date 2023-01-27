# Prediction Model for NHL

### Description

Using machine learning algorithms i build predictive model

### Data

Collected data took from [flashscore](https://www.flashscorekz.com/hockey/). This website provides a lot of sport results, including football, tennis and other sport games. Probably site collects results just for last 7 days and updates every day. To collect a huge dataset for better accuracy of my model, i should collect data for several days.
`parser.py` is a script which collects results of games played for last week and table standings of teams for current day.
All collected data based in `data` folder.

##### Data Explanation:

`table.json` has a following structure:
```
    "team": "Boston", - team name
    "pos": 1,  - team current position in league table of all teams
    "sg": 183, - goals scored
    "cg": 101, - goals against
    "tp": 80,  - total points
    "win_rate": 0.7916666667,  - winning rate
    "lose_rate": 0.2083333333, - losing rate
    "win_rate_ft": 0.8684210526, - winning rate without OT
    "lose_rate_ft": 0.6,   - losing rate without OT
    "tie_ft_rate": 0.1875, - draw rate
    "sg_per_game": 3.8125, - goals scored per game
    "cg_per_game": 2.1041666667 - goals against per game
```
`table_home.json` - this table describes team statistics, when it plays at home stadium:
```
    "team": "Boston", - team name
    "sg_home": 81, - goals scored
    "cg_home": 55, - goals against
    "tp_home": 34, - the number of points collected in home games
    "win_rate_home": 0.7083333333, - win rate
    "lose_rate_home": 0.2916666667, - lose rate
    "sg_per_game_home": 3.375, - goals scored per game
    "cg_per_game_home": 2.2916666667, - goals against per game
    "tie_ft_rate_home": 0.125 - draw rate
```
`table_guest.json` - this table describes team statistics, when it plays away
```
    "team": "Seattle Kraken", - team name
    "sg_guest": 99, - goals scored
    "cg_guest": 74, - goals against
    "tp_guest": 34, - the number of points collected in away games
    "win_rate_guest": 0.6956521739, - win rate
    "lose_rate_guest": 0.3043478261, - lose rate
    "sg_per_game_guest": 4.3043478261, - goals scored per game
    "cg_per_game_guest": 3.2173913043, - goals against per game
    "tie_ft_rate_guest": 0.1304347826 - draw rate
```

After all aggregations, final data for training model will be in `next_tour_games.json`.

```
    "home_team": "New York Islanders",
    "guest_team": "Detroit Red Wings",
    "date": 1674874800000, - date of game
    "h_pos": 21, - home team position in league table
    "h_sg": 144, - home team goals scored
    "h_cg": 143, - home team goals against
    "h_tp": 51, - home team total points
    "h_win_rate": 0.46, - home team win rate
    "h_lose_rate": 0.54, - home team lose rate
    "h_win_rate_ft": 0.8695652174, - home team win rate without OT
    "h_lose_rate_ft": 0.8148148148, - home team lose rate without OT
    "h_tie_ft_rate": 0.16, - home team draw rate
    "h_sg_per_game": 2.88, - home team goals scored per game
    "h_cg_per_game": 2.86, - home team goals against per game
    "g_pos": 22, - guest team position in league table
    "g_sg": 145, - guest team goals scored
    "g_cg": 158, - guest team goals against
    "g_tp": 50, - guest team total points
    "g_win_rate": 0.4468085106, - guest team win rate
    "g_lose_rate": 0.5531914894, - guest team lose rate
    "g_win_rate_ft": 0.7619047619, - guest team win rate without OT
    "g_lose_rate_ft": 0.6923076923, - guest team lose rate without OT
    "g_tie_ft_rate": 0.2765957447, - guest team draw rate
    "g_sg_per_game": 3.085106383, - guest team goals scored per game
    "g_cg_per_game": 3.3617021277, - guest team goals against per game
    "sg_home": 68, - home team scored goals at home
    "cg_home": 60, - home team against goals at home
    "tp_home": 28, - home team total points in home games
    "win_rate_home": 0.5416666667, - home team win rate in home games
    "lose_rate_home": 0.4583333333, - home team lose rate in home games
    "sg_per_game_home": 2.8333333333, - home team scored goals per game in home
    "cg_per_game_home": 2.5, - home team goals against per game in home
    "tie_ft_rate_home": 0.1666666667, - home team draw rate in home game
    "sg_guest": 70, - guest team scored goals in away game
    "cg_guest": 82, - guest team goals against in away game
    "tp_guest": 23, - guest team total points in away games
    "win_rate_guest": 0.4090909091, - guest team win rate in away game
    "lose_rate_guest": 0.5909090909, - guest team lose rate in away game
    "sg_per_game_guest": 3.1818181818, - guest team goals scored per away game
    "cg_per_game_guest": 3.7272727273, - guest team goals against per away game
    "tie_ft_rate_guest": 0.3636363636 - guest team draw rate in away game
```
