<h1 align="center" style="font-weight: bold;">Mosquitto Railway Template - Otimizado para Baixa Latência</h1>

<div align="center">

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/mosquitto-broker?referralCode=ePU7HL)

</div>

<h2 id="info">📝 Info</h2>

Mosquitto is an open source (EPL/EDL licensed) message broker that implements the MQTT protocol versions 5.0, 3.1.1 and 3.1. Mosquitto is **lightweight** and is suitable for use on all devices from low power single board computers to full servers.

An MQTT message broker is a central component that enables communication between clients and IoT devices using the MQTT protocol. It follows the publish-subscribe (pub/sub) messaging model, which plays a crucial role in managing MQTT connections and performing data transmission.

The broker receives messages from publishers, verifies their publishing rights, and queues messages according to their Quality of Service (QoS) levels. It further identifies authorized subscribers and routes them to appropriate subscribers.

Learn more about Mosquitto here: [Eclipse Mosquitto](https://mosquitto.org)

<h2 id="env">🔐 Variables</h2>

- `MOSQUITTO_USERNAME`: Username used to publish and subscribe
- `MOSQUITTO_PASSWORD`: Password used to publish and subscribe

<h2 id="performance">⚡ Otimizações de Performance</h2>

Esta versão foi otimizada para alcançar a menor latência possível:

- **TCP_NODELAY**: Desabilita o algoritmo de Nagle para reduzir delay
- **Sem Persistência**: Remove I/O de disco para máxima velocidade
- **QoS Máximo 1**: Reduz overhead de confirmações
- **Buffers Otimizados**: Melhora throughput de mensagens
- **Logging Mínimo**: Apenas erros e avisos para reduzir processamento
- **Alpine Linux**: Imagem menor e mais rápida

<h2 id="latency">📊 Latência Esperada</h2>

- **Local**: < 1ms
- **Mesma Região**: < 10ms
- **Cross-Region**: 20-50ms (dependendo da distância)

Para testar a latência, use o script `test_latency.py` incluído.

<h2>🛠️ Examples</h2>

- [How to Publish (Python)](https://github.com/Lima-e-Silva/mosquitto-railway-template/wiki/How-to-Publish)
- [How to Subscribe (Python)](https://github.com/Lima-e-Silva/mosquitto-railway-template/wiki/How-to-Subscribe)
- Script de teste de latência: `test_latency.py`
