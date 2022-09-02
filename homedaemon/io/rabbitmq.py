from __future__ import annotations
from homedaemon.io import BaseInput
from homedaemon.bus import Bus
import amqpstorm
import ssl
import json
from typing import Dict, Any
from time import sleep
import asyncio

class Input(BaseInput):
    def __init__(self, bus: Bus, config:Dict[str, Any], loop):
        super(Input, self).__init__(bus, loop)
        self.config = config
        self.connection:amqpstorm.Connection
        self.connected = False
        self.channel:amqpstorm.Channel | None = None
        context = ssl.create_default_context(cafile=self.config['rabbitmq']['cafile'])
        context.load_cert_chain(certfile=self.config['rabbitmq']['certfile'],
                                keyfile=self.config['rabbitmq']['keyfile'],
                                password=self.config['rabbitmq']['password'])
        
        self.ssl_options = {'context': context,
                            'check_hostname': True,
                            "server_hostname": self.config['rabbitmq']['host']}
        self.bus.add_trigger('report.*.*.*', self.publish_msg)
        self.bus.add_trigger('homed.device.init.*', self.publish_msg)
    
    def connect(self):
        while not self.connected and self.loop.is_running():
            try:
                self.connection:amqpstorm.Connection = amqpstorm.Connection(hostname=self.config['rabbitmq']['host'],
                                                                            username=self.config['rabbitmq']['user'],
                                                                            password=self.config['rabbitmq']['user_password'],
                                                                            port=self.config['rabbitmq']['port'],
                                                                            ssl=self.config['rabbitmq']['ssl'],
                                                                            ssl_options=self.ssl_options)
                self.channel:amqpstorm.Channel = self.connection.channel()
                self.channel.exchange.declare(exchange='homedaemon', exchange_type='topic', auto_delete=False)
                self.channel.queue.declare(queue='homed_queue')
                self.channel.queue.bind(queue='homed_queue', exchange='homedaemon', routing_key=f"homedaemon.{self.config['homed']['homeid']}.in")
                self.channel.basic.consume(queue='homed_queue', callback=self.on_message, no_ack=True)
                self.connected = True
                self.publish_msg({"cmd": "connect", "homeid": self.config['homed']['homeid']}, routing_key='homedaemon.main')
                self.bus.emit('info.rabbitmq.status.online')
                self.loop.create_task(self.ping())
            except (ConnectionRefusedError, amqpstorm.exception.AMQPConnectionError) as err:
                self.connected = False
                self.bus.emit('info.rabbitmq.status.offline')
                print(err)
                sleep(10)
    
    async def ping(self, interval: int = 5):
        while True:
            if self.connected:
                self.publish_msg({"cmd": "ping", "homeid": self.config['homed']['homeid']}, routing_key='homedaemon.main')
                await asyncio.sleep(interval)
    
    def on_message(self, msg:Any) -> None:
        try:
            _msg = json.loads(msg.body)
            if event := _msg.get('event'):
                args = _msg.get('args')
                print(args)
                if args[1] is None:
                    self.bus.emit(event, (args[0],))
                else:
                    self.bus.emit(event, args)
                    
        except json.JSONDecodeError as err:
            print(f'json {err} : {msg}')
        #     return
        
    def publish_msg(self, msg_data:Any, routing_key:str ='') -> None:
        if not routing_key:
            routing_key = f"homedaemon.{self.config['homed']['homeid']}.reports"
            
        if self.connected:
            properties = {'content_type': 'text/plain',
                          'expiration': '3600',}
            
            try:
                txt_msg = json.dumps(msg_data)
            except json.JSONDecodeError as err:
                print(f'json {err} : {msg_data}')
                return
            
            message: amqpstorm.Message = amqpstorm.Message.create(self.channel, txt_msg, properties)
            message.publish(exchange='homedaemon', routing_key=routing_key)
            
    def run(self) -> None:
        self.connect()
        while True:
            try:
                self.channel.start_consuming()
            except amqpstorm.AMQPConnectionError:
                self.connected = False
                self.connect()
            except OSError:
                self.connected = False
                self.connect()

    

