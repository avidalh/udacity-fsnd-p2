#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *
from prettytable import PrettyTable
from math import log, ceil
from random import getrandbits, choice

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def print_query(query):
    """
    print the query array in the psql way to easy view of the database tables
    """
    db = connect()
    c = db.cursor()
    c.execute(query)
    rows = c.fetchall()
    db.close()
    col_names = [cn[0] for cn in c.description]
    y=PrettyTable()
    y.padding_width = 1
    for i in range(len(rows[0])):
        y.add_column(col_names[i],[row[i] for row in rows])
        y.align[col_names[i]]="r"
    y.align[col_names[1]]="l"
    print query
    print y


def testPairingsAdvanced(debug_level=0, ):
    """
    advanced test to check whole tournaments.
    enter the number of tournaments and players (even or odd) and the function
    simulates the tournaments rounds setting random winner/loser/draw in each
    match. 
    To view the output info set debug_level to 1 or 2 in the function call at 
    the end of the source code. 
    In each round the standings and matches table are displayed.
    Finally the final score is displayed for each tournament.
    """
    deleteMatches()
    deletePlayers()    
    
    # in debug mode ask for the number of players, if normal mode uses 8 players and 2 tournaments
    # players must be more than one and tournaments must be more than zero...
    if debug_level:
        print "Tournament simulation"
        print "Enter number of tournaments: ",
        tournaments_number = 0
        while True:
            try:
                tournaments_number = int(raw_input())
                if tournaments_number >0:
                    break
            except:
                pass
            print "Enter number of tournaments (must be more than zero!): ",

        players_number = []
        for t in range(tournaments_number):
            print "Tournament number %d" % t
            print "Enter number of players: ",
            
            while True:
                try: 
                    number = (int(raw_input()))
                    if number >1:
                        players_number.append(number)
                        for i in range(number):
                            registerPlayer('Player_%d' % i, t)
                        break
                except:
                    pass
                print "Enter number of players (must be more than one!): ",
                        
                
    else: 
        players_number = [2,5,3]
        tournaments_number = 3

    # create players names and insert them into DB 
        for tournament in range(int(tournaments_number)):
            for i in range(players_number[tournament]):
                registerPlayer('Player_%d' % i, tournament)

    # in debug mode shows the generated list of players

    # print players_number

    if debug_level:
        print 'Players:'
        print_query("SELECT * FROM standings ORDER BY tid, pid;")
        print 'execution paused, press <ENTER>',
        raw_input()

    for tournament in range(tournaments_number):
        # calculate the number of rounds in the tournament
        # max rounds will be the upper nearest int of log(base2)(players number)
        max_rounds = int(ceil(log(players_number[tournament], 2)))
        if debug_level:
            print 'tournament %d' % tournament
            print 'max_rounds: ', max_rounds
        rnd = 0
        
        # looping until tournament ends...
        
        while True:
            rnd += 1
            pairs = []

            # call the function to pairing the players
            pairings =  swissPairings(debug_level,tournament)
            
            if debug_level > 1:
                print 'pairings: ', pairings

            # create a pairs list with only the players ID
            for pair in pairings:
                pairs.append((pair[0], pair[2]))

            # and use it to report the matches results
            for pair in pairs:
                if choice([0,1,2]) == 0:
                    reportMatch(pair[0], pair[1], 1)
                else:
                    if bool(getrandbits(2)):
                        reportMatch(pair[0], pair[1])
                    else:
                        reportMatch(pair[1], pair[0])
            # debugging info
            if debug_level:
                print 'pairing / round %s results' % rnd
                print_query("SELECT * FROM view_matches WHERE tid = %s;" % tournament)
            if debug_level:
                print('tournament %d round %d standings' % (tournament, rnd))
                print_query("SELECT * FROM standings WHERE tid = %s;" % tournament)

            # if rounds exhausted the tournament ends
            if rnd == max_rounds:
                if debug_level: 
                    print "reached the needed number of rounds to get a champion," \
                          " tournament %s ended!" % t
                    print 'execution paused, press <ENTER>',
                    raw_input()
                break

            # pause to evaluate the debug info in each round
            if debug_level: 
                print 'execution paused, press <ENTER>',
                raw_input()
    if debug_level:
        print('All Tournaments and Players final rank:')
        for tournament in range(tournaments_number):
            print_query("SELECT * FROM final_score WHERE tid = %s;" % tournament)
    print "9. A complete simulation for all tournaments ended successfully!."

if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()

    # use as you like:
    # testPairingsAdvanced()   # no info shown
    # testPairingsAdvanced(1)  # debug level 1 (info..)
    # testPairingsAdvanced(2)  # debug level 2 (more info...)
    testPairingsAdvanced(1)

    print "Success!  All tests pass!"
