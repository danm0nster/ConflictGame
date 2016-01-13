# -*- coding: utf-8 -*-
import pymysql
from time import strftime


class DatabaseManager(object):
    def __init__(self):
        try:
            db_file = open('db_settings.ini', 'r')
            lines = db_file.readlines()
            # for each relevant line, it checks it the formatting is appropriate
            # it does this by sub stringing the line and checking the value vs the expected value
            # if it's wrong it raises an exception saying that the db_settings file is malformed
            if lines[0][:5] != 'user=':
                raise IOError('db_settings malformed')
            if lines[1][:9] != 'password=':
                raise IOError('db_settings malformed')
            if lines[2][:3] != 'db=':
                raise IOError('db_settings malformed')
            # initiates variables to the values in the settings file
            self._user = lines[0][5:].strip()
            self._secret = lines[1][9:].strip()
            self._db = lines[2][3:].strip()
            self._exp_session_id = None
            self._current_game_phase = None
        except IOError:
            # TODO message informing user that it can't connect to the database
            pass

    def connect(self):
        connection = pymysql.connect(host='rankdb.cobelab.au.dk',
                         user=self._user,
                         password=self._secret,
                         db=self._db,
                         charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
        return connection

    def start_experimental_session(self, template, location, experimenter_name, server_version):
        con = self.connect()
        try:
            with con.cursor() as cursor:
                sql = "INSERT INTO experimental_session" \
                      "(experiment_date, template, location, experimenter_name, server_version)" \
                      "VALUES(%s, %s, %s, %s, %s);"
                cur_time = strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(sql, (str(cur_time), str(template), str(location),
                                     str(experimenter_name), str(server_version)))
            con.commit()

            # Finds ID of current session by getting highest ID value, meaning the one we just inserted
            with con.cursor() as cursor:
                sql = "SELECT MAX(ID) FROM experimental_session"
                cursor.execute(sql)
                self._exp_session_id = cursor.fetchone()['MAX(ID)']
        finally:
            con.close()

    def start_new_game_phase(self):
        con = self.connect()
        try:
            with con.cursor() as cursor:
                sql = "INSERT INTO game_phase(start_time, exp_session_ID)" \
                      "VALUES(%s, %s);"
                cur_time = strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(sql, (str(cur_time), self._exp_session_id))
            con.commit()

            # Finds ID of the game session
            with con.cursor() as cursor:
                sql = "SELECT MAX(ID) FROM game_phase"

                cursor.execute(sql)
                self._current_game_phase = cursor.fetchone()['MAX(ID)']
        finally:
            con.close()

    def end_game_phase(self):
        con = self.connect()
        try:
            with con.cursor() as cursor:
                sql = "UPDATE game_phase" \
                      " SET end_time = %s" \
                      " WHERE ID = %s"
                cur_time = strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(sql, (str(cur_time), self._current_game_phase))
            con.commit()

            self._current_game_phase = None
        finally:
            con.close()

    def insert_attacks(self, attacks, round_number):
        con = self.connect()
        try:
            with con.cursor() as cursor:
                for attack in attacks:
                    print attack
                    print attacks[attack]
                    sql = "INSERT INTO attack(game_phase_ID, round_number, attack_time, attacker, defender)" \
                          "VALUES(%s, %s, %s, %s, %s);"
                    # TODO change from current time to number of ms it took
                    cur_time = strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute(sql, (self._current_game_phase, round_number, str(cur_time), attack, attacks[attack]))
            con.commit()
        finally:
            con.close()

    def insert_session_order(self, experimental_round, game_phase=None, information=None, questionnaire=None):
        con = self.connect()
        if game_phase is not None:
            game_phase = self._current_game_phase
        try:
            with con.cursor() as cursor:
                sql = "INSERT INTO session_order(turn_number, game_phase_ID, information_ID, questionnaire_ID, exp_session_ID)" \
                      "VALUES(%s, %s, %s, %s, %s);"
                cursor.execute(sql, (experimental_round, game_phase, information, questionnaire, self._exp_session_id))
            con.commit()
        finally:
            con.close()

    def register_jabber_ids(self, jabber_id_list):
        con = self.connect()
        try:
            with con.cursor() as cursor:
                for jid in jabber_id_list:
                    sql = "INSERT INTO exp_session_to_jid(jabber_ID, exp_session_ID)" \
                          "VALUES(%s, %s);"
                    cursor.execute(sql, (jid.name, self._exp_session_id))
            con.commit()
        finally:
            con.close()
