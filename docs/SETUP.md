# Ghost-Vox Setup Guide

Complete setup instructions for the Ghost-Vox spirit box application.

## System Requirements

### Minimum Requirements
- Python 3.8 or higher
- 4GB RAM
- Audio input device (microphone)
- Operating System: Windows, macOS, or Linux

### Recommended Setup
- Python 3.10+
- 8GB+ RAM
- Quality audio interface or directional microphone
- EMP sensor hardware (for full functionality)
- Stable internet connection (for future cloud features)

## Installation Steps

### 1. Install Python

Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python --version
```

### 2. Clone Repository

```bash
git clone https://github.com/brandonlanebrown660-source/Ghost-Vox.git
cd Ghost-Vox
```

### 3. Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Platform-Specific Setup

#### macOS
```bash
# Install PortAudio (required for PyAudio)
brew install portaudio
pip install pyaudio
```

#### Windows
PyAudio is included in requirements.txt. If you encounter issues:
```bash
pip install pipwin
pipwin install pyaudio
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

## Hardware Setup

### Audio Input Configuration

1. **Connect your audio device**
   - USB microphone
   - Audio interface
   - Built-in microphone

2. **Configure in Ghost-Vox**
   - Run: `python main.py`
   - The application will list available devices
   - Edit `config/default_config.json` to select your device:
     ```json
     "audio": {
       "device_index": 2
     }
     ```

### EMP Sensor Configuration

1. **Hardware Connection**
   - Connect EMP sensor to appropriate interface
   - USB adapter or serial connection

2. **Driver Installation**
   - Install sensor-specific drivers if required
   - Verify connection: `python -c "import <sensor_module>"`

3. **Calibration**
   - Place sensor in quiet environment
   - Run calibration: `python -m src.core.emp_sensor`
   - Note baseline values

## Configuration

### Initial Configuration

1. Copy default configuration:
```bash
cp config/default_config.json config/my_config.json
```

2. Edit settings as needed:
```json
{
  "audio": {
    "sample_rate": 44100,
    "channels": 1,
    "chunk_size": 2048,
    "device_index": -1
  },
  "evp_detection": {
    "sensitivity": 0.7,
    "min_frequency": 300,
    "max_frequency": 8000,
    "threshold_db": -40
  },
  "emp_sensor": {
    "sensitivity": 0.8,
    "alert_threshold": 150
  }
}
```

### Environment Variables

Create `.env` file in project root:
```
GHOST_VOX_LOG_LEVEL=INFO
GHOST_VOX_SESSION_DIR=./sessions
GHOST_VOX_CONFIG=config/default_config.json
```

## Running Ghost-Vox

### Command Line

```bash
# Basic run
python main.py

# With custom config
python main.py --config config/my_config.json

# With debug logging
python main.py --debug
```

### Testing Installation

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Troubleshooting

### Audio Device Not Detected

1. Check available devices:
```python
import pyaudio
pa = pyaudio.PyAudio()
for i in range(pa.get_device_count()):
    print(f"{i}: {pa.get_device_info_by_index(i)['name']}")
```

2. Update `device_index` in config

### PyAudio Installation Issues

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
LDFLAGS=-L/usr/local/opt/portaudio/lib CPPFLAGS=-I/usr/local/opt/portaudio/include pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install python3-dev portaudio19-dev
pip install pyaudio
```

### High Latency

1. Reduce `chunk_size` in config (e.g., 512 or 1024)
2. Close other audio applications
3. Update audio drivers
4. Use a dedicated audio interface

### EMP Sensor Not Responding

1. Check USB connection
2. Verify driver installation
3. Check `dmesg` for device recognition (Linux)
4. Review sensor documentation

## First Run Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Audio device detected
- [ ] Configuration file reviewed
- [ ] Hardware calibrated
- [ ] Tests passing (`pytest tests/`)
- [ ] Can run: `python main.py`

## Next Steps

1. Read [USAGE.md](USAGE.md) for operation guide
2. Review [API.md](API.md) for developer documentation
3. Configure your investigation parameters
4. Run initial calibration
5. Begin paranormal investigation!

## Support

For issues:
1. Check logs in `logs/ghost_vox.log`
2. Review GitHub issues
3. Consult sensor documentation
4. Check system audio settings

---
**Last Updated**: 2026-06-14
