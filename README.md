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

All tests in `tournament_test.py` passed and the function 
`testPairingsAdvanced()` has been added to in order to recreate a full 
tournament.

`testPairingsAdvanced(debug_level)` has three possible debugging levels:
* `testPairingsAdvanced(0)`: no debug info, this is the default option (mute mode).
* `testPairingsAdvanced(1)`: debug messages level 1, before and after the functions calls.
* `testPairingsAdvanced(2)`: debug messages level 2, idem level 1 plus information from inside functions.

In debug mode (1 or 2) the system ask for the number of players in the 
tournament, enter the number and hit <enter>, and hit <enter> again in every round 
