#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
import statistics
import sys

# Configuration
BROKER_HOST = "mosquitto-railway.up.railway.app"
BROKER_PORT = 1883  # Standard MQTT port
USE_WEBSOCKETS = False
TOPIC = "test/latency"
NUM_MESSAGES = 100

# Storage for latency measurements
latencies = []
message_times = {}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker at {BROKER_HOST}:{BROKER_PORT}")
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")
        sys.exit(1)

def on_message(client, userdata, msg):
    try:
        # Calculate latency
        message_id = msg.payload.decode()
        if message_id in message_times:
            latency = (time.time() - message_times[message_id]) * 1000  # Convert to ms
            latencies.append(latency)
            if len(latencies) % 10 == 0:
                print(f"Received {len(latencies)} messages...")
    except Exception as e:
        print(f"Error processing message: {e}")

def test_latency(username, password):
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        print(f"Connecting to {BROKER_HOST}:{BROKER_PORT}...")
        if USE_WEBSOCKETS:
            client.tls_set()
            client.ws_set_options(path="/")
        client.connect(BROKER_HOST, BROKER_PORT, 60)
        client.loop_start()
        
        # Wait for connection
        time.sleep(2)
        
        print(f"Sending {NUM_MESSAGES} test messages...")
        
        # Send test messages
        for i in range(NUM_MESSAGES):
            message_id = f"msg_{i}_{time.time()}"
            message_times[message_id] = time.time()
            client.publish(TOPIC, message_id)
            time.sleep(0.01)  # Small delay between messages
        
        # Wait for all messages to return
        timeout = 30
        start_wait = time.time()
        while len(latencies) < NUM_MESSAGES and time.time() - start_wait < timeout:
            time.sleep(0.1)
        
        client.loop_stop()
        client.disconnect()
        
        # Calculate statistics
        if latencies:
            print(f"\n=== Latency Test Results ===")
            print(f"Messages sent: {NUM_MESSAGES}")
            print(f"Messages received: {len(latencies)}")
            print(f"Average latency: {statistics.mean(latencies):.2f} ms")
            print(f"Median latency: {statistics.median(latencies):.2f} ms")
            print(f"Min latency: {min(latencies):.2f} ms")
            print(f"Max latency: {max(latencies):.2f} ms")
            if len(latencies) > 1:
                print(f"Std deviation: {statistics.stdev(latencies):.2f} ms")
            
            # Check if we meet the < 50ms target
            avg_latency = statistics.mean(latencies)
            if avg_latency < 50:
                print(f"\n✅ SUCCESS: Average latency ({avg_latency:.2f} ms) is below 50ms target!")
            else:
                print(f"\n❌ FAILED: Average latency ({avg_latency:.2f} ms) exceeds 50ms target.")
        else:
            print("\n❌ No messages received!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test_latency.py <username> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    test_latency(username, password)