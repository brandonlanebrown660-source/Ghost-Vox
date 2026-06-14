# Ghost-Vox API Documentation

Developer API reference for Ghost-Vox components.

## Core Modules

### EVPDetector

Electronic Voice Phenomenon detection system.

#### Initialization

```python
from src.core.evp_detection import EVPDetector

detector = EVPDetector(sample_rate=44100, config=config_dict)
```

#### Methods

##### `calibrate_noise_profile(audio_chunk, samples=100)`

Calibrate noise profile from background audio.

**Parameters:**
- `audio_chunk` (np.ndarray): Audio data for calibration
- `samples` (int): Number of FFT samples to average

**Example:**
```python
detector.calibrate_noise_profile(background_audio, samples=100)
```

##### `apply_bandpass_filter(audio)`

Apply bandpass filter to isolate EVP frequency range.

**Parameters:**
- `audio` (np.ndarray): Input audio data

**Returns:**
- (np.ndarray): Filtered audio data

**Example:**
```python
filtered = detector.apply_bandpass_filter(audio_data)
```

##### `detect_anomalies(audio_chunk)`

Detect anomalous audio patterns indicating EVP.

**Parameters:**
- `audio_chunk` (np.ndarray): Audio data to analyze

**Returns:**
- List[EVPEvent]: Detected EVP events

**Example:**
```python
events = detector.detect_anomalies(audio_chunk)
for event in events:
    print(f"EVP detected: {event.frequency}Hz")
```

##### `get_spectrum(audio_chunk)`

Get frequency spectrum of audio.

**Parameters:**
- `audio_chunk` (np.ndarray): Audio data

**Returns:**
- Tuple[np.ndarray, np.ndarray]: (frequencies, magnitudes)

**Example:**
```python
freqs, spec = detector.get_spectrum(audio_data)
```

##### `process_audio_stream(audio_chunk)`

Process audio stream for EVP detection.

**Parameters:**
- `audio_chunk` (np.ndarray): Audio data chunk

**Returns:**
- Dict: Detection results

**Result Keys:**
- `events` (List[EVPEvent]): Detected events
- `frequencies` (np.ndarray): Frequency array
- `spectrum` (np.ndarray): Magnitude spectrum
- `buffer_size` (int): Current buffer size
- `event_count` (int): Number of events

**Example:**
```python
result = detector.process_audio_stream(chunk)
print(f"Found {result['event_count']} events")
```

#### EVPEvent Dataclass

```python
@dataclass
class EVPEvent:
    timestamp: float          # Event time in seconds
    frequency: float          # Frequency in Hz
    amplitude: float          # Signal strength in dB
    duration_ms: float        # Duration in milliseconds
    confidence: float         # Confidence 0-1
    audio_data: np.ndarray    # Event audio data
```

---

### EMPSensor

Electromagnetic field sensor interface.

#### Initialization

```python
from src.core.emp_sensor import EMPSensor

sensor = EMPSensor(config=config_dict)
```

#### Methods

##### `calibrate_baseline(readings)`

Calibrate baseline from quiet environment.

**Parameters:**
- `readings` (List[float]): Baseline readings

**Example:**
```python
baseline_readings = [45.2, 46.1, 45.8, 44.9]
sensor.calibrate_baseline(baseline_readings)
```

##### `process_reading(field_strength)`

Process a raw EMP sensor reading.

**Parameters:**
- `field_strength` (float): Field strength value

**Returns:**
- EMPReading: Processed reading

**Example:**
```python
reading = sensor.process_reading(125.5)
if reading.is_anomaly:
    print("Anomaly detected!")
```

##### `get_statistics()`

Get sensor statistics.

**Returns:**
- Dict: Sensor statistics

**Statistics Keys:**
- `baseline` (float): Calibrated baseline
- `current_reading` (float): Latest reading
- `average_reading` (float): Average reading
- `max_reading` (float): Maximum reading
- `min_reading` (float): Minimum reading
- `anomalies_detected` (int): Count of anomalies
- `anomaly_percentage` (float): Percentage of anomalies

**Example:**
```python
stats = sensor.get_statistics()
print(f"Anomalies: {stats['anomalies_detected']}")
```

##### `get_recent_anomalies(count=10)`

Get recent anomalies.

**Parameters:**
- `count` (int): Number of recent anomalies

**Returns:**
- List[EMPReading]: Recent anomalies

**Example:**
```python
recent = sensor.get_recent_anomalies(count=5)
for anomaly in recent:
    print(f"Anomaly: {anomaly.field_strength}mV")
```

#### EMPReading Dataclass

```python
@dataclass
class EMPReading:
    timestamp: float      # Reading time
    field_strength: float # Field strength in mV
    frequency: float      # Frequency in Hz
    anomaly_score: float  # Anomaly score 0-1
    is_anomaly: bool      # Is anomalous
```

---

### AudioProcessor

Real-time audio capture and processing.

#### Initialization

```python
from src.core.audio_processor import AudioProcessor

processor = AudioProcessor(config=config_dict)
```

#### Methods

##### `get_input_devices()`

Get list of available audio input devices.

**Returns:**
- List[Dict]: Device information

**Device Keys:**
- `index` (int): Device index
- `name` (str): Device name
- `channels` (int): Input channels
- `sample_rate` (float): Sample rate

**Example:**
```python
devices = processor.get_input_devices()
for dev in devices:
    print(f"[{dev['index']}] {dev['name']}")
```

##### `start_recording()`

Start audio recording stream.

**Returns:**
- bool: Success status

**Example:**
```python
if processor.start_recording():
    print("Recording started")
```

##### `stop_recording()`

Stop audio recording stream.

**Returns:**
- bool: Success status

**Example:**
```python
processor.stop_recording()
```

##### `get_audio_frame(timeout=1.0)`

Get next audio frame from queue.

**Parameters:**
- `timeout` (float): Timeout in seconds

**Returns:**
- AudioFrame or None: Audio frame or None if timeout

**Example:**
```python
frame = processor.get_audio_frame(timeout=1.0)
if frame:
    print(f"Got frame {frame.frame_number}")
```

##### `get_statistics()`

Get processor statistics.

**Returns:**
- Dict: Processor statistics

**Statistics Keys:**
- `sample_rate` (int): Sample rate
- `channels` (int): Number of channels
- `frames_captured` (int): Total frames captured
- `frames_dropped` (int): Frames dropped
- `queue_size` (int): Current queue size

**Example:**
```python
stats = processor.get_statistics()
print(f"Captured: {stats['frames_captured']}")
```

#### AudioFrame Dataclass

```python
@dataclass
class AudioFrame:
    data: np.ndarray      # Audio data (float32)
    timestamp: float      # Capture time
    frame_number: int     # Frame sequence number
```

---

## Complete Example

```python
import json
import numpy as np
from src.core.evp_detection import EVPDetector
from src.core.emp_sensor import EMPSensor
from src.core.audio_processor import AudioProcessor
from src.utils.logger import setup_logging

# Setup
config = json.load(open('config/default_config.json'))
logger = setup_logging(config)

# Initialize components
audio = AudioProcessor(config)
evp = EVPDetector(sample_rate=config['audio']['sample_rate'], config=config)
emp = EMPSensor(config=config)

# Calibrate
audio.start_recording()
time.sleep(2)  # Record calibration audio
calib_frames = []
for _ in range(10):
    frame = audio.get_audio_frame()
    if frame:
        calib_frames.append(frame.data)

if calib_frames:
    calib_audio = np.concatenate(calib_frames)
    evp.calibrate_noise_profile(calib_audio)
    emp.calibrate_baseline([50.0] * 100)

# Main loop
try:
    while True:
        # Get audio frame
        frame = audio.get_audio_frame()
        if frame:
            # Process EVP
            evp_result = evp.process_audio_stream(frame.data)
            
            # Log events
            for event in evp_result['events']:
                logger.warning(f"EVP: {event.frequency}Hz, {event.confidence:.0%}")
            
            # Process EMP (simulated)
            import random
            reading = emp.process_reading(random.uniform(40, 150))
            
            if reading.is_anomaly:
                logger.warning(f"EMP Anomaly: {reading.field_strength}mV")

except KeyboardInterrupt:
    audio.stop_recording()
    print(audio.get_statistics())
    print(emp.get_statistics())
```

## Utilities

### Logger

```python
from src.utils.logger import setup_logging, get_logger

# Setup logging
logger = setup_logging(config)

# Get named logger
logger = get_logger('my_module')
logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
```

### Helpers

```python
from src.utils.helpers import *

# Configuration
config = load_config('config/default_config.json')
save_config(config, 'config/new.json')

# Utilities
timestamp = get_timestamp()
filename = get_session_filename('session')
linear = db_to_linear(-20)
db = linear_to_db(0.1)
freq_str = format_frequency(1500)  # "1.50 kHz"
dur_str = format_duration(125.5)   # "00:02:05"
```

## Configuration Reference

```json
{
  "audio": {
    "sample_rate": 44100,
    "channels": 1,
    "chunk_size": 2048,
    "device_index": -1
  },
  "evp_detection": {
    "enabled": true,
    "sensitivity": 0.7,
    "min_frequency": 300,
    "max_frequency": 8000,
    "threshold_db": -40
  },
  "emp_sensor": {
    "enabled": true,
    "sensitivity": 0.8,
    "baseline_threshold": 50,
    "alert_threshold": 150
  }
}
```

## Error Handling

```python
try:
    result = evp.process_audio_stream(audio_data)
except Exception as e:
    logger.error(f"EVP processing error: {e}")

try:
    reading = emp.process_reading(value)
except Exception as e:
    logger.error(f"EMP reading error: {e}")

try:
    if not audio.start_recording():
        logger.error("Failed to start recording")
except Exception as e:
    logger.error(f"Audio error: {e}")
```

---
**Last Updated**: 2026-06-14
