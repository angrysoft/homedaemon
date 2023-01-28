"""
This type stub file was generated by pyright.
"""

"""AMQPStorm Base."""
AUTH_MECHANISM = ...
IDLE_WAIT = ...
LOCALE = ...
MAX_FRAME_SIZE = ...
MAX_CHANNELS = ...
class Stateful:
    """Stateful implementation."""
    CLOSED = ...
    CLOSING = ...
    OPENING = ...
    OPEN = ...
    def __init__(self) -> None:
        ...
    
    @property
    def lock(self): # -> Lock:
        """Threading lock.

        :return:
        """
        ...
    
    def set_state(self, state): # -> None:
        """Set State.

        :param int state:
        :return:
        """
        ...
    
    @property
    def current_state(self): # -> Literal[0]:
        """Get the State.

        :rtype: int
        """
        ...
    
    @property
    def is_closed(self): # -> bool:
        """Is Closed?

        :rtype: bool
        """
        ...
    
    @property
    def is_closing(self): # -> bool:
        """Is Closing?

        :rtype: bool
        """
        ...
    
    @property
    def is_opening(self): # -> bool:
        """Is Opening?

        :rtype: bool
        """
        ...
    
    @property
    def is_open(self): # -> bool:
        """Is Open?

        :rtype: bool
        """
        ...
    
    @property
    def exceptions(self): # -> list[Unknown]:
        """Stores all exceptions thrown by this instance.

            This is useful for troubleshooting, and is used internally
            to check the health of the connection.

        :rtype: list
        """
        ...
    


class BaseChannel(Stateful):
    """Channel base class."""
    __slots__ = ...
    def __init__(self, channel_id) -> None:
        ...
    
    @property
    def channel_id(self):
        """Get Channel id.

        :rtype: int
        """
        ...
    
    @property
    def consumer_tags(self): # -> list[Unknown]:
        """Get a list of consumer tags.

        :rtype: list
        """
        ...
    
    def add_consumer_tag(self, tag): # -> None:
        """Add a Consumer tag.

        :param str tag: Consumer tag.
        :return:
        """
        ...
    
    def remove_consumer_tag(self, tag=...): # -> None:
        """Remove a Consumer tag.

            If no tag is specified, all all tags will be removed.

        :param str,None tag: Consumer tag.
        :return:
        """
        ...
    


class BaseMessage:
    """Message base class.

    :param Channel channel: AMQPStorm Channel
    :param str,unicode body: Message body
    :param dict method: Message method
    :param dict properties: Message properties
    :param bool auto_decode: This is not implemented in the base message class.
    """
    __slots__ = ...
    def __init__(self, channel, body=..., method=..., properties=..., auto_decode=...) -> None:
        ...
    
    def __iter__(self): # -> Generator[tuple[str, Any], None, None]:
        ...
    
    def to_dict(self): # -> dict[str, Unknown | dict[Any, Any]]:
        """Message to Dictionary.

        :rtype: dict
        """
        ...
    
    def to_tuple(self): # -> tuple[Unknown, Unknown, Unknown, Unknown | dict[Any, Any]]:
        """Message to Tuple.

        :rtype: tuple
        """
        ...
    


class Handler:
    """Operations Handler (e.g. Queue, Exchange)"""
    __slots__ = ...
    def __init__(self, channel) -> None:
        ...
    


