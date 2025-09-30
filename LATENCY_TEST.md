# Mosquitto Latency Test

## Prerequisites

Install the Paho MQTT client:

```bash
pip install paho-mqtt
```

## Running the Test

```bash
python test_latency.py <username> <password>
```

Replace `<username>` and `<password>` with your Mosquitto credentials.

## What the Test Does

1. Connects to the broker at `mosquitto-railway.up.railway.app`
2. Sends 100 test messages to the `test/latency` topic
3. Measures round-trip time for each message
4. Calculates statistics including average, median, min, and max latency
5. Reports whether the average latency is below the 50ms target

## Configuration Optimizations

The following optimizations were made to reduce latency:

- **Persistence disabled**: Removes disk I/O overhead
- **Optimized message queues**: `max_queued_messages` and `max_inflight_messages` configured
- **Reduced logging**: Only errors and warnings are logged
- **Simplified configuration**: Removed unnecessary options that were causing errors