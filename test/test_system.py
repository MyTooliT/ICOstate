"""Tests code for ICOsystem class"""

# -- Imports ------------------------------------------------------------------

from asyncio import sleep

from icotronic.can.adc import ADCConfiguration
from netaddr import EUI
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
    async def name_changed(name: str):
        assert isinstance(name, str)
        nonlocal name_event_triggered
        name_event_triggered = True

    @icosystem.on("sensor_node_mac_address")
    async def mac_address_changed(mac_address: EUI):
        assert isinstance(mac_address, EUI)
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
    async def name_changed(name: str):
        assert isinstance(name, str)
        nonlocal name_event_triggered
        name_event_triggered = True

    await icosystem.connect_stu()
    await icosystem.rename(NAME, MAC_ADDRESS)
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert name_event_triggered is True
    await icosystem.disconnect_stu()


@mark.asyncio
async def test_adc_get():
    """Test ADC get coroutine"""

    icosystem = ICOsystem()
    adc_event_triggered = False

    @icosystem.on("sensor_node_adc_configuration")
    async def adc_config_changed(adc_configuration: ADCConfiguration):
        assert isinstance(adc_configuration, ADCConfiguration)
        nonlocal adc_event_triggered
        adc_event_triggered = True

    await icosystem.connect_stu()
    await icosystem.connect_sensor_node_mac(MAC_ADDRESS)
    await icosystem.get_adc_configuration()
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert adc_event_triggered is True
    await icosystem.disconnect_sensor_node()
    await icosystem.disconnect_stu()


@mark.asyncio
async def test_adc_set():
    """Test ADC set coroutine"""

    icosystem = ICOsystem()
    adc_event_triggered = 0

    @icosystem.on("sensor_node_adc_configuration")
    async def adc_config_changed(adc_configuration: ADCConfiguration):
        assert isinstance(adc_configuration, ADCConfiguration)
        nonlocal adc_event_triggered
        adc_event_triggered += 1

    # Connect
    await icosystem.connect_stu()
    await icosystem.connect_sensor_node_mac(MAC_ADDRESS)
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert adc_event_triggered == 1

    # Set non-default ADC configuration
    non_default_adc_config = ADCConfiguration(
        prescaler=2, acquisition_time=8, oversampling_rate=64
    )
    await icosystem.set_adc_configuration(non_default_adc_config)
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert adc_event_triggered == 2
    adc_config = await icosystem.get_adc_configuration()
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert adc_event_triggered == 3
    assert adc_config == non_default_adc_config

    # Set default ADC configuration
    default_adc_config = ADCConfiguration(
        prescaler=2, acquisition_time=8, oversampling_rate=64
    )
    await icosystem.set_adc_configuration(default_adc_config)
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert adc_event_triggered == 4
    adc_config = await icosystem.get_adc_configuration()
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert adc_event_triggered == 5
    assert adc_config == default_adc_config

    # Disconnect
    await icosystem.disconnect_sensor_node()
    await icosystem.disconnect_stu()
