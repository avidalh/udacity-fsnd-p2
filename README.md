# Udacity [Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004)
##Project 2: Tournament Results </h2>
by Angel Vidal
###About
The project has three python files:
* `tournament.py`: functions to manage the database.
* `tournament.sql`: SQL file to create the database, tables and views.
* `tournament_test.py`: main file to test the `tournament.py` functions.
* `drop_all.sql`: SQL file to DELETE all database, tables and views involved 
in tournament.

To run the program type `python tournament_test.py`.

The function swissPairing(s) has support for both even and odd number of players.

All tests in `tournament_test.py` are passed and the function 
`testPairingsAdvanced()` has been added in order to recreate a full 
tournament.

`testPairingsAdvanced(debug_level)` has three possible debugging levels:
* `testPairingsAdvanced()`: no debug info, this is the default option (mute mode).
* `testPairingsAdvanced(1)`: debug messages level 1, before and after the functions calls.
* `testPairingsAdvanced(2)`: debug messages level 2, idem level 1 plus information from inside functions.

In debug mode (1 or 2) the system ask for the number of players in the 
tournament, enter the number, hit `<enter>`, and hit `<enter>` again in every round.
The output in debug mode 1 is something like this:
```
$ python tournament_test.py 
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
Tournament simulation
Enter number of players:  3
Players:
SELECT * FROM view_standings ORDER BY id;
+----+----------+---------+-----+------+-----+
| id | name     | matches | won | lost | bye |
+----+----------+---------+-----+------+-----+
| 36 | Player_1 |       0 |   0 |    0 |   0 |
| 37 | Player_2 |       0 |   0 |    0 |   0 |
| 38 | Player_3 |       0 |   0 |    0 |   0 |
+----+----------+---------+-----+------+-----+
execution paused, press <ENTER> 
max_rounds:  2
pairing / round 1 results
SELECT * FROM view_matches;
+-----+----------+-----+----------+-----------+
| id1 | player1  | id2 |  player2 | winner id |
+-----+----------+-----+----------+-----------+
|  36 | Player_1 |  37 | Player_2 |        36 |
+-----+----------+-----+----------+-----------+
round 1 standings
SELECT * FROM view_standings;
+----+----------+---------+-----+------+-----+
| id | name     | matches | won | lost | bye |
+----+----------+---------+-----+------+-----+
| 38 | Player_3 |       0 |   1 |    0 |   1 |
| 36 | Player_1 |       1 |   1 |    0 |   0 |
| 37 | Player_2 |       1 |   0 |    1 |   0 |
+----+----------+---------+-----+------+-----+
execution paused, press <ENTER> 
pairing / round 2 results
SELECT * FROM view_matches;
+-----+----------+-----+----------+-----------+
| id1 | player1  | id2 |  player2 | winner id |
+-----+----------+-----+----------+-----------+
|  36 | Player_1 |  37 | Player_2 |        36 |
|  38 | Player_3 |  36 | Player_1 |        38 |
+-----+----------+-----+----------+-----------+
round 2 standings
SELECT * FROM view_standings;
+----+----------+---------+-----+------+-----+
| id | name     | matches | won | lost | bye |
+----+----------+---------+-----+------+-----+
| 38 | Player_3 |       1 |   2 |    0 |   1 |
| 37 | Player_2 |       1 |   1 |    1 |   1 |
| 36 | Player_1 |       2 |   1 |    1 |   0 |
+----+----------+---------+-----+------+-----+
reached the needed number of rounds to get a champion, tournament ended successfully! 
9. A complete tournament ended successfully!.
Success!  All tests pass!
$ 
```
