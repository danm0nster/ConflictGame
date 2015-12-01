INSERT INTO experimental_session(experiment_date, template, location, experimenter_name, server_version)
VALUES('2015-11-25 12:00:13', 'test', 'cobelab', 'tets mctest', '0.1');

INSERT INTO jabber_id
VALUES('test1@ylgw036484');

INSERT INTO jabber_id
VALUES('test2@ylgw036484');

INSERT INTO exp_session_to_jid(jabber_ID, exp_session_ID)
VALUES('test1@ylgw036484', 1);

INSERT INTO exp_session_to_jid(jabber_ID, exp_session_ID)
VALUES('test2@ylgw036484', 1);

INSERT INTO game_phase(start_time, end_time, exp_session_ID)
VALUES('2015-11-25 12:02:13', '2015-11-25 13:00:13', 1);

INSERT INTO attack(game_phase_ID, round_number, attack_time, attacker, defender)
VALUES(1, 1, '1015-11-25 12:02:41', 'test1@ylgw036484', 'test2@ylgw036484');

INSERT INTO computer_agent(type, version, jabber_ID)
VALUES('test_type', 'min condition 1.2', 'test2@ylgw036484');
    
INSERT INTO client(version, client_condition, jabber_ID)
VALUES('1.3', 'min. condition', 'test1@ylgw036484');

INSERT INTO information(info_string)
VALUES('test for information, this is some long string');

INSERT INTO session_order(turn_number, game_phase_ID, information_ID, questionnaire_ID, exp_session_ID)
VALUES(1, 1, null, null, 1);

INSERT INTO session_order(turn_number, game_phase_ID, information_ID, questionnaire_ID, exp_session_ID)
VALUES(2, null, 1, null, 1);

INSERT INTO session_order(turn_number, game_phase_ID, information_ID, questionnaire_ID, exp_session_ID)
VALUES(3, null, null, 1, 1);
