#!/usr/bin/env python
"""
log.py - Phenny Database Logger
Copyright 2012, Alexander R.M. Minges, athemis.de
Licensed under the Eiffel Forum License 2.
"""

import os
import sqlite3

def setup(self):
    fn = '{0}_log.db'.format(self.config.host)
    self.logger_db = os.path.join(os.path.expanduser('~/.phenny'), fn)
    self.logger_conn = sqlite3.connect(self.logger_db)

    with self.logger_conn:

        cur = self.logger_conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Log (
              Time        timestamp default CURRENT_TIMESTAMP,
              Channel     varchar(255),
              Nick        varchar(255),
              Msg         text);''')        

def log(phenny, input):
    if not logger.conn:
        logger.conn = sqlite3.connect(phenny.logger_db)

    sqlite_data = {
        'channel': input.sender,
        'nick': input.nick,
        'msg': input.group(1) }

    if sqlite_data['msg'][:8] == '\x01ACTION':
        sqlite_data['msg'] = '* {0} {1}'.format(sqlite_data['nick'], sqlite_data['msg'][8:-1])

    with logger.conn:
        cur = logger.conn.cursor()

        data = (sqlite_data['channel'], sqlite_data['nick'], sqlite_data['msg'])
        cur.execute('INSERT INTO Log VALUES(CURRENT_TIMESTAMP, ?, ?, ?)', data)
logger.conn = None
logger.priority = 'low'
logger.rule = r'(.*)'
logger.thread = False

if __name__ == '__main__':
    print(__doc__.strip())
