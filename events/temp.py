from house.event import EventBase
import sqlite3


class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'temp'
        self._type = 'sensors'

    def start(self):
        if self.args.find('.') < 0:
            return
        num, val = self.args.split('.', 1)
        conn = sqlite3.connect('/tmp/smarthome.db', check_same_thread=False)
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS sensors (number INT, value TEXT)')
        cur.execute('SELECT COUNT(1) FROM sensors WHERE number=?', (num,))
        ret = cur.fetchone()
        if ret[0] == 0:
            cur.execute('INSERT INTO sensors (number,value) VALUES (?,?)', (num, val))
        elif ret[0] == 1:
            cur.execute('UPDATE sensors SET value=? WHERE number=?', (val, num))
        conn.commit()
        conn.close()
