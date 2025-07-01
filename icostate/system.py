"""Application Programming Interface for stateful access to ICOtronic system"""

# pylint: disable=too-few-public-methods

# -- Imports ------------------------------------------------------------------

from asyncio import sleep

from icotronic.can import Connection, STU
from icotronic.can.status import State as NodeState

from icostate.error import IncorrectStateError
from icostate.state import State

# -- Classes ------------------------------------------------------------------


class ICOsystem:
    """Stateful access to ICOtronic system"""

    def __init__(self):
        self.state = State.DISCONNECTED
        self.connection = Connection()
        self.stu: STU | None = None

    def _check_state(self, states: set[State], description: str) -> None:
        """Check if the system is in an allowed state

        Args:

            states:
                The set of allowed states

            description:
                A description of the action that is only allowed in the states
                specified by ``states``

        Raises:

            IncorrectStateError:
                If the current state is not included in ``states``

        """

        if self.state not in states:
            plural = "" if len(states) <= 1 else "s"
            raise IncorrectStateError(
                f"{description} only allowed in the state{plural}: "
                f"{', '.join(map(repr, states))}"
            )

    async def connect_stu(self) -> None:
        """Connect to STU

        Examples:

            Import necessary code

            >>> from asyncio import run

            Connect and disconnect from STU

            >>> async def connect_disconnect_stu(icosystem: ICOsystem):
            ...     states = [icosystem.state]
            ...     await icosystem.connect_stu()
            ...     states.append(icosystem.state)
            ...     await icosystem.disconnect_stu()
            ...     states.append(icosystem.state)
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

    async def reset_stu(self) -> None:
        """Reset STU

        Examples:

            Import necessary code

            >>> from asyncio import run

            Reset a connected STU

            >>> async def reset_stu(icosystem: ICOsystem):
            ...     await icosystem.connect_stu()
            ...     await icosystem.reset_stu()
            ...     await icosystem.disconnect_stu()
            >>> run(reset_stu(ICOsystem()))

            Resetting the STU will not work if the STU is not connected

            >>> async def reset_stu_without_connection(icosystem: ICOsystem):
            ...     await icosystem.reset_stu()
            >>> run(reset_stu_without_connection(
            ...     ICOsystem())) # doctest:+NORMALIZE_WHITESPACE
            Traceback (most recent call last):
               ...
            icostate.error.IncorrectStateError: Resetting STU only allowed in
                                                the state: STU Connected

        """

        self._check_state({State.STU_CONNECTED}, "Resetting STU")

        assert isinstance(self.stu, STU)

        await self.stu.reset()

        # Make sure that the STU is in the correct state after the reset,
        # although this seems to be the case anyway. At least in my limited
        # tests the STU was always in the “operating state” even directly
        # after the reset.
        operating = NodeState(location="Application", state="Operating")
        while (state := await self.stu.get_state()) != operating:
            await sleep(1)

        assert state == operating


if __name__ == "__main__":
    from doctest import testmod

    testmod()
