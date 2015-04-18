#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

# used to generate pairs
from itertools import combinations

# used to random assigning 'bye'
from random import choice


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches(tid=0):
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM delete_matches_by_tid(%s)", (tid,))
    db.commit()
    db.close()


def deletePlayers(tid=0):
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players")
    db.commit()
    c.execute("DELETE FROM tournaments WHERE tid = %s", (tid,))
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(pid)from players")
    count = c.fetchone()
    db.close()
    return count[0];


def registerPlayer(name, tid=0, tname="tournament_0"):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
      tid: tournament tid
      tname: tournament name

    Extra: the function has 'tid' and 'tname' as new parameters with default
    values allowing be used as anterior version and provide support for 
    more than one tournaments at same time.
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM register_player(%s,%s,%s)", (name, tid, tname,))
    db.commit()
    db.close()


def playerStandings(tid=0, giveme_bye=0):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tid for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played

    Extras: 
    - the function has 'tid' as a new parameter with a default value = 0. 
    this option allows the function be used as anterior version and provide
    support for more than one tournaments at same time.
    - the function has 'giveme_bye' as a new parameter to support odd players
    """
    db = connect()
    c = db.cursor()
    if not giveme_bye:
        c.execute("SELECT pid, name, wins, matches \
                    FROM standings WHERE tid=%s", (tid,))
    else:
        c.execute("SELECT pid, name, bye \
                    FROM standings where tid =%s",(tid,))
    standings = c.fetchall()
    db.close()
    return standings;


def reportMatch(winner, loser, draw=0):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
     
      draw: in tid matches draw=1 and the winner field in database is updated
      to value 0.
    
    Extra: the function has 'draw' as a new parameter with a default value = 0. 
    this option allows the function be used as anterior version and provide
    support for tid matches.
    """
    query = '''
        SELECT * FROM report_match(%s,%s,%s);
    '''
    db = connect()
    c = db.cursor()
    
    if not draw:
        c.execute(query, (winner, loser, winner,))
    else:
        c.execute(query, (winner, loser, 0,))
    db.commit()
    db.close()


def not_in(pair_to_test, pairs, debug_level):
    """
    checks if pair_to _test is into pairs array.
    Returns: 
        True if not in
        False if in
    """
    if debug_level>1:
        print '     pair_to_test: ', pair_to_test
    if debug_level>1:
        print '     pairs: ', pairs
    
    for player in pair_to_test:
        for pair in pairs:
            if player in pair:
                return False
    return True


def swissPairings(debug_level=0, tid=0):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name

    Extra: 
        - the function has 'tid' as a new parameter with a default value = 0. 
        this option allows the function be used as anterior version and provide
        support for more than one tournaments at same time.
        - just for debugging parameter 'debug_level' has been added with a
        default value of 0 for compatibility with udacity tests file.
    """

    # in first instance read the list of matches played (even if it is empty)
    # by means of a SQL view 'view_matches'
    db = connect()
    c = db.cursor()
    c.execute("SELECT pid1, player1, pid2, player2 FROM view_matches")
    matches = c.fetchall()
    db.close()
    
    if debug_level>1: 
        print '   matches: ', matches  
    
    # now read the list of players sorted by rank descending in order to acomplish
    # with the swiss system pairing players with the same or almost same rank.
    # here is used the SQL view standings
    
    players = playerStandings(tid, giveme_bye=1)
    
    # check the number of players for even or odd
    # if odd: take a random player (with no bye) and assign him/her a "bye" flag 
    # and a "free win" and them pop it from the list of candidates to
    # pairing
    if len(players) % 2:
        if debug_level>1:
            print '   odd players'
        while True:
            player = choice(players)
            print player
            if player[2] == 0: 
                if debug_level>1:
                    print '   found player with bye = 0, poping it from the list'
                players.pop(players.index(player))
                db = connect()
                c = db.cursor()
                c.execute("UPDATE players SET bye = 1 \
                                WHERE pid = %s", (player[0],))
                db.commit() 
                db.close()
                break
    else:
        if debug_level>1:
            print '   even players'

    # generates all the possible combinations (pairs)
    groups = combinations(players,2)
    
    # this piece of code is the core of the pairing system, it takes the 
    # combinations and check against the matches table, 
    # if it is not into that table: check if any player in the combination
    # have been used in other precedent pair
    # once the new pair passes that two filters will be inserted 
    # into the pairs list and matches table.
    # when even players the list is sorted by wins due to bye=0
    # when odd players the list is "pseudo sorted" due to one player is 
    # picked up from the list, so may appears a discontinuity in the sorting 
    pairs = []
    for group in groups:
        pair_to_test = (group[0][0], group[0][1],  group[1][0], group[1][1])
        if debug_level>1:
            print '   pair_to_test: ', pair_to_test
        if debug_level>1:
            print '   matches: ', matches
        if pair_to_test not in matches:
            if debug_level>1:
                print '   pair_to_test NOT IN matches'
            if (not_in(pair_to_test, pairs, debug_level)):
                if debug_level>1:
                    print '   pair_to_test NOT IN pairs, inserting into ----------> DB!'
                pairs.append((group[0][0], group[0][1], group[1][0], group[1][1]))
                db = connect()
                c = db.cursor()
                c.execute("INSERT INTO matches(pid1,pid2) VALUES(%s,%s)", (group[0][0], group[1][0],))
                db.commit() 
                db.close()
            else:
                if debug_level>1:
                    print '   pair_to_test has one player IN pairs, no insertion'
        else: 
            if debug_level>1:
                print '   pair_to_test IN matches, no insertion'
    return pairs

