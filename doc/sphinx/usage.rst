*****
Usage
*****

.. currentmodule:: icostate

The main class for communication in the stateful API provided by this package is :class:`ICOsystem`. Depending on the `current state <#state-diagram>`_  of objects of this class you will be able to use different coroutines to interact with the system.

State Diagram
#############

.. mermaid::

   stateDiagram-v2
       disconnected: Disconnected
       stu_connected: STU Connected
       sensor_node_connected: Sensor Node Connected
       measurement: Measurement

       disconnected --> stu_connected: connect_stu

       stu_connected --> disconnected: disconnect_stu
       stu_connected --> stu_connected: collect_sensor_nodes, get_adc_configuration, rename, reset, set_adc_configuration
       stu_connected --> sensor_node_connected: connect_sensor_node_mac

       sensor_node_connected --> stu_connected: disconnect_sensor_node
       sensor_node_connected --> sensor_node_connected: get_adc_configuration, rename, set_adc_configuration
       sensor_node_connected --> measurement: start_measurement

       measurement --> sensor_node_connected: stop_measurement


In addition to coroutines that label the edges of the `state diagram <#state-diagram>`_ above you can also use the coroutine :meth:`ICOsystem.is_sensor_node_connected`, which works in any state.

STU
###

Connecting to STU
*****************

Before you work with the ICOtronic system you need to set up the CAN connection to the STU (Stationary Transceiver Unit), which you can do using the coroutine :meth:`ICOsystem.connect_stu`. After you are done working working with the STU you also need to disconnect the connection using the coroutine :meth:`ICOsystem.disconnect_stu`.

.. doctest::

   >>> from asyncio import run
   >>> from icostate import ICOsystem

   >>> async def connect_disconnect_stu(icosystem: ICOsystem):
   ...     await icosystem.connect_stu()
   ...     await icosystem.disconnect_stu()

   >>> run(connect_disconnect_stu(ICOsystem()))

Resetting STU
*************

In case you have the ICOtronic system does not react as you expect you can reset it using the coroutine :meth:`ICOsystem.reset_stu`.

.. doctest::

   >>> from asyncio import run
   >>> from icostate import ICOsystem

   >>> async def reset_stu(icosystem: ICOsystem):
   ...     await icosystem.connect_stu()
   ...     await icosystem.reset_stu()
   ...     await icosystem.disconnect_stu()

   >>> run(reset_stu(ICOsystem()))

Finding Available Sensor Nodes
******************************

To retrieve information about available sensor nodes use the coroutine :meth:`ICOsystem.collect_sensor_nodes`.

.. doctest::

   >>> from asyncio import run
   >>> from netaddr import EUI
   >>> from icostate import ICOsystem, SensorNodeInfo

   >>> async def get_sensor_nodes(icosystem: ICOsystem) -> list[SensorNodeInfo]:
   ...     await icosystem.connect_stu()
   ...     sensor_nodes = await icosystem.collect_sensor_nodes()
   ...     await icosystem.disconnect_stu()
   ...     return sensor_nodes

   >>> sensor_nodes = run(get_sensor_nodes(ICOsystem()))
   >>> # We assume that at least one sensor node is available
   >>> len(sensor_nodes) >= 1
   True
   >>> node_info = sensor_nodes[0]
   >>> # Each list entry contains information about name, MAC address and RSSI
   >>> isinstance(node_info.name, str)
   True
   >>> len(node_info.name) <= 8
   True
   >>> isinstance(node_info.mac_address, EUI)
   True
   >>> -80 < node_info.rssi < 0
   True

Sensor Node
###########

Connecting to Sensor Node
*************************

Before you start a measurement you need to connect to a sensor node. To do that use the coroutine :meth:`ICOsystem.connect_sensor_node_mac`. Please do not forget to disconnect from the node with the coroutine :meth:`ICOsystem.disconnect_sensor_node` afterwards.

.. doctest::

   >>> from asyncio import run
   >>> from icostate import ICOsystem

   >>> async def connect_disconnect_sensor_node(icosystem: ICOsystem,
   ...                                          mac_address: str):
   ...     await icosystem.connect_stu()
   ...     print(f"Connected: {await icosystem.is_sensor_node_connected()}")
   ...     await icosystem.connect_sensor_node_mac(mac_address)
   ...     print(f"Connected: {await icosystem.is_sensor_node_connected()}")
   ...     await icosystem.disconnect_sensor_node()
   ...     print(f"Connected: {await icosystem.is_sensor_node_connected()}")
   ...     await icosystem.disconnect_stu()

   >>> mac_address = (
   ...     "08-6B-D7-01-DE-81") # Change to MAC address of your sensor node
   >>> run(connect_disconnect_sensor_node(ICOsystem(), mac_address))
   Connected: False
   Connected: True
   Connected: False

Rename a Sensor Node
********************

To rename a sensor node use the coroutine :meth:`ICOsystem.rename`, which requires the new name of the sensor node as parameter. If the system is currently not connected to a sensor node, then the coroutine also requires the MAC address of the sensor node. After using the coroutine successfully the system will switch back to the state it was in before renaming the sensor node (either “STU Connected” or “Sensor Node Connected”).

.. doctest::

   >>> from asyncio import run
   >>> from icostate import ICOsystem

   >>> async def rename_disconnected(icosystem: ICOsystem,
   ...                               mac_address: str,
   ...                               new_name: str):
   ...     await icosystem.connect_stu()
   ...     print(f"State Before: {icosystem.state}")
   ...     await icosystem.rename(new_name, mac_address)
   ...     print(f"State After: {icosystem.state}")
   ...     await icosystem.disconnect_stu()

   >>> mac_address = (
   ...     "08-6B-D7-01-DE-81") # Change to MAC address of your sensor node
   >>> name = "Test-STH"
   >>> run(rename_disconnected(ICOsystem(), mac_address, name))
   State Before: STU Connected
   State After: STU Connected

Events
######

Objects of the :class:`ICOsystem` provides an event based API (based on `pyee`_) you can use to react to changes to the system. Currently the following events are supported:

- ``sensor_node_name``: Called when the name of the current sensor node changes
- ``sensor_node_mac_address``: Called when the MAC address of a sensor node changes
- ``sensor_node_adc_configuration``: Called when the ADC configuration of a sensor node is updated
- ``sensor_node_streaming_data``: Called when new streaming data is available

.. _pyee: https://pyee.readthedocs.io

The example below shows how you can react to changes of the sensor node name:

.. doctest::

   >>> from asyncio import sleep, run
   >>> from icostate import ICOsystem

   >>> async def react_sensor_node_name(icosystem: ICOsystem, mac_address: str):
   ...
   ...     @icosystem.on("sensor_node_name")
   ...     async def name_changed(name: str):
   ...         print(f"Name of sensor node: {name}")
   ...
   ...     await icosystem.connect_stu()
   ...     await icosystem.connect_sensor_node_mac(mac_address)
   ...     await sleep(0)  # Allow scheduler to trigger event coroutine
   ...     await icosystem.disconnect_sensor_node()
   ...     await icosystem.disconnect_stu()

   >>> mac_address = "08-6B-D7-01-DE-81"  # Change to MAC address of your
   >>>                                    # sensor node
   >>> run(react_sensor_node_name(ICOsystem(), mac_address))
   Name of sensor node: Test-STH
