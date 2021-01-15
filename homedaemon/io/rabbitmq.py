from __future__ import annotations
import typing
from homedaemon.io import BaseInput
from homedaemon.bus import Bus
import asyncio
import amqp
import json
from typing import Dict, Any


class Input(BaseInput):
    def __init__(self, bus: Bus, config:Dict[str, Any], loop):
        super(Input, self).__init__(bus, loop)
        self.config = config
        self.connection:amqp.Connection
        self.connected = False
        self.channel = None
        self.sslopts = {'certfile': self.config['rabbitmq']['certfile'],
                        'keyfile': self.config['rabbitmq']['keyfile'],
                        'cafile': self.config['rabbitmq']['cafile'],
                        'password': self.config['rabbitmq']['password'],
                        "server_hostname": self.config['rabbitmq']['host']}
        self.bus.add_trigger('report.*.*.*', self.publish_msg)
        self.bus.add_trigger('homed.device.init.*', self.publish_msg)
    
    def connect(self):
        while not self.connected:
            try:
                self.connection = amqp.Connection(f"{self.config['rabbitmq']['host']}:{self.config['rabbitmq']['port']}",
                                                  userid=self.config['rabbitmq']['user'], password=self.config['rabbitmq']['user_password'],
                                                  ssl=self.config['rabbitmq']['ssl'], ssl_options=self.sslopts, login_method='AMQPLAIN')
                self.channel = self.connection.channel()
                self.channel.exchange_declare('homedaemon', 'topic', auto_delete=False)
                self.channel.queue_declare('homed_queue')
                self.channel.queue_bind('homed_queue', 'homedaemon', routing_key=f"homedaemon.{self.config['homed']['homeid']}.in")
                self.channel.basic_consume(queue='homed_queue', callback=self.on_message, no_ack=True)
                self.connected = True
                self.publish_msg({"cmd": "connect", "homeid": self.config['homed']['homeid']}, routing_key='homedaemon.main')
                self.bus.emit('info.rabbitmq.status.online')
            except ConnectionRefusedError as err:
                self.connected = False
                self.bus.emit('info.rabbitmq.status.offline')
                print(err)
                sleep(10)
    
    def on_message(self, msg:Any) -> None:
        print('on_msg', msg)
        try:
            self.bus.emit_cmd(json.loads(msg.body)) 
        except json.JSONDecodeError as err:
                print(f'json {err} : {msg}')
    
    def publish_msg(self, msg:Any, routing_key:str ='') -> None:
        print(msg)
        if not routing_key:
            routing_key = f"homedaemon.{self.config['homed']['homeid']}.reports"
            
        if self.connected:
            try:
                print('msg: ', msg)
                txt_msg = json.dumps(msg)
                self.channel.basic_publish(amqp.Message(txt_msg), exchange='homedaemon', routing_key=routing_key)
            except json.JSONDecodeError as err:
                print(f'json {err} : {msg}')
            
    def run(self) -> None:
        self.connect()
        while True:
            try:
                self.connection.drain_events()
            except ConnectionResetError:
                self.connected = False
                self.connect()
            except OSError:
                self.connected = False
                self.connect()

    

