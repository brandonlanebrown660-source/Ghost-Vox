# Ghost-Vox Usage Guide

Complete guide for operating the Ghost-Vox spirit box application.

## Quick Start

### 1. Launch Application
```bash
python main.py
```

### 2. Initial Calibration
- Place sensors in quiet environment
- Let calibration run for 10-30 seconds
- Review baseline readings

### 3. Begin Investigation
- Adjust sensitivity as needed
- Monitor EVP and EMP feeds
- Record sessions

## User Interface

### Main Window

The main Ghost-Vox window displays:

- **EVP Monitor**: Real-time audio frequency analysis
- **EMP Display**: Electromagnetic field readings
- **Control Panel**: Sensitivity and parameter adjustments
- **Session Info**: Recording status and statistics
- **Event Log**: Detected phenomena

### Control Panel

#### EVP Controls
- **Sensitivity Slider**: 0-100% detection sensitivity
- **Frequency Range**: Min/Max frequency filter (Hz)
- **Threshold**: Minimum detection threshold (dB)
- **Calibrate Button**: Recalibrate noise profile

#### EMP Controls
- **Sensitivity**: 0-100% sensor sensitivity
- **Baseline Threshold**: Quiet environment baseline
- **Alert Threshold**: Anomaly detection threshold
- **Reset Stats**: Clear statistics

#### Recording Controls
- **Record Button**: Start/stop session recording
- **Session Name**: Name for current session
- **Output Directory**: Where to save recordings
- **Auto-Archive**: Automatically archive old sessions

## Operation Modes

### Passive Monitoring
- Monitor without recording
- Useful for learning and calibration
- No data saved

```bash
python main.py --monitor-only
```

### Active Investigation
- Full recording and analysis
- All data saved
- Real-time alerts for anomalies

```bash
python main.py --investigation
```

### Calibration Mode
- Establish baseline readings
- Noise profile generation
- Device testing

```bash
python main.py --calibrate
```

## Configuration Adjustments

### Audio Settings

Edit `config/default_config.json`:

```json
"audio": {
  "sample_rate": 44100,
  "channels": 1,
  "chunk_size": 2048,
  "device_index": 0
}
```

- **sample_rate**: Higher = better frequency resolution, more CPU usage
- **channels**: 1 for mono, 2 for stereo
- **chunk_size**: Smaller = lower latency, higher CPU usage
- **device_index**: Select audio device (run `python main.py --list-devices`)

### EVP Detection Settings

```json
"evp_detection": {
  "sensitivity": 0.7,
  "min_frequency": 300,
  "max_frequency": 8000,
  "threshold_db": -40
}
```

- **sensitivity**: 0.0-1.0 (higher = more detections, more false positives)
- **min_frequency**: Lowest frequency to detect (Hz)
- **max_frequency**: Highest frequency to detect (Hz)
- **threshold_db**: Minimum signal strength to detect

### EMP Sensor Settings

```json
"emp_sensor": {
  "sensitivity": 0.8,
  "baseline_threshold": 50,
  "alert_threshold": 150
}
```

- **sensitivity**: 0.0-1.0 (higher = more sensitive)
- **baseline_threshold**: Quiet environment reading
- **alert_threshold**: Anomaly trigger point

## Session Recording

### Starting a Session

1. Click "Record" or press 'R'
2. Enter session name (optional)
3. Confirm output directory
4. Recording begins

### During Recording

- All EVP events logged
- EMP readings recorded
- Audio stream captured
- Real-time monitoring continues

### Ending Session

1. Click "Stop" or press 'S'
2. Session automatically saved
3. Review summary
4. File locations displayed

### Session Files

Sessions saved to `./sessions/` with structure:

```
sessions/
├── session_20260614_143022/
│   ├── audio.wav              # Audio recording
│   ├── metadata.json          # Session info
│   ├── evp_events.csv        # EVP detections
│   ├── emp_readings.csv      # EMP data
│   └── session_log.txt       # Full event log
```

## Interpreting Results

### EVP Events

Displayed in format:
```
Frequency: 850 Hz
Amplitude: -28 dB
Confidence: 85%
Duration: 450 ms
```

**Frequency**: Voice frequency typically 300-3500 Hz
**Amplitude**: Signal strength (higher = louder)
**Confidence**: Detection certainty (0-100%)

### EMP Anomalies

Displayed as:
```
Field Strength: 145 mV
Baseline: 50 mV
Deviation: +95 mV
Anomaly Score: 78%
```

**Baseline**: Normal environmental reading
**Deviation**: Difference from baseline
**Anomaly Score**: How unusual the reading is

## Troubleshooting

### No Audio Input

1. Check microphone connection
2. Verify in system audio settings
3. Test: `python -m src.core.audio_processor`
4. Run: `python main.py --list-devices`

### False Positives

- Reduce sensitivity
- Increase threshold_db
- Recalibrate noise profile
- Check for RF interference

### Low Sensitivity

- Increase sensitivity slider
- Lower threshold_db
- Reduce min_frequency
- Recalibrate with better baseline

### High Latency

- Reduce chunk_size
- Lower sample_rate
- Close other applications
- Use dedicated audio interface

## Investigation Tips

### Best Practices

1. **Calibrate First**: Always calibrate in quiet environment
2. **Start Conservative**: Begin with lower sensitivity
3. **Document Everything**: Note environmental conditions
4. **Multiple Sessions**: Run multiple sessions for comparison
5. **Verify Findings**: Cross-reference EVP and EMP data

### Environmental Conditions

- Temperature: Stable temperature reduces false positives
- Electricity: Avoid areas with lots of electrical equipment
- RF Interference: Move away from WiFi, cell towers
- Background Noise: Quieter environment = better results

### Investigation Techniques

#### Word Association
- Ask yes/no questions
- Listen for EVP responses
- Compare EMP spikes with questions

#### Frequency Scanning
- Sweep EVP frequency range
- Note where spirit communicates
- Adjust filters to target frequency

#### EMP Baseline Building
- Record normal EMP readings
- Establish location baseline
- Compare investigation to baseline

## Advanced Features

### Command Line Options

```bash
# List available audio devices
python main.py --list-devices

# Run with specific config
python main.py --config config/custom.json

# Debug mode (verbose logging)
python main.py --debug

# Headless mode (no GUI)
python main.py --headless

# Show version
python main.py --version
```

### API Usage

For programmatic access:

```python
from src.core.evp_detection import EVPDetector
from src.core.emp_sensor import EMPSensor
from src.core.audio_processor import AudioProcessor

# Initialize components
evp = EVPDetector(sample_rate=44100, config=config)
emp = EMPSensor(config=config)
audio = AudioProcessor(config=config)

# Start processing
audio.start_recording()

# Get frames and process
while True:
    frame = audio.get_audio_frame()
    if frame:
        evp_result = evp.process_audio_stream(frame.data)
        emp_reading = emp.process_reading(get_emp_value())
```

## Data Export

### Exporting Sessions

1. Sessions automatically saved to `./sessions/`
2. Each session is a directory with:
   - Raw audio (WAV)
   - Event logs (CSV)
   - Metadata (JSON)

### Analyzing Data

```python
import json
import pandas as pd

# Load metadata
with open('session_20260614_143022/metadata.json') as f:
    meta = json.load(f)

# Load EVP events
evp_events = pd.read_csv('session_20260614_143022/evp_events.csv')
emp_readings = pd.read_csv('session_20260614_143022/emp_readings.csv')

# Analyze
print(evp_events.describe())
print(emp_readings['anomaly_score'].mean())
```

## Support & Resources

- **Documentation**: See `docs/` directory
- **Issues**: GitHub issues page
- **Logs**: Check `logs/ghost_vox.log`
- **Configuration**: Edit `config/default_config.json`

---
**Last Updated**: 2026-06-14
