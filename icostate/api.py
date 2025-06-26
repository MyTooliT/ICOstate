"""Application Programming Interface for stateful access to ICOtronic system"""

# pylint: disable=too-few-public-methods

# -- Imports ------------------------------------------------------------------

from icotronic.can import Connection

# -- Classes ------------------------------------------------------------------


class ICOSystem:
    """Stateful access to ICOtronic system"""

    def __init__(self):
        self.connection = Connection()
