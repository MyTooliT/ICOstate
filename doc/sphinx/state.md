# State Diagram

```{mermaid}
stateDiagram-v2
    stu_connected: STU Connected
    disconnected: Disconnected

    disconnected --> stu_connected: stu_connect
    stu_connected --> disconnect: disconnect_stu
```
