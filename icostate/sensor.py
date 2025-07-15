"""Support code for sensor nodes"""

# -- Imports ------------------------------------------------------------------

from netaddr import EUI

# -- Classes ------------------------------------------------------------------

# pylint: disable=too-few-public-methods


class SensorNodeAttributes:
    """Store information about a sensor node

    Args:

        name:

            The Bluetooth advertisement name of the sensor node

        mac_address:

            The MAC address of the sensor node

    """

    def __init__(
        self, name: str | None = None, mac_address: EUI | None = None
    ) -> None:
        self.name: str | None = name
        self.mac_address: EUI | None = mac_address

    def __repr__(self) -> str:
        """Get the textual representation of the sensor node

        Returns:

            A string containing information about the sensor node attributes

        Examples:

            Get representation of a sensor node with defined name & MAC address

            >>> SensorNodeAttributes(name="hello",
            ...                      mac_address=EUI("12-34-56-78-90-AB"))
            Name: hello, MAC Address: 12-34-56-78-90-AB

            Get representation of a sensor node with defined name

            >>> SensorNodeAttributes(name="hello")
            Name: hello, MAC Address: Undefined

        """

        def attribute_or_undefined(attribute):
            return f"{attribute}" if attribute is not None else "Undefined"

        return ", ".join([
            f"Name: {attribute_or_undefined(self.name)}",
            f"MAC Address: {attribute_or_undefined(self.mac_address)}",
        ])


# pylint: enable=too-few-public-methods

# -- Main ---------------------------------------------------------------------

if __name__ == "__main__":
    from doctest import testmod

    testmod()
