# Udacity [Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004)
##Project 2: Tournament Results
by Angel Vidal
###About
The project has these files:
* `tournament.py`: functions to manage the database.
* `tournament.sql`: SQL file to create the database, tables functions, and views.
* `tournament_test.py`: main file to test the `tournament.py` functions.

In order to use the program you should:
1- clone the git repository
2- use `tournament.sql`to create the database using `\i tournament.sql` command from psql environment
3- run the program typping `python tournament_test.py` and evaluate

The functions have support for:
* both even and odd number of players
* games with draw
* opponent match-wins ranking
* multiple tournaments at same time

I've adopted the followings weights for the final score table:
* win: 2 points  (2x)
* bye: 2 points  (2x) (same as win and maximum one bye per player)
* draw: 1 point  (1x)
* lose: 0 points (0x)
* OMW: 1/2 point (0.5x)

All tests in `tournament_test.py` passed and the function 
`testPairingsAdvanced()` has been added in order to recreate full 
tournaments setting a random result to every match (winner1, winner2 or draw with 1/3 probability for each result)
Sometimes many matches draws and so tied rankings may appear even using the OMW system...


Function `testPairingsAdvanced(debug_level)` in `tournament_test.py` has three possible debugging levels:
* `testPairingsAdvanced()`: no debug info, this is the default option (mute mode).
* `testPairingsAdvanced(1)`: debug messages level 1, before and after the functions calls.
* `testPairingsAdvanced(2)`: debug messages level 2, idem level 1 plus information from inside functions.

In debug mode (1 or 2) the system ask for the number of players in the 
tournament, enter the number, hit `<enter>`, and hit `<enter>` again in every round.
The output in debug mode 1 is something like this:
```
vagrant@vagrant-ubuntu-trusty-32:/vagrant/fsnd/p2-tournament$ python tournament_test.py 
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
Tournaments simulation
Enter number of tournaments:  2
Tournament number 0
Enter number of players:  3
Tournament number 1
Enter number of players:  4
Players:
SELECT * FROM standings ORDER BY tid, pid;
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
| tid | tname        | pid |     name | matches | bye | wins | wins_plus_bye | draws | losses |
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
|   0 | Tournament_1 |  33 | Player_0 |       0 |   0 |    0 |             0 |     0 |      0 |
|   0 | Tournament_1 |  34 | Player_1 |       0 |   0 |    0 |             0 |     0 |      0 |
|   0 | Tournament_1 |  35 | Player_2 |       0 |   0 |    0 |             0 |     0 |      0 |
|   1 | Tournament_1 |  36 | Player_0 |       0 |   0 |    0 |             0 |     0 |      0 |
|   1 | Tournament_1 |  37 | Player_1 |       0 |   0 |    0 |             0 |     0 |      0 |
|   1 | Tournament_1 |  38 | Player_2 |       0 |   0 |    0 |             0 |     0 |      0 |
|   1 | Tournament_1 |  39 | Player_3 |       0 |   0 |    0 |             0 |     0 |      0 |
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
execution paused, press <ENTER> 
tournament 0
max_rounds:  2
(33, 'Player_0', 0)
pairing / round 1 results
SELECT * FROM view_matches WHERE tid = 0;
+-----+------+----------+------+----------+--------+
| tid | pid1 |  player1 | pid2 |  player2 | winner |
+-----+------+----------+------+----------+--------+
|   0 | 34   | Player_1 |   35 | Player_2 |     35 |
+-----+------+----------+------+----------+--------+
tournament 0 round 1 standings
SELECT * FROM standings WHERE tid = 0;
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
| tid | tname        | pid |     name | matches | bye | wins | wins_plus_bye | draws | losses |
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
|   0 | Tournament_1 |  33 | Player_0 |       0 |   1 |    0 |             1 |     0 |      0 |
|   0 | Tournament_1 |  35 | Player_2 |       1 |   0 |    1 |             1 |     0 |      0 |
|   0 | Tournament_1 |  34 | Player_1 |       1 |   0 |    0 |             0 |     0 |      1 |
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
execution paused, press <ENTER> 
(34, 'Player_1', 0)
pairing / round 2 results
SELECT * FROM view_matches WHERE tid = 0;
+-----+------+----------+------+----------+--------+
| tid | pid1 |  player1 | pid2 |  player2 | winner |
+-----+------+----------+------+----------+--------+
|   0 | 33   | Player_0 |   35 | Player_2 |     33 |
|   0 | 34   | Player_1 |   35 | Player_2 |     35 |
+-----+------+----------+------+----------+--------+
tournament 0 round 2 standings
SELECT * FROM standings WHERE tid = 0;
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
| tid | tname        | pid |     name | matches | bye | wins | wins_plus_bye | draws | losses |
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
|   0 | Tournament_1 |  33 | Player_0 |       1 |   1 |    1 |             2 |     0 |      0 |
|   0 | Tournament_1 |  34 | Player_1 |       1 |   1 |    0 |             1 |     0 |      1 |
|   0 | Tournament_1 |  35 | Player_2 |       2 |   0 |    1 |             1 |     0 |      1 |
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
reached the needed number of rounds to get a champion, tournament 1 ended!
execution paused, press <ENTER> 
tournament 1
max_rounds:  2
pairing / round 1 results
SELECT * FROM view_matches WHERE tid = 1;
+-----+------+----------+------+----------+--------+
| tid | pid1 |  player1 | pid2 |  player2 | winner |
+-----+------+----------+------+----------+--------+
|   1 | 36   | Player_0 |   37 | Player_1 |     37 |
|   1 | 38   | Player_2 |   39 | Player_3 |     39 |
+-----+------+----------+------+----------+--------+
tournament 1 round 1 standings
SELECT * FROM standings WHERE tid = 1;
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
| tid | tname        | pid |     name | matches | bye | wins | wins_plus_bye | draws | losses |
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
|   1 | Tournament_1 |  37 | Player_1 |       1 |   0 |    1 |             1 |     0 |      0 |
|   1 | Tournament_1 |  39 | Player_3 |       1 |   0 |    1 |             1 |     0 |      0 |
|   1 | Tournament_1 |  36 | Player_0 |       1 |   0 |    0 |             0 |     0 |      1 |
|   1 | Tournament_1 |  38 | Player_2 |       1 |   0 |    0 |             0 |     0 |      1 |
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
execution paused, press <ENTER> 
pairing / round 2 results
SELECT * FROM view_matches WHERE tid = 1;
+-----+------+----------+------+----------+--------+
| tid | pid1 |  player1 | pid2 |  player2 | winner |
+-----+------+----------+------+----------+--------+
|   1 | 36   | Player_0 |   37 | Player_1 |     37 |
|   1 | 36   | Player_0 |   38 | Player_2 |     38 |
|   1 | 37   | Player_1 |   39 | Player_3 |      0 |
|   1 | 38   | Player_2 |   39 | Player_3 |     39 |
+-----+------+----------+------+----------+--------+
tournament 1 round 2 standings
SELECT * FROM standings WHERE tid = 1;
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
| tid | tname        | pid |     name | matches | bye | wins | wins_plus_bye | draws | losses |
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
|   1 | Tournament_1 |  37 | Player_1 |       2 |   0 |    1 |             1 |     1 |      0 |
|   1 | Tournament_1 |  38 | Player_2 |       2 |   0 |    1 |             1 |     0 |      1 |
|   1 | Tournament_1 |  39 | Player_3 |       2 |   0 |    1 |             1 |     1 |      0 |
|   1 | Tournament_1 |  36 | Player_0 |       2 |   0 |    0 |             0 |     0 |      2 |
+-----+--------------+-----+----------+---------+-----+------+---------------+-------+--------+
reached the needed number of rounds to get a champion, tournament 1 ended!
execution paused, press <ENTER> 

FINAL RANKINGS:

Tournament 0 results:
SELECT * FROM v_final_score WHERE tid = 0;
+-----+--------------+-----+----------+---------+-----+------+-------+--------+------+-------+
| tid | tname        | pid |     name | matches | bye | wins | draws | losses |  omw | score |
+-----+--------------+-----+----------+---------+-----+------+-------+--------+------+-------+
|   0 | Tournament_1 |  33 | Player_0 |       1 |   1 |    1 |     0 |      0 | 2.00 |  4.50 |
|   0 | Tournament_1 |  34 | Player_1 |       1 |   1 |    0 |     0 |      1 | 2.00 |  2.50 |
|   0 | Tournament_1 |  35 | Player_2 |       2 |   0 |    1 |     0 |      1 | 1.00 |  2.25 |
+-----+--------------+-----+----------+---------+-----+------+-------+--------+------+-------+

Tournament 1 results:
SELECT * FROM v_final_score WHERE tid = 1;
+-----+--------------+-----+----------+---------+-----+------+-------+--------+------+-------+
| tid | tname        | pid |     name | matches | bye | wins | draws | losses |  omw | score |
+-----+--------------+-----+----------+---------+-----+------+-------+--------+------+-------+
|   1 | Tournament_1 |  39 | Player_3 |       2 |   0 |    1 |     1 |      0 | 2.00 |  3.50 |
|   1 | Tournament_1 |  37 | Player_1 |       2 |   0 |    1 |     1 |      0 | 1.00 |  3.25 |
|   1 | Tournament_1 |  38 | Player_2 |       2 |   0 |    1 |     0 |      1 | 1.00 |  2.25 |
|   1 | Tournament_1 |  36 | Player_0 |       2 |   0 |    0 |     0 |      2 | 2.00 |  0.50 |
+-----+--------------+-----+----------+---------+-----+------+-------+--------+------+-------+
9. A complete simulation for all tournaments ended successfully!.
Success!  All tests pass!
```
