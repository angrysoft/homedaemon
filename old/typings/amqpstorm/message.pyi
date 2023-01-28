"""
This type stub file was generated by pyright.
"""

from amqpstorm.base import BaseMessage

"""AMQPStorm Message."""
class Message(BaseMessage):
    """RabbitMQ Message.

    e.g.
    ::

        # Message Properties.
        properties = {
            'content_type': 'text/plain',
            'expiration': '3600',
            'headers': {'key': 'value'},
        }
        # Create a new message.
        message = Message.create(channel, 'Hello RabbitMQ!', properties)
        # Publish the message to a queue called, 'my_queue'.
        message.publish('my_queue')

    :param Channel channel: AMQPStorm Channel
    :param bytes,str,unicode body: Message payload
    :param dict method: Message method
    :param dict properties: Message properties
    :param bool auto_decode: Auto-decode strings when possible. Does not
                             apply to to_dict, or to_tuple.
    """
    __slots__ = ...
    def __init__(self, channel, body=..., method=..., properties=..., auto_decode=...) -> None:
        ...
    
    @staticmethod
    def create(channel, body, properties=...): # -> Message:
        """Create a new Message.

        :param Channel channel: AMQPStorm Channel
        :param bytes,str,unicode body: Message payload
        :param dict properties: Message properties

        :rtype: Message
        """
        ...
    
    @property
    def body(self): # -> bytes | str:
        """Return the Message Body.

            If auto_decode is enabled, the body will automatically be
            decoded using decode('utf-8') if possible.

        :rtype: bytes,str,unicode
        """
        ...
    
    @property
    def channel(self):
        """Return the Channel used by this message.

        :rtype: Channel
        """
        ...
    
    @property
    def method(self): # -> dict[Unknown, Unknown] | bytes | str:
        """Return the Message Method.

            If auto_decode is enabled, all strings will automatically be
            decoded using decode('utf-8') if possible.

        :rtype: dict
        """
        ...
    
    @property
    def properties(self): # -> dict[Unknown, Unknown] | bytes | str:
        """Returns the Message Properties.

            If auto_decode is enabled, all strings will automatically be
            decoded using decode('utf-8') if possible.

        :rtype: dict
        """
        ...
    
    def ack(self): # -> None:
        """Acknowledge Message.

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :return:
        """
        ...
    
    def nack(self, requeue=...): # -> None:
        """Negative Acknowledgement.

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :param bool requeue: Re-queue the message
        """
        ...
    
    def reject(self, requeue=...): # -> None:
        """Reject Message.

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :param bool requeue: Re-queue the message
        """
        ...
    
    def publish(self, routing_key, exchange=..., mandatory=..., immediate=...):
        """Publish Message.

        :param str routing_key: Message routing key
        :param str exchange: The exchange to publish the message to
        :param bool mandatory: Requires the message is published
        :param bool immediate: Request immediate delivery

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: bool,None
        """
        ...
    
    @property
    def app_id(self): # -> None:
        """Get AMQP Message attribute: app_id.

        :return:
        """
        ...
    
    @app_id.setter
    def app_id(self, value): # -> None:
        """Set AMQP Message attribute: app_id.

        :return:
        """
        ...
    
    @property
    def message_id(self): # -> None:
        """Get AMQP Message attribute: message_id.

        :return:
        """
        ...
    
    @message_id.setter
    def message_id(self, value): # -> None:
        """Set AMQP Message attribute: message_id.

        :return:
        """
        ...
    
    @property
    def content_encoding(self): # -> None:
        """Get AMQP Message attribute: content_encoding.

        :return:
        """
        ...
    
    @content_encoding.setter
    def content_encoding(self, value): # -> None:
        """Set AMQP Message attribute: content_encoding.

        :return:
        """
        ...
    
    @property
    def content_type(self): # -> None:
        """Get AMQP Message attribute: content_type.

        :return:
        """
        ...
    
    @content_type.setter
    def content_type(self, value): # -> None:
        """Set AMQP Message attribute: content_type.

        :return:
        """
        ...
    
    @property
    def correlation_id(self): # -> None:
        """Get AMQP Message attribute: correlation_id.

        :return:
        """
        ...
    
    @correlation_id.setter
    def correlation_id(self, value): # -> None:
        """Set AMQP Message attribute: correlation_id.

        :return:
        """
        ...
    
    @property
    def delivery_mode(self): # -> None:
        """Get AMQP Message attribute: delivery_mode.

        :return:
        """
        ...
    
    @delivery_mode.setter
    def delivery_mode(self, value): # -> None:
        """Set AMQP Message attribute: delivery_mode.

        :return:
        """
        ...
    
    @property
    def timestamp(self): # -> None:
        """Get AMQP Message attribute: timestamp.

        :return:
        """
        ...
    
    @timestamp.setter
    def timestamp(self, value): # -> None:
        """Set AMQP Message attribute: timestamp.

        :return:
        """
        ...
    
    @property
    def priority(self): # -> None:
        """Get AMQP Message attribute: priority.

        :return:
        """
        ...
    
    @priority.setter
    def priority(self, value): # -> None:
        """Set AMQP Message attribute: priority.

        :return:
        """
        ...
    
    @property
    def reply_to(self): # -> None:
        """Get AMQP Message attribute: reply_to.

        :return:
        """
        ...
    
    @reply_to.setter
    def reply_to(self, value): # -> None:
        """Set AMQP Message attribute: reply_to.

        :return:
        """
        ...
    
    @property
    def message_type(self): # -> None:
        """Get AMQP Message attribute: message_type.

        :return:
        """
        ...
    
    @message_type.setter
    def message_type(self, value): # -> None:
        """Set AMQP Message attribute: message_type.

        :return:
        """
        ...
    
    @property
    def expiration(self): # -> None:
        """Get AMQP Message attribute: expiration.

        :return:
        """
        ...
    
    @expiration.setter
    def expiration(self, value): # -> None:
        """Set AMQP Message attribute: expiration.

        :return:
        """
        ...
    
    @property
    def user_id(self): # -> None:
        """Get AMQP Message attribute: user_id.

        :return:
        """
        ...
    
    @user_id.setter
    def user_id(self, value): # -> None:
        """Set AMQP Message attribute: user_id.

        :return:
        """
        ...
    
    @property
    def redelivered(self): # -> None:
        """Indicates if this message may have been delivered before (but not
        acknowledged).

        :rtype: bool,None
        """
        ...
    
    @property
    def delivery_tag(self): # -> None:
        """Server-assigned delivery tag.

        :rtype: int,None
        """
        ...
    
    def json(self): # -> Any:
        """Deserialize the message body, if it is JSON.

        :return:
        """
        ...
    


