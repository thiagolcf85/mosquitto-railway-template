#!/usr/bin/env python3
"""
Teste de latência com sistema acelerado
Compara performance entre broker normal e acelerado
"""

import paho.mqtt.client as mqtt
import time
import statistics
import threading
from concurrent.futures import ThreadPoolExecutor

class AcceleratedLatencyTest:
    def __init__(self):
        self.test_configs = {
            'railway_direct': {
                'host': 'switchback.proxy.rlwy.net',
                'port': 34718,
                'name': 'Railway Direto',
                'username': 'admin_mosquitto',
                'password': 'sl977w05jmmqzbgr4g4v27x4umxyf01z'
            },
            'local_cache': {
                'host': 'localhost',
                'port': 1884,
                'name': 'Cache Local',
                'username': None,
                'password': None
            },
            'load_balanced': {
                'host': 'localhost',
                'port': 1885,
                'name': 'Load Balanced',
                'username': None,
                'password': None
            }
        }
    
    def test_single_broker(self, config, num_messages=50):
        """Testa latência de um broker específico"""
        latencies = []
        message_times = {}
        received_count = 0
        
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                client.subscribe("test/accelerated")
        
        def on_message(client, userdata, msg):
            nonlocal received_count
            try:
                msg_id = msg.payload.decode()
                if msg_id in message_times:
                    latency = (time.time() - message_times[msg_id]) * 1000
                    latencies.append(latency)
                    received_count += 1
            except:
                pass
        
        client = mqtt.Client()
        if config['username'] and config['password']:
            client.username_pw_set(config['username'], config['password'])
        
        client.on_connect = on_connect
        client.on_message = on_message
        
        try:
            client.connect(config['host'], config['port'], 60)
            client.loop_start()
            time.sleep(1)
            
            # Envia mensagens
            for i in range(num_messages):
                msg_id = f"acc_{i}_{time.time()}"
                message_times[msg_id] = time.time()
                client.publish("test/accelerated", msg_id, qos=0)
                time.sleep(0.02)  # 20ms entre mensagens
            
            # Aguarda respostas
            time.sleep(3)
            client.loop_stop()
            client.disconnect()
            
            return {
                'config': config['name'],
                'sent': num_messages,
                'received': received_count,
                'latencies': latencies,
                'success_rate': (received_count / num_messages * 100) if num_messages > 0 else 0
            }
            
        except Exception as e:
            return {
                'config': config['name'],
                'error': str(e),
                'sent': num_messages,
                'received': 0,
                'latencies': [],
                'success_rate': 0
            }
    
    def run_parallel_test(self):
        """Executa teste paralelo em todos os brokers"""
        print("🚀 Teste de Latência - Sistema Acelerado vs Normal")
        print("=" * 70)
        
        results = {}
        
        # Testa conectividade primeiro
        print("🔍 Verificando conectividade dos brokers...")
        for name, config in self.test_configs.items():
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((config['host'], config['port']))
                sock.close()
                status = "✅ Online" if result == 0 else "❌ Offline"
                print(f"  {config['name']}: {status}")
            except:
                print(f"  {config['name']}: ❌ Erro de conexão")
        
        print("\n📊 Executando testes de latência...")
        
        # Executa testes em paralelo
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self.test_single_broker, config): name 
                for name, config in self.test_configs.items()
            }
            
            for future in futures:
                name = futures[future]
                try:
                    result = future.result(timeout=30)
                    results[name] = result
                    
                    if result['latencies']:
                        avg_lat = statistics.mean(result['latencies'])
                        min_lat = min(result['latencies'])
                        max_lat = max(result['latencies'])
                        print(f"  ✅ {result['config']}: {avg_lat:.1f}ms avg ({min_lat:.1f}-{max_lat:.1f}ms)")
                    else:
                        print(f"  ❌ {result['config']}: {result.get('error', 'Sem resposta')}")
                        
                except Exception as e:
                    print(f"  ❌ {self.test_configs[name]['name']}: Timeout ou erro")
                    results[name] = {'config': self.test_configs[name]['name'], 'error': str(e)}
        
        return results
    
    def analyze_results(self, results):
        """Analisa e compara resultados"""
        print("\n" + "=" * 70)
        print("📈 ANÁLISE COMPARATIVA DE PERFORMANCE")
        print("=" * 70)
        
        valid_results = {k: v for k, v in results.items() if v.get('latencies')}
        
        if not valid_results:
            print("❌ Nenhum teste válido completado.")
            return
        
        # Tabela de resultados
        print(f"{'Broker':<20} {'Média (ms)':<12} {'Min (ms)':<10} {'Max (ms)':<10} {'Taxa %':<8}")
        print("-" * 70)
        
        best_config = None
        best_latency = float('inf')
        
        for name, result in valid_results.items():
            if result['latencies']:
                avg = statistics.mean(result['latencies'])
                min_lat = min(result['latencies'])
                max_lat = max(result['latencies'])
                rate = result['success_rate']
                
                print(f"{result['config']:<20} {avg:<12.1f} {min_lat:<10.1f} {max_lat:<10.1f} {rate:<8.1f}")
                
                if avg < best_latency:
                    best_latency = avg
                    best_config = result['config']
        
        print("\n🏆 RECOMENDAÇÕES:")
        if best_config:
            print(f"  Melhor performance: {best_config} ({best_latency:.1f}ms)")
            
            improvement = None
            railway_result = None
            for result in valid_results.values():
                if 'Railway' in result['config'] and result['latencies']:
                    railway_avg = statistics.mean(result['latencies'])
                    improvement = ((railway_avg - best_latency) / railway_avg * 100)
                    break
            
            if improvement and improvement > 0:
                print(f"  Melhoria de latência: {improvement:.1f}% vs Railway direto")
            
            if best_latency < 50:
                print("  ✨ Excelente! Latência otimizada para tempo real.")
            elif best_latency < 100:
                print("  ✅ Boa latência para aplicações MQTT.")
            else:
                print("  ⚠️  Latência ainda pode ser melhorada.")

def main():
    tester = AcceleratedLatencyTest()
    results = tester.run_parallel_test()
    tester.analyze_results(results)

if __name__ == "__main__":
    main()