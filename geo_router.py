#!/usr/bin/env python3
"""
Roteador Geográfico Inteligente para MQTT
Direciona clientes para o broker mais próximo baseado na localização
"""

import requests
import json
import socket
from typing import Dict, Tuple, Optional
import geoip2.database
import geoip2.errors

class MQTTGeoRouter:
    def __init__(self):
        self.brokers = {
            'us-east': {
                'host': 'switchback.proxy.rlwy.net',
                'port': 34718,
                'region': 'US-East',
                'lat': 39.0458, 'lon': -76.6413,  # Baltimore
                'weight': 100
            },
            'local-cache': {
                'host': 'localhost',
                'port': 1884,
                'region': 'Local-Cache',
                'lat': 0, 'lon': 0,
                'weight': 200  # Prioridade alta para cache local
            },
            'accelerated': {
                'host': 'localhost',
                'port': 1885,
                'region': 'Load-Balanced',
                'lat': 0, 'lon': 0,
                'weight': 150
            }
        }
    
    def get_client_location(self, ip_address: str) -> Optional[Tuple[float, float]]:
        """Obtém localização do cliente por IP"""
        try:
            # Tenta usar serviço online primeiro
            response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return (data['lat'], data['lon'])
        except:
            pass
        
        # Fallback para detecção local
        if ip_address.startswith(('192.168.', '10.', '172.')):
            return (0, 0)  # Rede local
        
        return None
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcula distância entre duas coordenadas (fórmula de Haversine)"""
        import math
        
        R = 6371  # Raio da Terra em km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2)**2 + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def find_best_broker(self, client_ip: str) -> Dict:
        """Encontra o melhor broker para o cliente"""
        client_location = self.get_client_location(client_ip)
        
        if not client_location:
            # Fallback para broker padrão
            return self.brokers['accelerated']
        
        client_lat, client_lon = client_location
        best_broker = None
        best_score = float('inf')
        
        for broker_id, broker in self.brokers.items():
            # Calcula distância
            distance = self.calculate_distance(
                client_lat, client_lon,
                broker['lat'], broker['lon']
            )
            
            # Score combinando distância e peso do broker
            # Menor distância e maior peso = melhor score
            score = distance / (broker['weight'] / 100)
            
            if score < best_score:
                best_score = score
                best_broker = broker.copy()
                best_broker['id'] = broker_id
                best_broker['distance_km'] = distance
                best_broker['score'] = score
        
        return best_broker
    
    def test_broker_latency(self, host: str, port: int) -> float:
        """Testa latência TCP para um broker"""
        try:
            import time
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            latency = (time.time() - start) * 1000
            return latency if result == 0 else float('inf')
        except:
            return float('inf')
    
    def get_broker_recommendation(self, client_ip: str) -> Dict:
        """Recomendação completa incluindo teste de latência"""
        broker = self.find_best_broker(client_ip)
        
        # Testa latência real
        latency = self.test_broker_latency(broker['host'], broker['port'])
        broker['tested_latency_ms'] = latency
        
        # Adiciona informações extras
        broker['connection_string'] = f"mqtt://{broker['host']}:{broker['port']}"
        broker['recommended'] = latency < 1000  # Considera bom se < 1s
        
        return broker

def main():
    router = MQTTGeoRouter()
    
    # Testa com alguns IPs exemplo
    test_ips = [
        '127.0.0.1',      # Local
        '8.8.8.8',        # Google DNS (US)
        '1.1.1.1',        # Cloudflare
    ]
    
    print("🌍 MQTT Geo Router - Teste de Roteamento Inteligente")
    print("=" * 60)
    
    for ip in test_ips:
        print(f"\n📍 Cliente IP: {ip}")
        recommendation = router.get_broker_recommendation(ip)
        
        print(f"  🎯 Broker recomendado: {recommendation['id']} ({recommendation['region']})")
        print(f"  🔗 Conexão: {recommendation['connection_string']}")
        print(f"  📏 Distância: {recommendation.get('distance_km', 0):.1f} km")
        print(f"  ⚡ Latência testada: {recommendation['tested_latency_ms']:.1f} ms")
        print(f"  ✅ Recomendado: {'Sim' if recommendation['recommended'] else 'Não'}")

if __name__ == "__main__":
    main()