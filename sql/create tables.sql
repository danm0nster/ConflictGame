DROP TABLE IF EXISTS questionnaire;
DROP TABLE IF EXISTS session_order;
DROP TABLE IF EXISTS information;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS computer_agent;
DROP TABLE IF EXISTS attack;
DROP TABLE IF EXISTS game_phase;
DROP TABLE IF EXISTS exp_session_to_jid;
DROP TABLE IF EXISTS jabber_id;
DROP TABLE IF EXISTS experimental_session;

CREATE TABLE experimental_session
(
ID int AUTO_INCREMENT,
experiment_date DATETIME NOT NULL,
template varchar(255),
location varchar(255) NOT NULL,
experimenter_name varchar(255) NOT NULL,
server_version varchar(255) NOT NULL,
PRIMARY KEY(ID)
);

CREATE TABLE jabber_id
(
ID varchar(255),
PRIMARY KEY(ID)
);

CREATE TABLE exp_session_to_jid
(
ID int AUTO_INCREMENT,
jabber_ID varchar(255),
exp_session_ID int,
PRIMARY KEY (ID),
FOREIGN KEY(jabber_ID) REFERENCES jabber_id(ID),
FOREIGN KEY(exp_session_ID) REFERENCES experimental_session(ID)
);

CREATE TABLE game_phase
(
ID int AUTO_INCREMENT,
start_time DATETIME NOT NULL,
end_time DATETIME,
exp_session_ID int,
PRIMARY KEY(ID),
FOREIGN KEY(exp_session_ID) REFERENCES experimental_session(ID) 
);

CREATE TABLE attack
(
ID int AUTO_INCREMENT,
game_phase_ID int NOT NULL,
round_number int NOT NULL, 
attack_time int NOT NULL,
attacker varchar(255),
defender varchar(255),
PRIMARY KEY(ID),
FOREIGN KEY(attacker) REFERENCES jabber_id(ID),
FOREIGN KEY(defender) REFERENCES jabber_id(ID),
FOREIGN KEY(game_phase_ID) REFERENCES game_phase(ID)
);

CREATE TABLE computer_agent
(
ID int AUTO_INCREMENT,
type varchar(255) NOT NULL,
version varchar(255) NOT NULL,
jabber_ID varchar(255),
PRIMARY KEY(ID),
FOREIGN KEY(jabber_ID) REFERENCES jabber_id(ID)
);

CREATE TABLE client
(
ID int AUTO_INCREMENT,
version varchar(255) NOT NULL,
client_condition varchar(255),
jabber_ID varchar(255),
PRIMARY KEY(ID),
FOREIGN KEY(jabber_ID) REFERENCES jabber_id(ID)
);

CREATE TABLE information
(
ID int AUTO_INCREMENT,
info_string varchar(255) NOT NULL,
PRIMARY KEY(ID)
);

CREATE TABLE questionnaire
(
ID int,
PRIMARY KEY(ID)
);

CREATE TABLE session_order
(
ID int AUTO_INCREMENT,
turn_number int NOT NULL,
game_phase_ID int NULL,
information_ID int NULL,
questionnaire_ID int UNIQUE NULL,
exp_session_ID int,
PRIMARY KEY(ID),
FOREIGN KEY(exp_session_ID) REFERENCES experimental_session(ID),
FOREIGN KEY(game_phase_ID) REFERENCES game_phase(ID),
FOREIGN KEY(information_ID) REFERENCES information(ID)
);


ALTER TABLE experimental_session CONVERT TO CHARACTER SET utf8;
