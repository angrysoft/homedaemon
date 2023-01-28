"""
This type stub file was generated by pyright.
"""

from amqpstorm.management.base import ManagementHandler

HEALTHCHECKS = ...
HEALTHCHECKS_NODE = ...
class HealthChecks(ManagementHandler):
    def get(self, node=...):
        """Run basic healthchecks against the current node, or against a given
        node.

            Example response:
                > {"status":"ok"}
                > {"status":"failed","reason":"string"}

        :param node: Node name

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        ...
    


