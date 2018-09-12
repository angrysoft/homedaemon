from house.event import EventBase
from house.rgb import RGB
import sqlite3


class Event(EventBase):
    def __init__(self):
        super(Event, self).__init__()
        self._event = 'rgb'
        self._type = 'command'
        self.rgb = RGB()

    def start(self):
        self.rgb.setRgb(self.args)
        self.send(self.rgb.toSend())
        conn = sqlite3.connect('/tmp/smarthome.db', check_same_thread=False)
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS leds (number INT, value TEXT)')
        cur.execute('SELECT COUNT(1) FROM leds WHERE number=?', (0,))
        ret = cur.fetchone()
        if ret[0] == 0:
            cur.execute('INSERT INTO leds (number,value) VALUES (?,?)', (0, self.args))
        elif ret[0] == 1:
            cur.execute('UPDATE leds SET value=? WHERE number=?', (self.args, 0))
        conn.commit()
        conn.close()
