"""
Unit tests for EVP Detection Module
"""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from core.evp_detection import EVPDetector, EVPEvent


@pytest.fixture
def detector():
    """Create EVP detector for testing"""
    config = {
        'evp_detection': {
            'sensitivity': 0.7,
            'min_frequency': 300,
            'max_frequency': 8000,
            'threshold_db': -40,
            'noise_floor': -60
        },
        'advanced': {
            'fft_resolution': 2048
        }
    }
    return EVPDetector(sample_rate=44100, config=config)


@pytest.fixture
def test_audio():
    """Generate test audio signal"""
    sample_rate = 44100
    duration = 1.0
    frequency = 1000.0
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Pure sine wave at 1kHz
    signal = np.sin(2 * np.pi * frequency * t).astype(np.float32)
    return signal


class TestEVPDetector:
    """Test EVP Detector functionality"""
    
    def test_initialization(self):
        """Test detector initialization"""
        detector = EVPDetector(sample_rate=44100)
        assert detector.sample_rate == 44100
        assert detector.is_calibrated == False
        assert len(detector.audio_buffer) == 0
    
    def test_calibrate_noise_profile(self, detector, test_audio):
        """Test noise profile calibration"""
        detector.calibrate_noise_profile(test_audio, samples=10)
        
        assert detector.is_calibrated == True
        assert detector.noise_profile is not None
        assert len(detector.noise_profile) > 0
    
    def test_bandpass_filter(self, detector, test_audio):
        """Test bandpass filter"""
        filtered = detector.apply_bandpass_filter(test_audio)
        
        assert filtered.shape == test_audio.shape
        assert filtered.dtype == np.float32
        # Filtered signal should have less energy overall
        assert np.max(np.abs(filtered)) <= np.max(np.abs(test_audio))
    
    def test_get_spectrum(self, detector, test_audio):
        """Test spectrum generation"""
        freqs, spec = detector.get_spectrum(test_audio)
        
        assert len(freqs) > 0
        assert len(spec) > 0
        assert len(freqs) == len(spec)
        # Check for peak around 1kHz (test frequency)
        peak_idx = np.argmax(spec)
        peak_freq = freqs[peak_idx]
        assert 900 < peak_freq < 1100  # Within 100Hz of 1kHz
    
    def test_detect_anomalies(self, detector, test_audio):
        """Test anomaly detection"""
        events = detector.detect_anomalies(test_audio)
        
        assert isinstance(events, list)
        # May or may not detect depending on thresholds
        if len(events) > 0:
            event = events[0]
            assert isinstance(event, EVPEvent)
            assert event.frequency > 0
            assert 0 <= event.confidence <= 1
    
    def test_process_audio_stream(self, detector, test_audio):
        """Test audio stream processing"""
        result = detector.process_audio_stream(test_audio)
        
        assert isinstance(result, dict)
        assert 'events' in result
        assert 'frequencies' in result
        assert 'spectrum' in result
        assert 'event_count' in result
        assert result['event_count'] >= 0
    
    def test_audio_buffer_management(self, detector, test_audio):
        """Test audio buffer doesn't grow unbounded"""
        # Process several chunks
        for _ in range(10):
            detector.process_audio_stream(test_audio)
        
        # Buffer should be limited
        assert len(detector.audio_buffer) <= detector.sample_rate * 5  # 5 seconds max


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
