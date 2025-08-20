"""Configuration for pytest"""

# -- Imports ------------------------------------------------------------------

from icotronic.can import Connection
from pytest import fixture

from icostate.system import ICOsystem

# -- Fixtures -----------------------------------------------------------------

# pylint: disable=redefined-outer-name


@fixture(scope="session")
def sensor_node_name():
    """Returns the name of the sensor node used for the test"""

    return "Test-STH"


@fixture(scope="session")
async def sensor_node_mac_address(sensor_node_name):
    """Return the MAC address of the sensor node used for the test"""

    async with Connection() as stu:
        async with stu.connect_sensor_node(sensor_node_name) as sensor_node:
            return await sensor_node.get_mac_address()


@fixture
async def connect_stu():
    """Connect to and disconnect from STU"""
    icosystem = ICOsystem()

    await icosystem.connect_stu()
    yield icosystem
    await icosystem.disconnect_stu()
