"""
This type stub file was generated by pyright.
"""

from amqpstorm.base import Handler

"""AMQPStorm Channel.Exchange."""
LOGGER = ...
class Exchange(Handler):
    """RabbitMQ Exchange Operations."""
    __slots__ = ...
    def declare(self, exchange=..., exchange_type=..., passive=..., durable=..., auto_delete=..., arguments=...):
        """Declare an Exchange.

        :param str exchange: Exchange name
        :param str exchange_type: Exchange type
        :param bool passive: Do not create
        :param bool durable: Durable exchange
        :param bool auto_delete: Automatically delete when not in use
        :param dict arguments: Exchange key/value arguments

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: dict
        """
        ...
    
    def delete(self, exchange=..., if_unused=...):
        """Delete an Exchange.

        :param str exchange: Exchange name
        :param bool if_unused: Delete only if unused

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: dict
        """
        ...
    
    def bind(self, destination=..., source=..., routing_key=..., arguments=...):
        """Bind an Exchange.

        :param str destination: Exchange name
        :param str source: Exchange to bind to
        :param str routing_key: The routing key to use
        :param dict arguments: Bind key/value arguments

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: dict
        """
        ...
    
    def unbind(self, destination=..., source=..., routing_key=..., arguments=...):
        """Unbind an Exchange.

        :param str destination: Exchange name
        :param str source: Exchange to unbind from
        :param str routing_key: The routing key used
        :param dict arguments: Unbind key/value arguments

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: dict
        """
        ...
    


