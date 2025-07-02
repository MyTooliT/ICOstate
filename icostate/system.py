"""Application Programming Interface for stateful access to ICOtronic system"""

# pylint: disable=too-few-public-methods

# -- Imports ------------------------------------------------------------------

from asyncio import sleep

from icotronic.can import Connection, NoResponseError, STU
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

    async def connect_stu(self) -> bool:
        """Connect to STU

        Returns:

            - ``True``, if everything worked as expected or
            - ``False``, if there was no response from the STU

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

        self._check_state({State.DISCONNECTED}, "Connecting to STU")

        try:
            # pylint: disable=unnecessary-dunder-call
            self.stu = await self.connection.__aenter__()
            # pylint: enable=unnecessary-dunder-call
            self.state = State.STU_CONNECTED
            assert isinstance(self.stu, STU)
            return True
        except NoResponseError:
            return False

    async def disconnect_stu(self) -> bool:
        """Disconnect from STU

        Returns:

            - ``True``, if everything worked as expected or
            - ``False``, if there was no response from the STU

        """

        self._check_state({State.STU_CONNECTED}, "Disconnecting from STU")

        try:
            await self.connection.__aexit__(None, None, None)
            self.state = State.DISCONNECTED
            self.stu = None
            return True
        except NoResponseError:
            return False

    async def reset_stu(self) -> bool:
        """Reset STU

        Returns:

            - ``True``, if everything worked as expected or
            - ``False``, if there was no response from the STU

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

        try:

            await self.stu.reset()

            # Make sure that the STU is in the correct state after the reset,
            # although this seems to be the case anyway. At least in my limited
            # tests the STU was always in the “operating state” even directly
            # after the reset.
            operating = NodeState(location="Application", state="Operating")
            while (state := await self.stu.get_state()) != operating:
                await sleep(1)
        except NoResponseError:
            return False

        assert state == operating
        return True

    async def enable_ota(self) -> bool:
        """Enable OTA (Over The Air) update mode

        Returns:

            - ``True``, if everything worked as expected or
            - ``False``, if there was no response from the STU

        Examples:

            Import necessary code

            >>> from asyncio import run

            Enable OTA update mode

            >>> async def enable_ota(icosystem: ICOsystem):
            ...     await icosystem.connect_stu()
            ...     await icosystem.enable_ota()
            ...     await icosystem.disconnect_stu()
            >>> run(enable_ota(ICOsystem()))

        """

        self._check_state({State.STU_CONNECTED}, "Enabling OTA mode")

        assert isinstance(self.stu, STU)

        try:
            # The coroutine below activates the advertisement required for the
            # Over The Air (OTA) firmware update. Please take a look at
            #
            # - https://github.com/MyTooliT/ICOtronic/blob/aaf9f380bccb0039e31faaefd09b13830d7ebe1c/icotronic/scripts/icon.py#L327-L338
            #
            # for more information
            await self.stu.activate_bluetooth()
            return True
        except NoResponseError:
            return False


if __name__ == "__main__":
    from doctest import testmod

    testmod()
