"""Application Programming Interface for stateful access to ICOtronic system"""

# pylint: disable=too-few-public-methods

# -- Imports ------------------------------------------------------------------

from icotronic.can import Connection, STU

from icostate.error import IncorrectStateError
from icostate.state import State

# -- Classes ------------------------------------------------------------------


class ICOsystem:
    """Stateful access to ICOtronic system"""

    def __init__(self):
        self.state = State.DISCONNECTED
        self.connection = Connection()
        self.stu: STU | None = None

    async def connect_stu(self) -> None:
        """Connect to STU

        Examples:

            Import necessary code

            >>> from asyncio import run

            Connect and disconnect from STU

            >>> async def connect_disconnect_stu(icotronic: ICOsystem):
            ...     states = [icotronic.state]
            ...     await icotronic.connect_stu()
            ...     states.append(icotronic.state)
            ...     await icotronic.disconnect_stu()
            ...     states.append(icotronic.state)
            ...     return states
            >>> run(connect_disconnect_stu(ICOsystem()))
            [Disconnected, STU Connected, Disconnected]

        """

        # Do not try to connect a second time, if already connected
        if self.stu is None:
            # pylint: disable=unnecessary-dunder-call
            self.stu = await self.connection.__aenter__()
            # pylint: enable=unnecessary-dunder-call
        self.state = State.STU_CONNECTED
        assert isinstance(self.stu, STU)

    async def disconnect_stu(self) -> None:
        """Disconnect from STU"""

        await self.connection.__aexit__(None, None, None)
        self.state = State.DISCONNECTED
        self.stu = None


if __name__ == "__main__":
    from doctest import testmod

    testmod()
