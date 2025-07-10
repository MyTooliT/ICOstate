.. currentmodule:: icostate

***
API
***

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

System
######

.. autoclass:: ICOsystem
   :members:
