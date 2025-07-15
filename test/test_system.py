"""Tests code for ICOsystem class"""

# -- Imports ------------------------------------------------------------------

from asyncio import sleep

from unittest import IsolatedAsyncioTestCase, main

from icostate.system import ICOsystem

# -- Classes ------------------------------------------------------------------


class TestSystem(IsolatedAsyncioTestCase):
    """Collected tests for ICOsystem class"""

    async def test_connect(self):
        """Test sensor connection"""

        icosystem = ICOsystem()
        event_triggered = False

        @icosystem.on("sensor_node_attributes")
        async def do_something(data):  # pylint: disable=unused-argument
            nonlocal event_triggered
            event_triggered = True

        await icosystem.connect_stu()
        await icosystem.connect_sensor_node_mac("08-6B-D7-01-DE-81")
        await sleep(0)  # Allow scheduler to trigger event coroutine
        self.assertTrue(event_triggered)
        await icosystem.disconnect_sensor_node()
        await icosystem.disconnect_stu()


if __name__ == "__main__":
    main()
