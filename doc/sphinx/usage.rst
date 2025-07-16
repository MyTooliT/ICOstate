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

       disconnected --> stu_connected: connect_stu

       stu_connected --> disconnected: disconnect_stu
       stu_connected --> stu_connected: enable_ota, collect_sensor_nodes, rename, reset
       stu_connected --> sensor_node_connected: connect_sensor_node_mac

       sensor_node_connected --> sensor_node_connected: rename
       sensor_node_connected --> stu_connected: disconnect_sensor_node

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
