-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- First of all create the database
CREATE DATABASE tournament;


-- Connect with it, is a postgresql specific command so review if other system
-- is used 
\c tournament;


-- Players table, used to store player's information
CREATE TABLE players(
	id serial PRIMARY KEY,
	name text,						-- player's name
	matches int,					-- matches played
	wins int,						-- matches wins
	bye int							--used in tournaments with odd players
	);


-- matches table, used for store pairings and results of every match
CREATE TABLE matches(					
	id1 int REFERENCES players(id), --player 1 in the match
	id2 int REFERENCES players(id), --player 2 in the match
	winner int,						--match winner
	PRIMARY KEY (id1, id2)			--primary key player's id.
	);


-- some usefull views
-- view the standings sorted by matches wins
CREATE VIEW view_standings AS
	SELECT id, name, matches, wins, matches+bye-wins as "losses", bye 
		FROM players 
		ORDER BY wins DESC;


-- view the matches with player's name and winner 
CREATE VIEW view_matches AS
	SELECT p1.id AS "id1", 
		   p1.name AS "player1", 
		   p2.id AS "id2", 
		   p2.name AS "player2", 
		   matches.winner AS "winner id" 
		FROM matches
			JOIN players as p1 on p1.id = matches.id1
			JOIN players as p2 on p2.id = matches.id2;



CREATE VIEW view_standings_omw AS
	select op.id, op.name, op.matches, op.wins, sum(pl.wins) as omw, op.matches + op.bye - op.wins as losses, op.bye
		from (
			select players.id, players.name, players.matches, players.wins, players.bye, matches.id2 as id_opp 
				from matches, players
					where matches.id1 = players.id 
				UNION 
			select players.id, players.name, players.matches, players.wins, players.bye, matches.id1 as id_opp 
				from players, matches 
					where matches.id2 = players.id ) as op
		left join players as pl 
			on op.id_opp = pl.id 
		group by op.id, op.name, op.matches, op.wins, op.bye, pl.bye
		ORDER by
			wins DESC, omw DESC;



-- select op.id, op.name, op.matches, op.wins, sum(pl.wins) as omw, op.matches + op.bye - op.wins as losses, op.bye
-- from (
-- select players.id, players.name, players.matches, players.wins, players.bye, matches.id2 as id_opp 
-- from matches, players
-- where matches.id1 = players.id 
-- UNION 
-- select players.id, players.name, players.matches, players.wins, players.bye, matches.id1 as id_opp 
-- from players, matches 
-- where matches.id2 = players.id ) as op
-- left join players as pl 
-- on op.id_opp = pl.id 
-- group by op.id, op.name, op.matches, op.wins, op.bye
-- ORDER by
-- wins DESC, omw DESC;

-- select op.id, op.name, op.matches, op.wins, sum(pl.wins)-pl.bye as omw, op.matches + op.bye - op.wins as losses, op.bye
-- from (
-- select players.id, players.name, players.matches, players.wins, players.bye, matches.id2 as id_opp 
-- from matches, players
-- where matches.id1 = players.id 
-- UNION 
-- select players.id, players.name, players.matches, players.wins, players.bye, matches.id1 as id_opp 
-- from players, matches 
-- where matches.id2 = players.id ) as op
-- left join players as pl 
-- on op.id_opp = pl.id 
-- group by op.id, op.name, op.matches, op.wins, op.bye
-- ORDER by
-- wins DESC, omw DESC;

