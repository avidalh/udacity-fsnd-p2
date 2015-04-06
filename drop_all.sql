-- This file is for DELETE all views, tables and database
-- USE WITH CAREFULL!

DROP VIEW view_standings;
DROP VIEW view_matches;

DROP TABLE matches;

DROP TABLE players;

-- In order to drop the database connect to other one to be allowed to do it
-- is a postgresql specific command, review for other systems
\c postgres

DROP DATABASE tournament;

