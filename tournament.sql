-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dAShes, like
-- these lines here.


-- First of all create the databASe
CREATE DATABASE tournament;


-- Connect with it, is a postgresql specific command so review if other system
-- is used 
\c tournament;


-- Players table, used to store player's information
CREATE TABLE players(
	tid int,						-- tournament number
	pid serial,						-- player ID
	name text,						-- player's name
	matches int,					-- matches played
	wins int,						-- matches wins
	draws int,						-- matches draws
	bye int,						-- used in tournaments with odd players
	PRIMARY KEY (pid)
	);


-- matches table, used for store pairings and results of every match
CREATE TABLE matches(					
	pid1 int REFERENCES players(pid), 	-- player 1 in the match
	pid2 int REFERENCES players(pid), 	-- player 2 in the match
	winner int,							-- match winner
	PRIMARY KEY (pid1, pid2)			-- primary key player's id.
	);


-- some usefull views:

-- view the standings sorted by score
-- the weights for wins, draws and losses are 2, 1 and 0 resp.
-- a bye counts like a win
CREATE VIEW standings AS
	SELECT 	tid, 
			pid, 
			name, 
			matches, 
			bye, 
			wins, 
			draws, 
			matches-(wins+draws) AS losses, 
			wins *2 + draws *1 + bye *2 AS score
		FROM players 
			ORDER BY tid, 
					 score DESC, 
					 wins DESC;


-- view the final list of players score with OMW calculation
-- per tournament
-- it's a bit complex view compounds by one UNION and a JOIN and some math.
-- the weights for wins, draws and losses are the same above and OMW has 0.5x
CREATE VIEW final_score AS
	SELECT 	pl.tid,
			pl.pid, 
			pl.name, 
			pl.matches, 
			pl.bye,
			pl.wins, 
			pl.draws, 
			pl.matches-(pl.wins+pl.draws) AS losses,
			ROUND((SUM(op.wins*0.5 + 0.0) / (pl.matches+0.0)), 2) AS omw,
			ROUND(((pl.wins *2 + pl.draws *1 + pl.bye *2) + (SUM(op.wins *0.5 +0.0) / 
				(pl.matches+0.0))), 2) AS score
		FROM (
			SELECT 	players.tid,
					players.pid, 
					players.name, 
					players.matches, 
					players.wins, 
					players.draws, 
					players.bye, 
					matches.pid1 AS opp 
				FROM players, matches 
					WHERE matches.pid2 = players.pid
			UNION
			SELECT 	players.tid,
					players.pid, 
					players.name, 
					players.matches, 
					players.wins, 
					players.draws, 
					players.bye, 
					matches.pid2 AS opp 
				FROM players, matches 
					WHERE matches.pid1 = players.pid
			) AS pl
		LEFT JOIN players AS op
			ON pl.opp = op.pid
		GROUP BY pl.tid,
				 pl.pid,
				 pl.name,
				 pl.matches,
				 pl.wins,
				 pl.draws,
				 pl.bye
		ORDER BY tid, 
				 score DESC, 
				 wins DESC;


-- view the matches with player's name and winner 
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
				ON p2.pid = matches.pid2;

