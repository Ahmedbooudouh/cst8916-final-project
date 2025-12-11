"""
Rideau Canal IoT Sensor Simulator
Simulates 3 sensors sending data to Azure IoT Hub
"""

import os
import time
import json
import random
from datetime import datetime
from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Sensor configurations
SENSORS = [
    {
        "device_id": "device-dows-lake",
        "location": "Dows Lake",
        "connection_string": os.getenv("IOT_HUB_DEVICE_DOWS_LAKE")
    },
    {
        "device_id": "device-fifth-avenue",
        "location": "Fifth Avenue",
        "connection_string": os.getenv("IOT_HUB_DEVICE_FIFTH_AVENUE")
    },
    {
        "device_id": "device-nac",
        "location": "NAC",
        "connection_string": os.getenv("IOT_HUB_DEVICE_NAC")
    }
]

# Simulation parameters for realistic data
SIMULATION_PARAMS = {
    "Dows Lake": {
        "ice_thickness": (28, 35),      # cm - Safe range
        "surface_temp": (-5, -1),       # °C
        "snow_accumulation": (0, 5),    # cm
        "external_temp": (-10, -2)      # °C
    },
    "Fifth Avenue": {
        "ice_thickness": (25, 32),      # cm - Caution range
        "surface_temp": (-3, 1),        # °C
        "snow_accumulation": (0, 8),    # cm
        "external_temp": (-8, 0)        # °C
    },
    "NAC": {
        "ice_thickness": (26, 33),      # cm
        "surface_temp": (-4, 0),        # °C
        "snow_accumulation": (0, 6),    # cm
        "external_temp": (-9, -1)       # °C
    }
}

def generate_sensor_data(location):
    """Generate realistic sensor readings for a location"""
    params = SIMULATION_PARAMS[location]
    
    # Add some random variation
    ice_thickness = round(random.uniform(*params["ice_thickness"]), 2)
    surface_temp = round(random.uniform(*params["surface_temp"]), 2)
    snow_accumulation = round(random.uniform(*params["snow_accumulation"]), 2)
    external_temp = round(random.uniform(*params["external_temp"]), 2)
    
    return {
        "deviceId": location.replace(" ", "-").lower(),
        "location": location,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "iceThickness": ice_thickness,
        "surfaceTemperature": surface_temp,
        "snowAccumulation": snow_accumulation,
        "externalTemperature": external_temp
    }

def send_telemetry(client, location):
    """Send telemetry data to IoT Hub"""
    try:
        # Generate sensor data
        data = generate_sensor_data(location)
        
        # Convert to JSON string
        message = Message(json.dumps(data))
        
        # Add properties
        message.content_encoding = "utf-8"
        message.content_type = "application/json"
        
        # Send message
        client.send_message(message)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {location}: "
              f"Ice={data['iceThickness']}cm, "
              f"Surface={data['surfaceTemperature']}°C, "
              f"Snow={data['snowAccumulation']}cm")
        
        return True
        
    except Exception as e:
        print(f"ERROR sending data for {location}: {e}")
        return False

def run_sensor(sensor_config):
    """Run a single sensor simulation"""
    device_id = sensor_config["device_id"]
    location = sensor_config["location"]
    connection_string = sensor_config["connection_string"]
    
    if not connection_string:
        print(f"ERROR: Missing connection string for {device_id}")
        return
    
    try:
        # Create IoT Hub client
        client = IoTHubDeviceClient.create_from_connection_string(connection_string)
        print(f"✓ Connected: {location} ({device_id})")
        
        # Send data every 10 seconds
        while True:
            send_telemetry(client, location)
            time.sleep(10)
            
    except KeyboardInterrupt:
        print(f"\n✓ Stopped: {location}")
    except Exception as e:
        print(f"ERROR with {location}: {e}")
    finally:
        client.shutdown()

def main():
    """Main function to run all sensors"""
    print("=" * 60)
    print("Rideau Canal IoT Sensor Simulator")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Sending data every 10 seconds...")
    print("Press Ctrl+C to stop\n")
    
    # Verify environment variables
    missing = []
    for sensor in SENSORS:
        if not sensor["connection_string"]:
            missing.append(sensor["device_id"])
    
    if missing:
        print("ERROR: Missing connection strings for:")
        for device in missing:
            print(f"  - {device}")
        print("\nPlease set these in your .env file:")
        print("IOT_HUB_DEVICE_DOWS_LAKE=...")
        print("IOT_HUB_DEVICE_FIFTH_AVENUE=...")
        print("IOT_HUB_DEVICE_NAC=...")
        return
    
        # Run each sensor in its own thread
    try:
        import threading
        
        threads = []
        for sensor in SENSORS:
            thread = threading.Thread(target=run_sensor, args=(sensor,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Keep main thread alive
        for thread in threads:
            thread.join()
            
    except KeyboardInterrupt:
        print("\n\n✓ Simulation stopped by user")
        print(f"Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()