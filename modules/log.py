#!/usr/bin/env python
"""
log.py - Phenny Database Logger
Copyright 2012, Alexander R.M. Minges, athemis.de
Licensed under the Eiffel Forum License 2.
"""

import os
import sqlite3

log_url = 'http://irclog.athemis.de'

def setup(self):
    fn = '{0}_log.db'.format(self.config.host)
    self.log_db = os.path.join(os.path.expanduser('~/.phenny'), fn)
    self.log_conn = sqlite3.connect(self.log_db)

    with self.log_conn:

        cur = self.log_conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Log (
              Time        timestamp default CURRENT_TIMESTAMP,
              Channel     varchar(255),
              Nick        varchar(255),
              Action      varchar(255),
              Msg         text);''')
              
def write_db(conn, sqlite_data):

    if len(sqlite_data) == 4:
  
        with conn:
            cur = conn.cursor()

            data = (sqlite_data['channel'], sqlite_data['nick'], sqlite_data['action'], sqlite_data['msg'])
            cur.execute('INSERT INTO Log VALUES(CURRENT_TIMESTAMP, ?, ?, ?, ?)', data)

def log_msg(phenny, input):
    if not log_msg.conn:
        log_msg.conn = sqlite3.connect(phenny.log_db)

    sqlite_data = {
        'channel': input.sender,
        'nick': input.nick,
        'action': 'PRIVMSG',
        'msg': input.group(1) }

    if sqlite_data['msg'].startswith('\x01ACTION'):
        sqlite_data['msg'] = sqlite_data['msg'].replace('\x01', '')
        sqlite_data['msg'] = sqlite_data['msg'].replace('ACTION', '').strip()
        sqlite_data['action'] = 'ACTION'

    write_db(log_msg.conn, sqlite_data)
log_msg.conn = None
log_msg.priority = 'low'
log_msg.rule = r'(.*)'
log_msg.thread = False

def log_join(phenny, input):
    if not log_join.conn:
        log_join.conn = sqlite3.connect(phenny.log_db)

        sqlite_data = {
            'channel': input.sender,
            'nick': input.nick,
            'action': 'JOIN',
            'msg': '{0} joined {1}'.format(input.nick, input.sender) }

        write_db(log_join.conn, sqlite_data)
log_join.conn = None
log_join.priority = 'low'	
log_join.event = 'JOIN'
log_join.rule = r'.*'
log_join.thread = False

def log_quit(phenny, input):
    if not log_quit.conn:
        log_quit.conn = sqlite3.connect(phenny.log_db)

        sqlite_data = {
            'channel': 'ALL',
            'nick': input.nick,
            'action': 'QUIT',
            'msg': '{0} quit'.format(input.nick) }

        write_db(log_quit.conn, sqlite_data)
log_quit.conn = None
log_quit.priority = 'low'	
log_quit.event = 'QUIT'
log_quit.rule = r'.*'
log_quit.thread = False

def log_part(phenny, input):
    if not log_part.conn:
        log_part.conn = sqlite3.connect(phenny.log_db)

        sqlite_data = {
            'channel': input.sender,
            'nick': input.nick,
            'action': 'PART',
            'msg': '{0} left {1}'.format(input.nick, input.sender) }

        write_db(log_part.conn, sqlite_data)
log_part.conn = None
log_part.priority = 'low'	
log_part.event = 'PART'
log_part.rule = r'.*'
log_part.thread = False

def log_nick(phenny, input):
    if not log_nick.conn:
        log_nick.conn = sqlite3.connect(phenny.log_db)

        sqlite_data = {
            'channel': 'ALL',
            'nick': input.nick,
            'action': 'NICK',
            'msg': '{0} changed his/her nick'.format(input.nick) }

        write_db(log_nick.conn, sqlite_data)
log_nick.conn = None
log_nick.priority = 'low'	
log_nick.event = 'NICK'
log_nick.rule = r'.*'
log_nick.thread = False

def log(phenny, input):
    phenny.reply('Today\'s log: {0}'.format(log_url))
log.commands = ['log']
log.priority = 'low'

if __name__ == '__main__':
    print(__doc__.strip())
