#!/usr/bin/python

from datetime import datetime
from urllib import request
import json

utcoffset = datetime.now() - datetime.utcnow()
with request.urlopen('https://api.sunrise-sunset.org/json?lat=52.2319581&lng=21.0067249&formatted=0') as r:
    try:    
        ret = json.loads(r.read().decode())
        if 'results' in  ret:
            ret = ret['results']
            sunrise_utc = datetime.fromisoformat(ret.get('sunrise', '')) + utcoffset
            sunset_utc = datetime.fromisoformat(ret.get('sunset', '')) + utcoffset
            print(f'{sunrise_utc.hour:02}:{sunrise_utc.minute:02}')
            print(f'{sunset_utc.hour:02}:{sunset_utc.minute:02}')
    except json.JSONDecodeError:
        pass
    
       