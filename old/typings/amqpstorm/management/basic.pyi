"""
This type stub file was generated by pyright.
"""

from amqpstorm.management.base import ManagementHandler

API_BASIC_PUBLISH = ...
API_BASIC_GET_MESSAGE = ...
class Basic(ManagementHandler):
    def publish(self, body, routing_key, exchange=..., virtual_host=..., properties=..., payload_encoding=...):
        """Publish a Message.

        :param bytes,str,unicode body: Message payload
        :param str routing_key: Message routing key
        :param str exchange: The exchange to publish the message to
        :param str virtual_host: Virtual host name
        :param dict properties: Message properties
        :param str payload_encoding: Payload encoding.

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        ...
    
    def get(self, queue, virtual_host=..., requeue=..., to_dict=..., count=..., truncate=..., encoding=...): # -> list[Unknown]:
        """Get Messages.

        :param str queue: Queue name
        :param str virtual_host: Virtual host name
        :param bool requeue: Re-queue message
        :param bool to_dict: Should incoming messages be converted to a
                             dictionary before delivery.
        :param int count: How many messages should we try to fetch.
        :param int truncate: The maximum length in bytes, beyond that the
                             server will truncate the message.
        :param str encoding: Message encoding.

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: list
        """
        ...
    


