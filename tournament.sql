-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- first delete the database (change to any other database just be allowed to
-- delete 'tournament' db) (all stuff inside db is deleted, use with caution!)
\c postgres
DROP DATABASE tournament;


-- First of all create the database
CREATE DATABASE tournament;


-- Connect with it, it is a postgresql specific command must be reviewed for 
-- other system
\c tournament;


-- Tournaments table
CREATE TABLE tournaments(
	tid int NOT NULL,
	tname text,
	PRIMARY KEY (tid)
	);


-- Players table, used to store player's information
-- ON DELETE CASCADE allows delete all players (and matches...) when delete any
-- tournament
CREATE TABLE players(
	tid int REFERENCES tournaments(tid) 
		ON DELETE CASCADE,		-- tournament number
	pid serial,					-- player ID
	name text,					-- player's name
	bye int DEFAULT 0,			-- used in tournaments with odd players
	PRIMARY KEY (pid)
	);


-- Matches table, used for store pairings and results of every match
-- ON DELETE CASCADE propagates deletes from players or tournaments...
CREATE TABLE matches(					
	pid1 int REFERENCES players(pid) 
		ON DELETE CASCADE, 					-- player 1 in the match
	pid2 int REFERENCES players(pid) 
		ON DELETE CASCADE, 					-- player 2 in the match
	winner int,								-- match winner
	PRIMARY KEY (pid1, pid2)				-- primary key player's id.
	);


-- Some usefull views:
-- view the matches with player's name and winner and etc.
CREATE VIEW view_matches AS
	SELECT 	p1.tid AS "tid",	
			p1.pid AS "pid1", 
			p1.name AS "player1", 
			p2.pid AS "pid2", 
			p2.name AS "player2", 
			matches.winner AS "winner" 
		FROM matches
			JOIN players AS p1 
				ON p1.pid = matches.pid1
			JOIN players AS p2 
				ON p2.pid = matches.pid2
		ORDER BY tid,
				 pid1,
				 pid2;


-- counting the draws
CREATE VIEW count_draws AS
	SELECT players.tid,
		   players.pid,
		   COUNT(matches.winner) AS draws
	FROM players LEFT JOIN matches
		ON (players.pid = matches.pid1 OR players.pid = matches.pid2) AND
			matches.winner = 0
	GROUP BY players.pid
	ORDER BY players.pid;


-- counting the wins
CREATE VIEW count_wins AS
	SELECT
		players.tid,
		players.pid,
		COUNT(matches.winner) AS wins
	FROM players LEFT JOIN matches
		ON players.pid = matches.winner
	GROUP BY players.pid
	ORDER BY players.pid;


-- counting the matches
CREATE VIEW count_matches AS
	SELECT
		players.tid,
		players.pid,
		COUNT(matches.winner) AS matches
	FROM players LEFT JOIN matches
		ON (players.pid = matches.pid1 OR players.pid = matches.pid2)
	GROUP BY players.pid
	ORDER BY players.pid;


-- view the standings order by wins.
CREATE VIEW standings AS
	SELECT players.tid,
		   tournaments.tname,
		   players.pid,
		   players.name,
		   count_matches.matches,
		   players.bye,
		   count_wins.wins,
		   count_wins.wins + players.bye AS wins_plus_bye,
		   count_draws.draws,
		   count_matches.matches - (count_wins.wins + count_draws.draws) AS losses
		FROM players, tournaments, count_draws, count_wins, count_matches
		WHERE players.tid = tournaments.tid AND
			  players.pid = count_matches.pid AND 
			  players.pid = count_wins.pid AND
			  players.pid = count_draws.pid
	ORDER BY wins_plus_bye DESC;


-- Global variables to define the weights for wins, draws, losses and OMW:
\set wins_weight 	2
\set bye_weight 	2
\set draws_weight 	1
\set losses_weight 	0
\set OMW_weight 	0.5


-- view the final list of players score with OMW (Opponents Match-Wins) figures
-- it's a bit complex view compounds by one UNION, a JOIN and some math.
-- the weights for wins, draws and losses are the same above and OMW has 0.5x
-- to figure out OMW is used the number of victories excluded the bye(free-wins)
CREATE VIEW v_final_score AS
	SELECT 	p.tid,
			p.tname,
			p.pid, 
			p.name, 
			p.matches, 
			p.bye,
			p.wins, 
			p.draws, 
			p.losses,
			ROUND((SUM(op.wins * :wins_weight + 0.0) / (p.matches+0.0)), 2) AS omw,
			ROUND(((p.wins * :wins_weight + p.draws *
					:draws_weight + p.bye * :bye_weight) +
					(SUM(op.wins * :OMW_weight+0.0)
					/ (p.matches+0.0))), 2) AS score
		FROM (
			SELECT 	standings.tid,
					standings.tname,
					standings.pid, 
					standings.name, 
					standings.matches, 
					standings.wins, 
					standings.draws,
					standings.losses,
					standings.bye, 
					matches.pid1 AS opp 
				FROM standings, matches 
					WHERE matches.pid2 = standings.pid
			UNION
			SELECT 	standings.tid,
					standings.tname,
					standings.pid, 
					standings.name, 
					standings.matches, 
					standings.wins, 
					standings.draws,
					standings.losses, 
					standings.bye, 
					matches.pid2 AS opp 
				FROM standings, matches 
					WHERE matches.pid1 = standings.pid
			) AS p
		LEFT JOIN standings AS op
			ON p.opp = op.pid
		GROUP BY p.tid,
				 p.tname,
				 p.pid,
				 p.name,
				 p.matches,
				 p.bye,
				 p.wins,
				 p.draws,
				 p.losses
		ORDER BY tid,
				 score DESC, 
				 wins DESC;


-- Some usefull functions:
-- report_match(int, int, int): updates or inserts (if doesn't exist) a match
-- result into the matches table. It is used by python function reportMatch()
CREATE FUNCTION report_match(integer, integer, integer)
RETURNS VOID AS $$
BEGIN
	IF EXISTS (SELECT 1 FROM matches
					WHERE (pid1 =$1 AND pid2 =$2))
		THEN
    		UPDATE matches SET winner = $3
    			WHERE (pid1 =$1 AND pid2 =$2);
    ELSIF EXISTS (SELECT 1 FROM matches
					WHERE (pid1=$2 AND pid2=$1))
		THEN
    		UPDATE matches SET winner = $3
    			WHERE (pid1=$2 AND pid2=$1);
    		--RAISE '2:-EXISTS! UPDATE...';
    ELSE
    	INSERT INTO matches(pid1, pid2, winner) VALUES($1, $2, $3);
    	--RAISE 'NOT EXISTS! INSERT INTO...';
    END IF;
END;
$$ LANGUAGE plpgsql;


-- register_player(): inserts new player into DB. Inserts or update tournament
-- info in tournament table. 
CREATE FUNCTION register_player(varchar(20), integer, varchar(20))
RETURNS VOID AS $$
BEGIN
	IF NOT EXISTS (SELECT 1 FROM tournaments
					WHERE tid =$2)
		THEN
    		INSERT INTO tournaments(tid, tname) VALUES($2, $3);
    END IF;
    INSERT INTO players(tid,name) VALUES ($2, $1);
END;
$$ LANGUAGE plpgsql;


-- Deletes the matches that belongs to one expecific tournament.
-- It is used by python function deleteMatches()
CREATE FUNCTION delete_matches_by_tid(integer)
RETURNS VOID AS $$
BEGIN
	DELETE FROM matches
		WHERE 	pid1 IN (SELECT pid FROM players WHERE tid = $1)
				OR
				pid2 IN (SELECT pid FROM players WHERE tid = $1);
END;
$$ LANGUAGE plpgsql;


-- -- -- just to test, delete before submit!!!
-- INSERT INTO tournaments (tid, tname) VALUES(0, 'tour 0');
-- INSERT INTO tournaments (tid, tname) VALUES(1, 'tour 1');

-- INSERT INTO players(tid, name) VALUES(0,'name 0');
-- INSERT INTO players(tid, name) VALUES(0,'name 1');
-- INSERT INTO players(tid, name) VALUES(0,'name 2');
-- INSERT INTO players(tid, name) VALUES(0,'name 3');
-- INSERT INTO players(tid, name) VALUES(1,'name 4');
-- INSERT INTO players(tid, name) VALUES(1,'name 5');
-- INSERT INTO players(tid, name) VALUES(1,'name 6');
-- INSERT INTO players(tid, name) VALUES(1,'name 7');

-- INSERT INTO matches(pid1, pid2, winner) VALUES(1,2,1);
-- INSERT INTO matches(pid1, pid2, winner) VALUES(3,4,4);
-- INSERT INTO matches(pid1, pid2, winner) VALUES(1,3,0);
-- INSERT INTO matches(pid1, pid2, winner) VALUES(5,6,1);
-- INSERT INTO matches(pid1, pid2, winner) VALUES(7,8,0);
