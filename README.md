# Udacity [Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004)
##Project 2: Tournament Results
by Angel Vidal
###About
The project has four files:
* `tournament.py`: functions to manage the database.
* `tournament.sql`: SQL file to create the database, tables and views.
* `tournament_test.py`: main file to test the `tournament.py` functions.
* `drop_all.sql`: SQL file to DELETE all database, tables and views involved 
in tournament.

To run the program type `python tournament_test.py`.

The functions have support for:
* both even and odd number of players
* games with draw
* opponent match-wins ranking
* multiple tournaments at same time

The ranking system I've adopted is the following:
* win: 2 points (2x)
* bye: 2 points (2x) (maximum one bye per player)
* draw: 1 point (1x)
* lose: 0 points (0x)
* OMW: sum of opponents wins times 1/2 (0.5x)

All tests in `tournament_test.py` passed and the function 
`testPairingsAdvanced()` has been added in order to recreate full 
tournaments giving a random result to every match (winner1, winner2 or draw with 1/3 probability for each result)
Sometimes many matches draws and so tied rankings may appear even using the OMW system...

`testPairingsAdvanced(debug_level)` has three possible debugging levels:
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
Enter number of players:  5
Players:
SELECT * FROM standings ORDER BY tid, pid;
+-----+-----+----------+---------+-----+------+-------+--------+-------+
| tid | pid |     name | matches | bye | wins | draws | losses | score |
+-----+-----+----------+---------+-----+------+-------+--------+-------+
|   0 | 929 | Player_0 |       0 |   0 |    0 |     0 |      0 |     0 |
|   0 | 930 | Player_1 |       0 |   0 |    0 |     0 |      0 |     0 |
|   0 | 931 | Player_2 |       0 |   0 |    0 |     0 |      0 |     0 |
|   1 | 932 | Player_0 |       0 |   0 |    0 |     0 |      0 |     0 |
|   1 | 933 | Player_1 |       0 |   0 |    0 |     0 |      0 |     0 |
|   1 | 934 | Player_2 |       0 |   0 |    0 |     0 |      0 |     0 |
|   1 | 935 | Player_3 |       0 |   0 |    0 |     0 |      0 |     0 |
|   1 | 936 | Player_4 |       0 |   0 |    0 |     0 |      0 |     0 |
+-----+-----+----------+---------+-----+------+-------+--------+-------+
execution paused, press <ENTER> 
tournament 0
max_rounds:  2
pairing / round 1 results
SELECT * FROM view_matches WHERE tid = 0;
+-----+------+----------+------+----------+--------+
| tid | pid1 |  player1 | pid2 |  player2 | winner |
+-----+------+----------+------+----------+--------+
|   0 | 929  | Player_0 |  930 | Player_1 |      0 |
+-----+------+----------+------+----------+--------+
tournament 0 round 1 standings
SELECT * FROM standings WHERE tid = 0;
+-----+-----+----------+---------+-----+------+-------+--------+-------+
| tid | pid |     name | matches | bye | wins | draws | losses | score |
+-----+-----+----------+---------+-----+------+-------+--------+-------+
|   0 | 931 | Player_2 |       0 |   1 |    0 |     0 |      0 |     2 |
|   0 | 929 | Player_0 |       1 |   0 |    0 |     1 |      0 |     1 |
|   0 | 930 | Player_1 |       1 |   0 |    0 |     1 |      0 |     1 |
+-----+-----+----------+---------+-----+------+-------+--------+-------+
execution paused, press <ENTER> 
pairing / round 2 results
SELECT * FROM view_matches WHERE tid = 0;
+-----+------+----------+------+----------+--------+
| tid | pid1 |  player1 | pid2 |  player2 | winner |
+-----+------+----------+------+----------+--------+
|   0 | 929  | Player_0 |  930 | Player_1 |      0 |
|   0 | 931  | Player_2 |  929 | Player_0 |    931 |
+-----+------+----------+------+----------+--------+
tournament 0 round 2 standings
SELECT * FROM standings WHERE tid = 0;
+-----+-----+----------+---------+-----+------+-------+--------+-------+
| tid | pid |     name | matches | bye | wins | draws | losses | score |
+-----+-----+----------+---------+-----+------+-------+--------+-------+
|   0 | 931 | Player_2 |       1 |   1 |    1 |     0 |      0 |     4 |
|   0 | 930 | Player_1 |       1 |   1 |    0 |     1 |      0 |     3 |
|   0 | 929 | Player_0 |       2 |   0 |    0 |     1 |      1 |     1 |
+-----+-----+----------+---------+-----+------+-------+--------+-------+
reached the needed number of rounds to get a champion, tournament 1 ended!
execution paused, press <ENTER> 
tournament 1
max_rounds:  3
pairing / round 1 results
SELECT * FROM view_matches WHERE tid = 1;
+-----+------+----------+------+----------+--------+
| tid | pid1 |  player1 | pid2 |  player2 | winner |
+-----+------+----------+------+----------+--------+
|   1 | 932  | Player_0 |  935 | Player_3 |    932 |
|   1 | 933  | Player_1 |  936 | Player_4 |    933 |
+-----+------+----------+------+----------+--------+
tournament 1 round 1 standings
SELECT * FROM standings WHERE tid = 1;
+-----+-----+----------+---------+-----+------+-------+--------+-------+
| tid | pid |     name | matches | bye | wins | draws | losses | score |
+-----+-----+----------+---------+-----+------+-------+--------+-------+
|   1 | 932 | Player_0 |       1 |   0 |    1 |     0 |      0 |     2 |
|   1 | 933 | Player_1 |       1 |   0 |    1 |     0 |      0 |     2 |
|   1 | 934 | Player_2 |       0 |   1 |    0 |     0 |      0 |     2 |
|   1 | 935 | Player_3 |       1 |   0 |    0 |     0 |      1 |     0 |
|   1 | 936 | Player_4 |       1 |   0 |    0 |     0 |      1 |     0 |
+-----+-----+----------+---------+-----+------+-------+--------+-------+
execution paused, press <ENTER> 
pairing / round 2 results
SELECT * FROM view_matches WHERE tid = 1;
+-----+------+----------+------+----------+--------+
| tid | pid1 |  player1 | pid2 |  player2 | winner |
+-----+------+----------+------+----------+--------+
|   1 | 932  | Player_0 |  933 | Player_1 |    932 |
|   1 | 932  | Player_0 |  935 | Player_3 |    932 |
|   1 | 933  | Player_1 |  936 | Player_4 |    933 |
|   1 | 934  | Player_2 |  935 | Player_3 |    934 |
+-----+------+----------+------+----------+--------+
tournament 1 round 2 standings
SELECT * FROM standings WHERE tid = 1;
+-----+-----+----------+---------+-----+------+-------+--------+-------+
| tid | pid |     name | matches | bye | wins | draws | losses | score |
+-----+-----+----------+---------+-----+------+-------+--------+-------+
|   1 | 932 | Player_0 |       2 |   0 |    2 |     0 |      0 |     4 |
|   1 | 934 | Player_2 |       1 |   1 |    1 |     0 |      0 |     4 |
|   1 | 933 | Player_1 |       2 |   0 |    1 |     0 |      1 |     2 |
|   1 | 936 | Player_4 |       1 |   1 |    0 |     0 |      1 |     2 |
|   1 | 935 | Player_3 |       2 |   0 |    0 |     0 |      2 |     0 |
+-----+-----+----------+---------+-----+------+-------+--------+-------+
execution paused, press <ENTER> 
pairing / round 3 results
SELECT * FROM view_matches WHERE tid = 1;
+-----+------+----------+------+----------+--------+
| tid | pid1 |  player1 | pid2 |  player2 | winner |
+-----+------+----------+------+----------+--------+
|   1 | 932  | Player_0 |  933 | Player_1 |    932 |
|   1 | 932  | Player_0 |  934 | Player_2 |      0 |
|   1 | 932  | Player_0 |  935 | Player_3 |    932 |
|   1 | 933  | Player_1 |  936 | Player_4 |    933 |
|   1 | 934  | Player_2 |  935 | Player_3 |    934 |
+-----+------+----------+------+----------+--------+
tournament 1 round 3 standings
SELECT * FROM standings WHERE tid = 1;
+-----+-----+----------+---------+-----+------+-------+--------+-------+
| tid | pid |     name | matches | bye | wins | draws | losses | score |
+-----+-----+----------+---------+-----+------+-------+--------+-------+
|   1 | 932 | Player_0 |       3 |   0 |    2 |     1 |      0 |     5 |
|   1 | 934 | Player_2 |       2 |   1 |    1 |     1 |      0 |     5 |
|   1 | 933 | Player_1 |       2 |   0 |    1 |     0 |      1 |     2 |
|   1 | 935 | Player_3 |       2 |   1 |    0 |     0 |      2 |     2 |
|   1 | 936 | Player_4 |       1 |   1 |    0 |     0 |      1 |     2 |
+-----+-----+----------+---------+-----+------+-------+--------+-------+
reached the needed number of rounds to get a champion, tournament 1 ended!
execution paused, press <ENTER> 

FINAL RANKINGS:

Tournament 0 results:
SELECT * FROM final_score WHERE tid = 0;
+-----+-----+----------+---------+-----+------+-------+--------+------+-------+
| tid | pid |     name | matches | bye | wins | draws | losses |  omw | score |
+-----+-----+----------+---------+-----+------+-------+--------+------+-------+
|   0 | 931 | Player_2 |       1 |   1 |    1 |     0 |      0 | 0.00 |  4.00 |
|   0 | 930 | Player_1 |       1 |   1 |    0 |     1 |      0 | 0.00 |  3.00 |
|   0 | 929 | Player_0 |       2 |   0 |    0 |     1 |      1 | 0.25 |  1.25 |
+-----+-----+----------+---------+-----+------+-------+--------+------+-------+

Tournament 1 results:
SELECT * FROM final_score WHERE tid = 1;
+-----+-----+----------+---------+-----+------+-------+--------+------+-------+
| tid | pid |     name | matches | bye | wins | draws | losses |  omw | score |
+-----+-----+----------+---------+-----+------+-------+--------+------+-------+
|   1 | 934 | Player_2 |       2 |   1 |    1 |     1 |      0 | 0.50 |  5.50 |
|   1 | 932 | Player_0 |       3 |   0 |    2 |     1 |      0 | 0.33 |  5.33 |
|   1 | 935 | Player_3 |       2 |   1 |    0 |     0 |      2 | 0.75 |  2.75 |
|   1 | 933 | Player_1 |       2 |   0 |    1 |     0 |      1 | 0.50 |  2.50 |
|   1 | 936 | Player_4 |       1 |   1 |    0 |     0 |      1 | 0.50 |  2.50 |
+-----+-----+----------+---------+-----+------+-------+--------+------+-------+
9. A complete simulation for all tournaments ended successfully!.
Success!  All tests pass!
vagrant@vagrant-ubuntu-trusty-32:/vagrant/fsnd/p2-tournament$
```
