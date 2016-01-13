delimiter //
DROP TRIGGER IF EXISTS trg_turn_number_insert//
CREATE TRIGGER trg_turn_number_insert BEFORE INSERT ON session_order
FOR EACH ROW
BEGIN
    declare msg varchar(255);
    # check if mutually excusive values are exclusive
    declare non_null_entries int;
    IF (new.game_phase_ID IS NOT NULL) THEN
        set non_null_entries = ifnull(non_null_entries, 0) +1;
    END IF;
    IF (new.information_ID IS NOT NULL) THEN
        set non_null_entries = ifnull(non_null_entries, 0) +1;
    END IF;
    IF (new.questionnaire_ID IS NOT NULL) THEN
        set non_null_entries = ifnull(non_null_entries, 0) +1;
    END IF;
    # if not exclusive raise error
    IF non_null_entries > 1 THEN
        SET msg = 'game_phase_ID, information_ID and questionnaire_ID is mutually exclusive';
        signal sqlstate '45000' set message_text = msg;
    END IF;

    # check for turn number consistency
    IF EXISTS (SELECT turn_number 
               FROM session_order 
               WHERE exp_session_ID = new.exp_session_ID AND turn_number = new.turn_number ) THEN
    SET msg = 'Turn number have allready been used';
        signal sqlstate '45000' set message_text = msg;
    END IF;

    # 
END//

delimiter ;
