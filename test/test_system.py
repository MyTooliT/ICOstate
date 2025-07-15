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
        name_event_triggered = False
        mac_address_event_triggered = False

        @icosystem.on("sensor_node_name")
        async def name_changed(data):  # pylint: disable=unused-argument
            nonlocal name_event_triggered
            name_event_triggered = True

        @icosystem.on("sensor_node_mac_address")
        async def mac_address_changed(data):  # pylint: disable=unused-argument
            nonlocal mac_address_event_triggered
            mac_address_event_triggered = True

        await icosystem.connect_stu()
        await icosystem.connect_sensor_node_mac("08-6B-D7-01-DE-81")
        await sleep(0)  # Allow scheduler to trigger event coroutines
        self.assertTrue(name_event_triggered)
        self.assertTrue(mac_address_event_triggered)
        await icosystem.disconnect_sensor_node()
        await icosystem.disconnect_stu()


# -- Main ---------------------------------------------------------------------

if __name__ == "__main__":
    main()
