"""
This type stub file was generated by pyright.
"""

"""AMQPStorm Rpc."""
class Rpc:
    """Internal RPC handler.

    :param object default_adapter: Connection or Channel.
    :param int,float timeout: Rpc timeout.
    """
    def __init__(self, default_adapter, timeout=...) -> None:
        ...
    
    @property
    def lock(self): # -> Lock:
        ...
    
    def on_frame(self, frame_in): # -> bool:
        """On RPC Frame.

        :param specification.Frame frame_in: Amqp frame.
        :return:
        """
        ...
    
    def register_request(self, valid_responses): # -> str:
        """Register a RPC request.

        :param list valid_responses: List of possible Responses that
                                     we should be waiting for.
        :return:
        """
        ...
    
    def remove(self, uuid): # -> None:
        """Remove any data related to a specific RPC request.

        :param str uuid: Rpc Identifier.
        :return:
        """
        ...
    
    def remove_request(self, uuid): # -> None:
        """Remove any RPC request(s) using this uuid.

        :param str uuid: Rpc Identifier.
        :return:
        """
        ...
    
    def remove_response(self, uuid): # -> None:
        """Remove a RPC Response using this uuid.

        :param str uuid: Rpc Identifier.
        :return:
        """
        ...
    
    def get_request(self, uuid, raw=..., multiple=..., connection_adapter=...): # -> dict[Unknown, Unknown] | None:
        """Get a RPC request.

        :param str uuid: Rpc Identifier
        :param bool raw: If enabled return the frame as is, else return
                         result as a dictionary.
        :param bool multiple: Are we expecting multiple frames.
        :param obj connection_adapter: Provide custom connection adapter.
        :return:
        """
        ...
    


