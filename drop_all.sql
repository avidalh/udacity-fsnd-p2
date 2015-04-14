-- This file is for DELETE all views, tables and database
-- USE WITH CAREFULL!

DROP VIEW standings;
DROP VIEW view_matches;
DROP VIEW final_score;

DROP TABLE matches;
DROP TABLE players;


-- In order to drop the database connect to other one to be allowed to do it
-- is a postgresql specific command, review for other systems
\c postgres

-- and finally delete th database
DROP DATABASE tournament;

