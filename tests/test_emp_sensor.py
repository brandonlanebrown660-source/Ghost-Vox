"""
Unit tests for EMP Sensor Module
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from core.emp_sensor import EMPSensor, EMPReading


@pytest.fixture
def sensor():
    """Create EMP sensor for testing"""
    config = {
        'emp_sensor': {
            'sensitivity': 0.8,
            'baseline_threshold': 50,
            'alert_threshold': 150,
            'averaging_window': 5
        }
    }
    return EMPSensor(config=config)


class TestEMPSensor:
    """Test EMP Sensor functionality"""
    
    def test_initialization(self):
        """Test sensor initialization"""
        sensor = EMPSensor()
        assert sensor.is_calibrated == False
        assert sensor.baseline is None
    
    def test_calibrate_baseline(self, sensor):
        """Test baseline calibration"""
        readings = [45.0, 46.0, 45.5, 46.2, 45.8]
        sensor.calibrate_baseline(readings)
        
        assert sensor.is_calibrated == True
        assert sensor.baseline is not None
        assert 45 < sensor.baseline < 47
    
    def test_detect_anomaly_normal(self, sensor):
        """Test anomaly detection with normal reading"""
        sensor.baseline = 50.0
        is_anomaly, score = sensor.detect_anomaly(60.0)
        
        assert isinstance(score, float)
        assert 0 <= score <= 1
    
    def test_detect_anomaly_high(self, sensor):
        """Test anomaly detection with high reading"""
        sensor.baseline = 50.0
        is_anomaly, score = sensor.detect_anomaly(200.0)
        
        assert is_anomaly == True or score > 0.5
    
    def test_smooth_reading(self, sensor):
        """Test reading smoothing"""
        # Add several readings
        readings = [100, 105, 102, 98, 101]
        smoothed_values = []
        
        for reading in readings:
            smoothed = sensor.smooth_reading(reading)
            smoothed_values.append(smoothed)
        
        # Last smoothed should be average of readings
        expected_avg = sum(readings) / len(readings)
        assert abs(smoothed_values[-1] - expected_avg) < 2
    
    def test_process_reading(self, sensor):
        """Test reading processing"""
        reading = sensor.process_reading(75.0)
        
        assert isinstance(reading, EMPReading)
        assert reading.field_strength > 0
        assert reading.timestamp > 0
        assert 0 <= reading.anomaly_score <= 1
        assert isinstance(reading.is_anomaly, bool)
    
    def test_get_statistics(self, sensor):
        """Test statistics generation"""
        # Process some readings
        for value in [50, 55, 60, 65, 70]:
            sensor.process_reading(value)
        
        stats = sensor.get_statistics()
        
        assert isinstance(stats, dict)
        assert 'current_reading' in stats
        assert 'average_reading' in stats
        assert 'max_reading' in stats
        assert 'min_reading' in stats
        assert stats['max_reading'] >= stats['min_reading']
    
    def test_get_recent_anomalies(self, sensor):
        """Test retrieving recent anomalies"""
        sensor.baseline = 50.0
        sensor.alert_threshold = 100.0
        
        # Generate some high readings to trigger anomalies
        for _ in range(5):
            sensor.process_reading(150.0)
        
        anomalies = sensor.get_recent_anomalies(count=5)
        
        assert isinstance(anomalies, list)
        assert len(anomalies) <= 5
    
    def test_reset_statistics(self, sensor):
        """Test statistics reset"""
        # Add some readings
        for value in [50, 60, 70]:
            sensor.process_reading(value)
        
        # Verify we have data
        assert sensor.readings_count > 0
        
        # Reset
        sensor.reset_statistics()
        
        assert sensor.readings_count == 0
        assert len(sensor.reading_history) == 0
        assert len(sensor.anomaly_history) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
