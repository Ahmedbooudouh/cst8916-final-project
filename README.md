# Rideau Canal Sensor Simulation

IoT sensor simulator for the Rideau Canal Skateway monitoring system. Simulates three sensors sending real-time data to Azure IoT Hub.

## Overview

This Python application simulates IoT sensors at three locations on the Rideau Canal:
- **Dows Lake** - Safe ice conditions
- **Fifth Avenue** - Variable conditions  
- **NAC** (National Arts Centre) - Monitored conditions

Each sensor sends telemetry every 10 seconds including:
- Ice Thickness (cm)
- Surface Temperature (°C)
- Snow Accumulation (cm)
- External Temperature (°C)

## Technologies Used

- **Python 3.8+**
- **Azure IoT Device SDK** - Communication with IoT Hub
- **python-dotenv** - Environment variable management

## Prerequisites

- Python 3.8 or higher
- Azure IoT Hub with 3 devices registered:
  - `device-dows-lake`
  - `device-fifth-avenue`
  - `device-nac`
- Device connection strings from Azure Portal

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ahmedbooudouh/rideau-canal-sensor-simulation.git
cd rideau-canal-sensor-simulation
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your IoT Hub connection strings
```

Get connection strings from:
**Azure Portal → IoT Hub → Devices → [Device Name] → Primary Connection String**

## Configuration

Edit `.env` file:

```bash
IOT_HUB_DEVICE_DOWS_LAKE=HostName=your-hub.azure-devices.net;DeviceId=device-dows-lake;SharedAccessKey=...
IOT_HUB_DEVICE_FIFTH_AVENUE=HostName=your-hub.azure-devices.net;DeviceId=device-fifth-avenue;SharedAccessKey=...
IOT_HUB_DEVICE_NAC=HostName=your-hub.azure-devices.net;DeviceId=device-nac;SharedAccessKey=...
```

## Usage

### Run the simulator

```bash
python sensor_simulator.py
```

### Expected output

```
============================================================
Rideau Canal IoT Sensor Simulator
============================================================
Started at: 2024-12-10 20:30:15
Sending data every 10 seconds...
Press Ctrl+C to stop

✓ Connected: Dows Lake (device-dows-lake)
✓ Connected: Fifth Avenue (device-fifth-avenue)
✓ Connected: NAC (device-nac)

[20:30:15] Dows Lake: Ice=32.4cm, Surface=-3.2°C, Snow=2.1cm
[20:30:15] Fifth Avenue: Ice=28.7cm, Surface=-1.5°C, Snow=4.3cm
[20:30:15] NAC: Ice=30.1cm, Surface=-2.8°C, Snow=3.5cm
...
```

### Stop the simulator

Press `Ctrl+C` to gracefully stop all sensors.

## Code Structure

```
rideau-canal-sensor-simulation/
├── sensor_simulator.py    # Main simulation script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example          # Example environment file
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

### Main Components

**`generate_sensor_data(location)`**
- Generates realistic sensor readings based on location parameters
- Adds random variation for realistic simulation

**`send_telemetry(client, location)`**
- Formats data as JSON message
- Sends to Azure IoT Hub with proper encoding

**`run_sensor(sensor_config)`**
- Creates IoT Hub client connection
- Runs continuous loop sending data every 10 seconds

## Sensor Data Format

```json
{
  "deviceId": "device-dows-lake",
  "location": "Dows Lake",
  "timestamp": "2024-12-10T20:30:15.123Z",
  "iceThickness": 32.45,
  "surfaceTemperature": -3.21,
  "snowAccumulation": 2.15,
  "externalTemperature": -5.43
}
```

## Simulation Parameters

### Dows Lake (Safe Conditions)
- Ice: 28-35 cm
- Surface Temp: -5°C to -1°C
- Snow: 0-5 cm
- External Temp: -10°C to -2°C

### Fifth Avenue (Variable Conditions)
- Ice: 25-32 cm
- Surface Temp: -3°C to 1°C
- Snow: 0-8 cm
- External Temp: -8°C to 0°C

### NAC (Monitored Conditions)
- Ice: 26-33 cm
- Surface Temp: -4°C to 0°C
- Snow: 0-6 cm
- External Temp: -9°C to -1°C

## Troubleshooting

### Error: Missing connection strings

```
ERROR: Missing connection strings for:
  - device-dows-lake
```

**Solution:** Ensure all three connection strings are set in `.env` file.

### Error: Connection refused

```
ERROR with Dows Lake: Connection refused
```

**Solution:** 
- Verify IoT Hub is running
- Check connection string is correct
- Ensure device is registered in IoT Hub

### Error: Module not found

```
ModuleNotFoundError: No module named 'azure'
```

**Solution:**
```bash
pip install -r requirements.txt
```

## Monitoring

### View messages in Azure Portal

1. Go to **Azure Portal → IoT Hub**
2. Click **Metrics** to see message count
3. Use **IoT Hub Explorer** or **Azure CLI** to see live data:

```bash
az iot hub monitor-events --hub-name your-hub-name
```

## Development

### Modify simulation parameters

Edit `SIMULATION_PARAMS` in `sensor_simulator.py`:

```python
SIMULATION_PARAMS = {
    "Dows Lake": {
        "ice_thickness": (28, 35),  # Adjust range
        "surface_temp": (-5, -1),
        # ...
    }
}
```

### Change transmission frequency

Edit line in `run_sensor()`:

```python
time.sleep(10)  # Change from 10 seconds to desired interval
```

## Related Repositories

- **Documentation:** [rideau-canal-monitoring](https://github.com/Ahmedbooudouh/rideau-canal-monitoring)
- **Dashboard:** [rideau-canal-dashboard](https://github.com/Ahmedbooudouh/rideau-canal-dashboard)

## Author

Ahmed Booudouh  
Student ID: 0411946  
Course: CST8916 - Fall 2024

## License

MIT License - Academic Project