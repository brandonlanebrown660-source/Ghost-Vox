"""
EMP (Electromagnetic Field) Sensor Module

Interfaces with electromagnetic field sensors to detect and log
anomalous readings and activity patterns.
"""

import logging
import time
from typing import Dict, List, Tuple
from dataclasses import dataclass
from collections import deque


logger = logging.getLogger(__name__)


@dataclass
class EMPReading:
    """Represents a single EMP sensor reading"""
    timestamp: float
    field_strength: float  # in mV or equivalent
    frequency: float  # Hz
    anomaly_score: float  # 0-1
    is_anomaly: bool


class EMPSensor:
    """
    Detects Electromagnetic Field phenomena
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize EMP Sensor
        
        Args:
            config: Configuration dictionary with EMP parameters
        """
        self.config = config or {}
        
        # Sensor parameters
        self.sensitivity = self.config.get('emp_sensor', {}).get('sensitivity', 0.8)
        self.baseline_threshold = self.config.get('emp_sensor', {}).get('baseline_threshold', 50)
        self.alert_threshold = self.config.get('emp_sensor', {}).get('alert_threshold', 150)
        self.sampling_interval_ms = self.config.get('emp_sensor', {}).get('sampling_interval_ms', 100)
        self.averaging_window = self.config.get('emp_sensor', {}).get('averaging_window', 10)
        
        # Baseline and calibration
        self.baseline = None
        self.is_calibrated = False
        self.last_reading_time = time.time()
        
        # Reading history
        self.reading_history = deque(maxlen=1000)
        self.anomaly_history = deque(maxlen=100)
        
        # Statistics
        self.max_reading = 0
        self.min_reading = float('inf')
        self.readings_count = 0
        
        logger.info("EMP Sensor initialized")
    
    def calibrate_baseline(self, readings: List[float]):
        """
        Calibrate baseline from quiet environment readings
        
        Args:
            readings: List of baseline readings
        """
        logger.info("Calibrating EMP baseline...")
        
        if len(readings) == 0:
            logger.warning("No readings provided for calibration")
            self.baseline = self.baseline_threshold
            return
        
        self.baseline = sum(readings) / len(readings)
        self.is_calibrated = True
        
        logger.info(f"Baseline calibrated: {self.baseline:.2f} mV")
    
    def detect_anomaly(self, field_strength: float) -> Tuple[bool, float]:
        """
        Detect if reading represents an anomaly
        
        Args:
            field_strength: Current field strength reading
            
        Returns:
            Tuple of (is_anomaly, anomaly_score)
        """
        if self.baseline is None:
            # Use default threshold if not calibrated
            anomaly_threshold = self.baseline_threshold
        else:
            # Anomaly threshold relative to baseline
            anomaly_threshold = self.baseline + (self.alert_threshold - self.baseline) * self.sensitivity
        
        # Calculate deviation from baseline
        if self.baseline is not None:
            deviation = abs(field_strength - self.baseline)
        else:
            deviation = field_strength
        
        # Anomaly score (0-1)
        anomaly_score = min(deviation / (self.alert_threshold * 2), 1.0)
        
        # Determine if anomaly
        is_anomaly = field_strength > anomaly_threshold
        
        return is_anomaly, anomaly_score
    
    def smooth_reading(self, new_reading: float) -> float:
        """
        Apply moving average smoothing to reduce noise
        
        Args:
            new_reading: New sensor reading
            
        Returns:
            Smoothed reading value
        """
        self.reading_history.append(new_reading)
        
        if len(self.reading_history) == 0:
            return new_reading
        
        # Use averaging window
        window_size = min(self.averaging_window, len(self.reading_history))
        recent_readings = list(self.reading_history)[-window_size:]
        smoothed = sum(recent_readings) / len(recent_readings)
        
        return smoothed
    
    def process_reading(self, field_strength: float) -> EMPReading:
        """
        Process a raw EMP sensor reading
        
        Args:
            field_strength: Raw field strength value
            
        Returns:
            Processed EMPReading object
        """
        current_time = time.time()
        
        # Smooth the reading
        smoothed = self.smooth_reading(field_strength)
        
        # Update statistics
        self.max_reading = max(self.max_reading, smoothed)
        self.min_reading = min(self.min_reading, smoothed)
        self.readings_count += 1
        
        # Detect anomalies
        is_anomaly, anomaly_score = self.detect_anomaly(smoothed)
        
        # Estimate frequency (simplified - in real implementation, would analyze patterns)
        frequency = self.estimate_frequency(smoothed)
        
        # Create reading object
        reading = EMPReading(
            timestamp=current_time,
            field_strength=smoothed,
            frequency=frequency,
            anomaly_score=anomaly_score,
            is_anomaly=is_anomaly
        )
        
        # Track anomalies
        if is_anomaly:
            self.anomaly_history.append(reading)
            logger.warning(f"EMP Anomaly detected: {smoothed:.2f} mV (Score: {anomaly_score:.2f})")
        
        self.last_reading_time = current_time
        
        return reading
    
    def estimate_frequency(self, field_strength: float) -> float:
        """
        Estimate electromagnetic frequency from reading
        
        Args:
            field_strength: Current field strength
            
        Returns:
            Estimated frequency in Hz
        """
        # Simplified frequency estimation based on field strength
        # In real implementation, would analyze temporal patterns
        
        if field_strength < self.baseline_threshold:
            return 50.0  # Common AC frequency
        elif field_strength < self.alert_threshold:
            return 60.0  # Alternative AC frequency
        else:
            # Anomalous - could be variable frequency
            return 50.0 + (field_strength - self.alert_threshold) * 0.1
    
    def get_statistics(self) -> Dict:
        """
        Get sensor statistics
        
        Returns:
            Dictionary with sensor statistics
        """
        total_readings = len(self.reading_history)
        total_anomalies = len(self.anomaly_history)
        
        if total_readings == 0:
            avg_reading = 0
            current_reading = 0
        else:
            current_reading = self.reading_history[-1] if self.reading_history else 0
            avg_reading = sum(self.reading_history) / len(self.reading_history)
        
        return {
            'baseline': self.baseline,
            'is_calibrated': self.is_calibrated,
            'current_reading': current_reading,
            'average_reading': avg_reading,
            'max_reading': self.max_reading,
            'min_reading': self.min_reading,
            'total_readings': self.readings_count,
            'recent_readings': list(self.reading_history),
            'anomalies_detected': total_anomalies,
            'anomaly_percentage': (total_anomalies / total_readings * 100) if total_readings > 0 else 0,
            'sensitivity': self.sensitivity,
            'baseline_threshold': self.baseline_threshold,
            'alert_threshold': self.alert_threshold
        }
    
    def get_recent_anomalies(self, count: int = 10) -> List[EMPReading]:
        """
        Get recent anomalies
        
        Args:
            count: Number of recent anomalies to return
            
        Returns:
            List of recent EMPReading anomalies
        """
        anomalies = list(self.anomaly_history)
        return anomalies[-count:] if anomalies else []
    
    def reset_statistics(self):
        """Reset sensor statistics"""
        self.reading_history.clear()
        self.anomaly_history.clear()
        self.max_reading = 0
        self.min_reading = float('inf')
        self.readings_count = 0
        logger.info("EMP sensor statistics reset")
