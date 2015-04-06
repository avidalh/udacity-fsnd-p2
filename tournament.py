#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from itertools import combinations


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(id)from players")
    count = c.fetchone()
    db.close()
    return count[0];


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players(name,matches,winned,bye) VALUES(%s,0,0,0)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has winned
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT id, name, winned, matches FROM players ORDER BY winned DESC")
    standings = c.fetchall()
    db.close()
    return standings;


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who winned
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("UPDATE players SET winned = winned+1, matches = matches+1 WHERE id = %s", (winner,))
    db.commit()
    c.execute("UPDATE players SET matches = matches+1 WHERE id = %s", (loser,))
    db.commit()
    c.execute("UPDATE matches SET winner = %s WHERE (id1 = %s AND id2 = %s) \
                OR (id1 = %s AND id2 = %s) ", (winner, winner, loser,loser, winner,))
    db.commit()
    db.close()



def not_in(pair_to_test, pairs, debug_level):
    """
    checks if the pair to test is into pairs array.
    return  True if not in
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


def swissPairings(debug_level=0):
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
    """

    # in first instance read the list of matches played (even if it is empty)
    # by means of a SQL view
    db = connect()
    c = db.cursor()
    c.execute("SELECT id1, player1, id2, player2 FROM view_matches")
    matches = c.fetchall()
    db.close()
    
    if debug_level>1: 
        print '   matches: ', matches  
    
    # now read the list of players sorted by rank descending
    # here is used another SQL view
    db = connect()
    c = db.cursor()
    c.execute("SELECT id, name, bye FROM view_standings")
    players = c.fetchall()
    db.close()

    #check the number of players for even or odd
    # if odd: take the last player and assign him/her a "bye" flag and 
    # give a "free win" 
    # 
    if len(players) % 2:
        if debug_level>1:
            print '   odd players'
        for player in reversed(players):
            if player[2] == 0: 
                if debug_level>1:
                    print '   found player with bye = 0, poping it from the list'
                players.pop()
                db = connect()
                c = db.cursor()
                c.execute("UPDATE players SET winned = winned+1, bye = 1 WHERE id = %s",
                             (player[0],))
                db.commit() 
                db.close()
                break
    else:
        if debug_level>1:
            print '   even players'

    pairs = []

    # generates all the possible combinations 
    groups = combinations(players,2)
    
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
                    print '   pair_to_test NOT IN pairs, inserting into DB *******'
                pairs.append((group[0][0], group[0][1], group[1][0], group[1][1]))
                db = connect()
                c = db.cursor()
                c.execute("INSERT INTO matches(id1,id2) VALUES(%s,%s)", (group[0][0], group[1][0],))
                db.commit() 
                db.close()
            else:
                if debug_level>1:
                    print '   pair_to_test has one player IN pairs, no insertion'
        else: 
            if debug_level>1:
                print '   pair_to_test IN matches, no insertion'

    return pairs


    





















