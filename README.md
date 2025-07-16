<h1 align="center" style="font-weight: bold;">Mosquitto Railway Template</h1>

<div align="center">

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/QFTCTq?referralCode=ePU7HL)

</div>

<h2 id="info">📝 Info</h2>

Mosquitto is an open source (EPL/EDL licensed) message broker that implements the MQTT protocol versions 5.0, 3.1.1 and 3.1. Mosquitto is **lightweight** and is suitable for use on all devices from low power single board computers to full servers.

An MQTT message broker is a central component that enables communication between clients and IoT devices using the MQTT protocol. It follows the publish-subscribe (pub/sub) messaging model, which plays a crucial role in managing MQTT connections and performing data transmission.

The broker receives messages from publishers, verifies their publishing rights, and queues messages according to their Quality of Service (QoS) levels. It further identifies authorised subscribers and routes them to appropriate subscribers.

Learn more about Mosquitto here: [Eclipse Mosquitto](https://mosquitto.org)

<h2 id="env">🔐 Variables</h2>

- `MOSQUITTO_USERNAME`: Username used to publish and subscribe
- `MOSQUITTO_PASSWORD`: Password used to publish and subscribe
