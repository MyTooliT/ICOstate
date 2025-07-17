"""Support code for sensor nodes"""

# -- Imports ------------------------------------------------------------------

from netaddr import EUI

from icotronic.can.adc import ADCConfiguration

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
        self,
        name: str | None = None,
        mac_address: EUI | None = None,
        adc_configuration: ADCConfiguration | None = None,
    ) -> None:
        self.name: str | None = name
        self.mac_address: EUI | None = mac_address
        self.adc_configuration: ADCConfiguration | None = adc_configuration

    def __repr__(self) -> str:
        """Get the textual representation of the sensor node

        Returns:

            A string containing information about the sensor node attributes

        Examples:

            Get representation sensor node with all attributes defined


            >>> config = ADCConfiguration(prescaler=2,
            ...                           acquisition_time=8,
            ...                           oversampling_rate=64)
            >>> SensorNodeAttributes(name="hello",
            ...                      mac_address=EUI("12-34-56-78-90-AB"),
            ...                      adc_configuration=config
            ...                     ) # doctest:+NORMALIZE_WHITESPACE
            Name: hello,
            MAC Address: 12-34-56-78-90-AB,
            ADC Configuration: [Prescaler: 2,
                                Acquisition Time: 8,
                                Oversampling Rate: 64,
                                Reference Voltage: 3.3 V]

            Get representation of a sensor node with defined name

            >>> SensorNodeAttributes(name="hello"
            ...                     ) # doctest:+NORMALIZE_WHITESPACE
            Name: hello,
            MAC Address: Undefined,
            ADC Configuration: Undefined

        """

        def attribute_or_undefined(attribute, brackets: bool = False) -> str:
            if attribute is None:
                return "Undefined"

            return f"[{attribute}]" if brackets else str(attribute)

        return ", ".join([
            f"Name: {attribute_or_undefined(self.name)}",
            f"MAC Address: {attribute_or_undefined(self.mac_address)}",
            (
                "ADC Configuration: "
                f"{attribute_or_undefined(self.adc_configuration, True)}"
            ),
        ])


# pylint: enable=too-few-public-methods

# -- Main ---------------------------------------------------------------------

if __name__ == "__main__":
    from doctest import testmod

    testmod()
