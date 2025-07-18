"""Tests code for ICOsystem class"""

# -- Imports ------------------------------------------------------------------

from asyncio import sleep

from pytest import mark

from icostate.system import ICOsystem

# -- Globals ------------------------------------------------------------------

MAC_ADDRESS = "08-6B-D7-01-DE-81"
NAME = "Test-STH"

# -- Functions ----------------------------------------------------------------


@mark.asyncio
async def test_connect():
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
    await icosystem.connect_sensor_node_mac(MAC_ADDRESS)
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert name_event_triggered is True
    assert mac_address_event_triggered is True
    await icosystem.disconnect_sensor_node()
    await icosystem.disconnect_stu()


@mark.asyncio
async def test_rename():
    """Test sensor renaming"""

    icosystem = ICOsystem()
    name_event_triggered = False

    @icosystem.on("sensor_node_name")
    async def name_changed(data):  # pylint: disable=unused-argument
        nonlocal name_event_triggered
        name_event_triggered = True

    await icosystem.connect_stu()
    await icosystem.rename(NAME, MAC_ADDRESS)
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert name_event_triggered is True
    await icosystem.disconnect_stu()
