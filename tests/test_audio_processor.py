"""
Unit tests for Audio Processor Module
"""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from core.audio_processor import AudioProcessor, AudioFrame


@pytest.fixture
def processor():
    """Create audio processor for testing"""
    config = {
        'audio': {
            'sample_rate': 44100,
            'channels': 1,
            'chunk_size': 2048,
            'device_index': -1
        }
    }
    return AudioProcessor(config=config)


class TestAudioProcessor:
    """Test Audio Processor functionality"""
    
    def test_initialization(self):
        """Test processor initialization"""
        processor = AudioProcessor()
        assert processor.sample_rate == 44100
        assert processor.channels == 1
        assert processor.is_recording == False
    
    def test_normalize_audio(self, processor):
        """Test audio normalization"""
        audio = np.array([0.5, -0.3, 0.8, -0.2], dtype=np.float32)
        normalized = processor.normalize_audio(audio)
        
        # Max value should be 1.0
        assert np.max(np.abs(normalized)) <= 1.0
    
    def test_apply_window(self, processor):
        """Test window function application"""
        audio = np.ones(2048, dtype=np.float32)
        windowed = processor.apply_window(audio, window_type='hann')
        
        # Windowed should have reduced edges
        assert windowed[0] < audio[0]
        assert windowed[-1] < audio[-1]
        assert windowed.shape == audio.shape
    
    def test_get_rms_level(self, processor):
        """Test RMS level calculation"""
        # Generate sine wave
        sample_rate = 44100
        duration = 0.1
        frequency = 1000.0
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        signal = np.sin(2 * np.pi * frequency * t).astype(np.float32)
        
        rms = processor.get_rms_level(signal)
        
        assert rms > 0
        # RMS of sine wave should be ~0.707
        assert 0.6 < rms < 0.75
    
    def test_get_statistics(self, processor):
        """Test statistics generation"""
        stats = processor.get_statistics()
        
        assert isinstance(stats, dict)
        assert 'sample_rate' in stats
        assert 'channels' in stats
        assert 'is_recording' in stats
        assert 'frames_captured' in stats
    
    def test_audio_frame_creation(self):
        """Test AudioFrame creation"""
        data = np.random.rand(2048).astype(np.float32)
        frame = AudioFrame(
            data=data,
            timestamp=1234567.89,
            frame_number=42
        )
        
        assert frame.frame_number == 42
        assert frame.timestamp == 1234567.89
        assert np.array_equal(frame.data, data)
    
    def test_get_input_devices(self, processor):
        """Test device listing"""
        # This may not work in all test environments
        try:
            devices = processor.get_input_devices()
            assert isinstance(devices, list)
            
            if len(devices) > 0:
                device = devices[0]
                assert 'index' in device
                assert 'name' in device
                assert 'channels' in device
        except Exception:
            # PyAudio may not be available in test environment
            pass
    
    def test_queue_management(self, processor):
        """Test audio queue management"""
        assert processor.audio_queue.empty()
        
        # Check queue attributes
        assert processor.audio_queue.maxsize > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
