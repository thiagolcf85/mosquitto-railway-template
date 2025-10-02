#!/usr/bin/env python3
"""
Script para testar latência do broker MQTT no Railway
"""

import paho.mqtt.client as mqtt
import time
import statistics
import sys
import argparse

class LatencyTester:
    def __init__(self, broker_host, broker_port, username=None, password=None):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.client = mqtt.Client()
        self.latencies = []
        self.message_times = {}
        self.test_topic = "test/latency"
        self.received_count = 0
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"✅ Conectado ao broker {self.broker_host}:{self.broker_port}")
            client.subscribe(self.test_topic)
        else:
            print(f"❌ Falha na conexão. Código: {rc}")
            if rc == 5:
                print("   Erro de autenticação - verifique usuário/senha")
            sys.exit(1)
            
    def on_message(self, client, userdata, msg):
        try:
            message_id = msg.payload.decode()
            if message_id in self.message_times:
                latency = (time.time() - self.message_times[message_id]) * 1000  # ms
                self.latencies.append(latency)
                self.received_count += 1
                
                # Mostra progresso a cada 10 mensagens
                if self.received_count % 10 == 0:
                    avg = statistics.mean(self.latencies[-10:])
                    print(f"  Mensagens: {self.received_count}/100 | Latência média (últimas 10): {avg:.1f}ms")
                    
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            
    def test_latency(self, num_messages=100):
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
            
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        try:
            print(f"\n🔌 Conectando a {self.broker_host}:{self.broker_port}...")
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            
            # Aguarda conexão
            time.sleep(2)
            
            print(f"\n📤 Enviando {num_messages} mensagens de teste...")
            print("─" * 60)
            
            for i in range(num_messages):
                message_id = f"msg_{i}_{time.time()}"
                self.message_times[message_id] = time.time()
                self.client.publish(self.test_topic, message_id, qos=1)
                time.sleep(0.01)  # 10ms entre mensagens
                
            # Aguarda últimas mensagens
            print("\n⏳ Aguardando últimas mensagens...")
            time.sleep(2)
            
            self.client.loop_stop()
            self.client.disconnect()
            
            # Resultados
            if self.latencies:
                print("\n" + "═" * 60)
                print("📊 RESULTADOS DO TESTE DE LATÊNCIA")
                print("═" * 60)
                print(f"🎯 Mensagens testadas: {len(self.latencies)}/{num_messages}")
                print(f"⚡ Latência mínima: {min(self.latencies):.2f} ms")
                print(f"🔥 Latência máxima: {max(self.latencies):.2f} ms")
                print(f"📈 Latência média: {statistics.mean(self.latencies):.2f} ms")
                print(f"📊 Latência mediana: {statistics.median(self.latencies):.2f} ms")
                if len(self.latencies) > 1:
                    print(f"📉 Desvio padrão: {statistics.stdev(self.latencies):.2f} ms")
                
                # Percentis
                sorted_latencies = sorted(self.latencies)
                p95 = sorted_latencies[int(len(sorted_latencies) * 0.95)]
                p99 = sorted_latencies[int(len(sorted_latencies) * 0.99)]
                print(f"📊 Percentil 95%: {p95:.2f} ms")
                print(f"📊 Percentil 99%: {p99:.2f} ms")
                print("═" * 60)
                
                # Análise
                if statistics.mean(self.latencies) < 10:
                    print("✨ Excelente! Latência muito baixa.")
                elif statistics.mean(self.latencies) < 50:
                    print("✅ Boa latência para aplicações em tempo real.")
                elif statistics.mean(self.latencies) < 100:
                    print("⚠️  Latência aceitável, mas pode ser melhorada.")
                else:
                    print("❌ Latência alta. Considere otimizações ou servidor mais próximo.")
                    
            else:
                print("❌ Nenhuma mensagem recebida. Verifique a conexão e credenciais.")
                
        except Exception as e:
            print(f"❌ Erro durante o teste: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Testa latência do broker MQTT')
    parser.add_argument('host', help='Endereço do broker MQTT')
    parser.add_argument('--port', '-p', type=int, default=1883, help='Porta do broker (padrão: 1883)')
    parser.add_argument('--username', '-u', help='Nome de usuário')
    parser.add_argument('--password', '-P', help='Senha')
    parser.add_argument('--messages', '-m', type=int, default=100, help='Número de mensagens (padrão: 100)')
    
    args = parser.parse_args()
    
    print("🚀 Teste de Latência MQTT - Mosquitto Railway")
    print("=" * 60)
    
    tester = LatencyTester(args.host, args.port, args.username, args.password)
    tester.test_latency(args.messages)