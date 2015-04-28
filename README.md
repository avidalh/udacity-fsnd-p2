# Udacity [Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004)
##Project 2: Tournament Results
by Angel Vidal
###About
The project has these files:
* `tournament.py`: functions to manage the database.
* `tournament.sql`: SQL file to create the database, tables functions, and views.
* `tournament_test.py`: main file to test the `tournament.py` functions.

In order to use the program you should:
- clone the git repository
- use `tournament.sql`to create the database using `\i tournament.sql` command from psql environment
- run the program typewriting `python tournament_test.py` from the command line and evaluate

The functions have support for:
* both even and odd number of players
* games with draw
* opponent match-wins ranking
* multiple tournaments at same time

I've adopted the following weights for the final score table:
* win: 2 points  (2x)
* bye: 2 points  (2x) (same as win and maximum one bye per player)
* draw: 1 point  (1x)
* lose: 0 points (0x)
* OMW: 1/2 point (0.5x)
You can change these values in `tournament.sql` at the variables declaration.

All tests in `tournament_test.py` passed and the function 
`testPairingsAdvanced()` has been added in order to recreate full tournaments, setting a random result to every match (winner1, winner2 or draw with 1/3 probability for each result).
Sometimes many matches draws and tied rankings may appear even using the OMW system! Anyway random means random... ;-)


Function `testPairingsAdvanced(debug_level)` in `tournament_test.py` has three possible debugging levels:
* `testPairingsAdvanced()`: no debug info, this is the default option (mute mode).
* `testPairingsAdvanced(1)`: debug messages level 1, before and after the functions calls.
* `testPairingsAdvanced(2)`: debug messages level 2, idem level 1 plus information from inside functions.

In debug mode (1 or 2) the system asks for the number of players in the 
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
...
...
FINAL RANKINGS:

Tournament 0 results:
SELECT * FROM final_score WHERE tid = 0;
+-----+--------------+-----+----------+---------+-----+------+-------+--------+------+-------+
| tid | tname        | pid |     name | matches | bye | wins | draws | losses |  omw | score |
+-----+--------------+-----+----------+---------+-----+------+-------+--------+------+-------+
|   0 | Tournament_0 | 431 | Player_0 |       1 |   1 |    0 |     1 |      0 | 2.00 |  4.00 |
|   0 | Tournament_0 | 432 | Player_1 |       2 |   0 |    1 |     1 |      0 | 0.00 |  3.00 |
|   0 | Tournament_0 | 433 | Player_2 |       1 |   1 |    0 |     0 |      1 | 2.00 |  3.00 |
+-----+--------------+-----+----------+---------+-----+------+-------+--------+------+-------+

Tournament 1 results:
SELECT * FROM final_score WHERE tid = 1;
+-----+--------------+-----+----------+---------+-----+------+-------+--------+------+-------+
| tid | tname        | pid |     name | matches | bye | wins | draws | losses |  omw | score |
+-----+--------------+-----+----------+---------+-----+------+-------+--------+------+-------+
|   1 | Tournament_1 | 436 | Player_2 |       2 |   0 |    2 |     0 |      0 | 0.00 |  4.00 |
|   1 | Tournament_1 | 434 | Player_0 |       2 |   0 |    2 |     0 |      0 | 0.00 |  4.00 |
|   1 | Tournament_1 | 435 | Player_1 |       2 |   0 |    0 |     0 |      2 | 2.00 |  1.00 |
|   1 | Tournament_1 | 437 | Player_3 |       2 |   0 |    0 |     0 |      2 | 2.00 |  1.00 |
+-----+--------------+-----+----------+---------+-----+------+-------+--------+------+-------+
9. A complete simulation for all tournaments ended successfully!.
Success!  All tests pass!
```
