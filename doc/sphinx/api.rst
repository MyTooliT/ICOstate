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

       disconnected --> stu_connected: stu_connect
       stu_connected --> disconnected: disconnect_stu

System
######

.. autoclass:: ICOsystem
   :members:
