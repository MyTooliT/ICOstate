"""Tests code for ICOsystem class"""

# -- Imports ------------------------------------------------------------------

from asyncio import sleep
from math import isclose
from statistics import mean
from time import monotonic

from icotronic.can.adc import ADCConfiguration
from icotronic.can import StreamingConfiguration
from netaddr import EUI
from pytest import mark

from icostate.measurement import MeasurementData
from icostate.system import ICOsystem

# -- Functions ----------------------------------------------------------------


@mark.asyncio
async def test_connect(sensor_node_mac_address, sensor_node_name):
    """Test sensor connection"""

    icosystem = ICOsystem()
    name_event_triggered = False
    mac_address_event_triggered = False

    @icosystem.on("sensor_node_name")
    async def name_changed(name: str):
        assert isinstance(name, str)
        assert name == sensor_node_name
        nonlocal name_event_triggered
        name_event_triggered = True

    @icosystem.on("sensor_node_mac_address")
    async def mac_address_changed(mac_address: EUI):
        assert isinstance(mac_address, EUI)
        assert mac_address == sensor_node_mac_address
        nonlocal mac_address_event_triggered
        mac_address_event_triggered = True

    await icosystem.connect_stu()
    await icosystem.connect_sensor_node_mac(sensor_node_mac_address)
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert name_event_triggered is True
    assert mac_address_event_triggered is True
    await icosystem.disconnect_sensor_node()
    await icosystem.disconnect_stu()


@mark.asyncio
async def test_rename_disconnected(
    connect_stu, sensor_node_mac_address, sensor_node_name
):
    """Test sensor renaming"""

    icosystem = connect_stu
    name_event_triggered = 0
    mac_address = str(sensor_node_mac_address)
    current_sensor_name = None

    @icosystem.on("sensor_node_name")
    async def name_changed(name: str):
        nonlocal current_sensor_name
        nonlocal name_event_triggered

        assert isinstance(name, str)
        assert len(name) <= 8
        current_sensor_name = name
        name_event_triggered += 1

    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert name_event_triggered == 0
    name_between = "ReNaMeD"

    await icosystem.rename(name_between, mac_address)
    await sleep(0)  # Allow scheduler to trigger event coroutines
    # Triggered twice, since rename coroutine sets name when it connects to
    # sensor node before renaming
    assert name_event_triggered == 2
    assert current_sensor_name == name_between

    await icosystem.rename(sensor_node_name, mac_address)
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert name_event_triggered == 4
    assert current_sensor_name == sensor_node_name


@mark.asyncio
async def test_adc_get(connect_sensor_node):
    """Test ADC get coroutine"""

    icosystem = connect_sensor_node
    adc_event_triggered = False

    @icosystem.on("sensor_node_adc_configuration")
    async def adc_config_changed(adc_configuration: ADCConfiguration):
        assert isinstance(adc_configuration, ADCConfiguration)
        nonlocal adc_event_triggered
        adc_event_triggered = True

    await icosystem.get_adc_configuration()
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert adc_event_triggered is True


@mark.asyncio
async def test_adc_set(connect_sensor_node):
    """Test ADC set coroutine"""

    icosystem = connect_sensor_node
    adc_event_triggered = 0

    @icosystem.on("sensor_node_adc_configuration")
    async def adc_config_changed(adc_configuration: ADCConfiguration):
        assert isinstance(adc_configuration, ADCConfiguration)
        nonlocal adc_event_triggered
        adc_event_triggered += 1

    # Set non-default ADC configuration
    non_default_adc_config = ADCConfiguration(
        prescaler=2, acquisition_time=8, oversampling_rate=64
    )
    await icosystem.set_adc_configuration(non_default_adc_config)
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert adc_event_triggered == 1
    adc_config = await icosystem.get_adc_configuration()
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert adc_event_triggered == 2
    assert adc_config == non_default_adc_config

    # Set default ADC configuration
    default_adc_config = ADCConfiguration(
        prescaler=2, acquisition_time=8, oversampling_rate=64
    )
    await icosystem.set_adc_configuration(default_adc_config)
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert adc_event_triggered == 3
    adc_config = await icosystem.get_adc_configuration()
    await sleep(0)  # Allow scheduler to trigger event coroutines
    assert adc_event_triggered == 4
    assert adc_config == default_adc_config


@mark.asyncio
async def test_measurement(connect_sensor_node):
    """Test measurement coroutines"""

    icosystem = connect_sensor_node
    collected_data: list[float] = []
    start = None

    @icosystem.on("sensor_node_measurement_data")
    async def measurement_data_changed(measurement_data: MeasurementData):
        nonlocal start
        if start is None:
            start = monotonic()
        assert isinstance(measurement_data, MeasurementData)
        collected_data.extend(measurement_data.first().values)

    streaming_configuration = StreamingConfiguration(
        first=True, second=False, third=False
    )
    sample_rate = (await icosystem.get_adc_configuration()).sample_rate()
    await icosystem.start_measurement(streaming_configuration)
    while len(collected_data) < sample_rate:
        await sleep(0.01)
    assert isinstance(start, float)
    collection_time = monotonic() - start

    assert 0.9 <= collection_time <= 1.3

    await icosystem.stop_measurement()
    assert len(collected_data) >= sample_rate
    average = mean(collected_data)
    approx_zero_g_absolute = 2**15
    approx_four_g_relative_100g_sensor = 4 * 2**16 / 200
    assert isclose(
        average,
        approx_zero_g_absolute,
        rel_tol=approx_four_g_relative_100g_sensor,
    )
