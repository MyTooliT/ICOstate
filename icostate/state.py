"""Support code for determining the current state of the ICOtronic system"""

# -- Imports ------------------------------------------------------------------

from enum import auto, Enum

# -- Classes ------------------------------------------------------------------


class State(Enum):
    """Contains the various states the ICOtronic system can be in"""

    DISCONNECTED = auto()
    STU_CONNECTED = auto()
    SENSOR_NODE_CONNECTED = auto()

    def __repr__(self) -> str:
        """Get string representation of state

        Returns:

            A human readable unique representation of the state

        Examples:

            Show the string representation of some states

            >>> State.STU_CONNECTED
            STU Connected

            >>> State.DISCONNECTED
            Disconnected

        """

        return " ".join([
            word.upper() if word in {"STH", "STU"} else word.capitalize()
            for word in self.name.split("_")
        ])
