from house.event import EventBase
import sqlite3


class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'light'
        self._type = 'sensors'

    def start(self):
        if self.args.find('.') < 0:
            return
        num, val = self.args.split('.', 1)
        conn = sqlite3.connect('/tmp/smarthome.db', check_same_thread=False)
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS light (number INT, value TEXT)')
        cur.execute('SELECT COUNT(1) FROM light WHERE number=?', (num,))
        ret = cur.fetchone()
        if ret[0] == 0:
            cur.execute('INSERT INTO light (number,value) VALUES (?,?)', (num, val))
        elif ret[0] == 1:
            cur.execute('UPDATE light SET value=? WHERE number=?', (val, num))
        conn.commit()
        conn.close()
