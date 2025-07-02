.. currentmodule:: icostate

***
API
***

State Diagram
#############

.. mermaid::

   stateDiagram-v2
       stu_connected: STU Connected
       disconnected: Disconnected

       disconnected --> stu_connected: connect_stu
       stu_connected --> disconnected: disconnect_stu
       stu_connected --> stu_connected: enable_ota, reset

System
######

.. autoclass:: ICOsystem
   :members:
