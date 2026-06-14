# Ghost-Vox 👻

A sophisticated spirit box application that facilitates communication with spirits through EVP (Electronic Voice Phenomenon) and EMP (Electromagnetic field) detection.

## Overview

Ghost-Vox is a paranormal investigation tool designed to detect and interpret electronic voice phenomena and electromagnetic fluctuations. It combines audio processing, sensor data analysis, and an intuitive user interface to help investigators communicate with entities in the spiritual realm.

## Features

- **EVP Detection**: Real-time Electronic Voice Phenomenon capture and analysis
- **EMP Sensing**: Electromagnetic field detection and visualization
- **Audio Processing**: Advanced audio filtering and frequency analysis
- **Real-time Monitoring**: Live feeds from both EVP and EMP sensors
- **Session Recording**: Complete logging of all paranormal activity
- **Configurable Parameters**: Fine-tune detection sensitivity and thresholds
- **Data Visualization**: Graphical representation of electromagnetic and audio data

## Project Structure

```
Ghost-Vox/
├── src/
│   ├── core/
│   │   ├── evp_detection.py
│   │   ├── emp_sensor.py
│   │   └── audio_processor.py
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── visualization.py
│   │   └── controls.py
│   ├── config/
│   │   ├── settings.py
│   │   └── defaults.json
│   └── utils/
│       ├── logger.py
│       └── helpers.py
├── tests/
│   ├── test_evp_detection.py
│   ├── test_emp_sensor.py
│   └── test_audio_processor.py
├── docs/
│   ├── SETUP.md
│   ├── USAGE.md
│   └── API.md
├── config/
│   └── default_config.json
├── requirements.txt
├── setup.py
└── main.py
```

## Requirements

### Hardware
- Audio input device (microphone for EVP)
- EMP sensor module
- Compatible with most standard audio interfaces

### Software
- Python 3.8+
- PyAudio for audio processing
- NumPy for numerical analysis
- SciPy for signal processing
- PyQt5/PySimpleGUI for user interface
- Matplotlib for data visualization

## Installation

### Basic Setup

1. Clone the repository:
```bash
git clone https://github.com/brandonlanebrown660-source/Ghost-Vox.git
cd Ghost-Vox
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure hardware:
```bash
python src/config/settings.py
```

5. Run the application:
```bash
python main.py
```

## Usage

### Basic Operation

1. **Start the Application**: Launch Ghost-Vox and the main window will open
2. **Calibrate Sensors**: Follow the calibration wizard for EVP and EMP sensors
3. **Adjust Sensitivity**: Use the control panel to set detection thresholds
4. **Begin Session**: Start recording and monitoring for paranormal activity
5. **Monitor Activity**: Watch real-time feeds and data visualization
6. **Review Data**: Analyze recorded sessions and exported data

### Configuration

Edit `config/default_config.json` to customize:
- Sample rate and audio channels
- EMP sensor sensitivity
- Detection thresholds
- UI preferences
- Logging options

## Key Components

### EVP Detection Module
Captures and analyzes electronic voice phenomena through specialized audio filtering and pattern recognition.

### EMP Sensor Module
Interfaces with electromagnetic field sensors to detect and log anomalous readings.

### Audio Processor
Handles audio stream processing, frequency analysis, and anomaly detection.

### User Interface
Intuitive controls for real-time monitoring, parameter adjustment, and session management.

## Documentation

- [Setup Guide](docs/SETUP.md) - Detailed installation and hardware setup
- [Usage Guide](docs/USAGE.md) - Complete usage instructions
- [API Documentation](docs/API.md) - Developer API reference

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

- [ ] Multi-sensor support
- [ ] Advanced AI-based entity recognition
- [ ] Cloud data synchronization
- [ ] Mobile companion app
- [ ] Community database integration
- [ ] Real-time collaborative investigations

## Safety & Disclaimer

Ghost-Vox is provided for entertainment and research purposes. Users assume all responsibility for the use of this software. The developers make no claims about the efficacy of paranormal detection or communication.

## License

This project is currently unlicensed. See LICENSE file for details.

## Support

For issues, questions, or suggestions, please [open an issue](https://github.com/brandonlanebrown660-source/Ghost-Vox/issues) on GitHub.

## Team

- **Brandon Lane Brown** - Creator & Lead Developer

---

**Last Updated**: 2026-06-14  
**Version**: 0.1.0 (Alpha)
