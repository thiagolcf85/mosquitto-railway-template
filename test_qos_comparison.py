#!/usr/bin/env python3
"""
Compara latência entre diferentes níveis de QoS
"""

import paho.mqtt.client as mqtt
import time
import statistics

class QoSComparison:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        
    def test_qos(self, qos_level, num_messages=20):
        client = mqtt.Client()
        client.username_pw_set(self.username, self.password)
        
        latencies = []
        message_times = {}
        received = 0
        
        def on_connect(c, u, f, rc):
            if rc == 0:
                c.subscribe(f"test/qos{qos_level}", qos=qos_level)
                
        def on_message(c, u, msg):
            nonlocal received
            msg_id = msg.payload.decode()
            if msg_id in message_times:
                latency = (time.time() - message_times[msg_id]) * 1000
                latencies.append(latency)
                received += 1
                
        client.on_connect = on_connect
        client.on_message = on_message
        
        client.connect(self.host, self.port)
        client.loop_start()
        time.sleep(1)
        
        # Enviar mensagens
        for i in range(num_messages):
            msg_id = f"q{qos_level}_{i}_{time.time()}"
            message_times[msg_id] = time.time()
            client.publish(f"test/qos{qos_level}", msg_id, qos=qos_level)
            time.sleep(0.05)  # 50ms entre mensagens
            
        # Aguardar
        time.sleep(2)
        client.loop_stop()
        client.disconnect()
        
        if latencies:
            return {
                'qos': qos_level,
                'sent': num_messages,
                'received': received,
                'min': min(latencies),
                'max': max(latencies),
                'avg': statistics.mean(latencies),
                'median': statistics.median(latencies)
            }
        return None

# Executar testes
print("🔬 Comparação de Latência por QoS - Mosquitto Railway")
print("=" * 60)

tester = QoSComparison(
    "switchback.proxy.rlwy.net", 
    34718,
    "admin_mosquitto",
    "sl977w05jmmqzbgr4g4v27x4umxyf01z"
)

for qos in [0, 1, 2]:
    print(f"\n📊 Testando QoS {qos}...")
    result = tester.test_qos(qos)
    if result:
        print(f"  ✅ Recebidas: {result['received']}/{result['sent']}")
        print(f"  ⚡ Min: {result['min']:.1f}ms | Max: {result['max']:.1f}ms")
        print(f"  📈 Média: {result['avg']:.1f}ms | Mediana: {result['median']:.1f}ms")
    else:
        print("  ❌ Falha no teste")

print("\n" + "=" * 60)
print("💡 Recomendações:")
print("- QoS 0: Mais rápido, sem garantia de entrega")
print("- QoS 1: Garante entrega, latência moderada")
print("- QoS 2: Garante entrega única, maior latência")