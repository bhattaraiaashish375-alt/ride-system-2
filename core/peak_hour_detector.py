"""Peak Hour Detection and Surge Pricing Analyzer"""

from datetime import datetime, time
from config.fare_config import TIME_PERIODS


class PeakHourDetector:
    """Detect peak hours and calculate surge pricing"""
    
    def __init__(self):
        self.peak_periods = {
            'morning': {'start': 6, 'end': 9, 'surge_bike': 0.35, 'surge_car': 0.30},
            'evening': {'start': 16, 'end': 21, 'surge_bike': 0.40, 'surge_car': 0.35},
        }
        self.off_peak_periods = {
            'day': {'start': 9, 'end': 16, 'surge': 0},
            'night': {'start': 21, 'end': 6, 'surge_bike': 0.15, 'surge_car': 0.20},
        }
    
    def is_peak_hour(self, current_time=None):
        """Check if current time is peak hour
        
        Args:
            current_time: str in format 'HH:MM' or None (uses current time)
            
        Returns:
            dict: {'is_peak': bool, 'period': str, 'surge_level': str}
        """
        if current_time is None:
            current_time = datetime.now().strftime('%H:%M')
        
        hour = int(current_time.split(':')[0])
        minute = int(current_time.split(':')[1])
        total_minutes = hour * 60 + minute
        
        # Check peak periods
        for period, times in self.peak_periods.items():
            period_start = times['start'] * 60
            period_end = times['end'] * 60
            
            if period_start <= total_minutes < period_end:
                return {
                    'is_peak': True,
                    'period': period,
                    'surge_level': 'HIGH',
                    'time': current_time
                }
        
        # Check night period (wraps around midnight)
        night_start = 21 * 60
        night_end = 6 * 60
        
        if total_minutes >= night_start or total_minutes < night_end:
            return {
                'is_peak': False,
                'period': 'night',
                'surge_level': 'LOW',
                'time': current_time
            }
        
        # Day period
        return {
            'is_peak': False,
            'period': 'day',
            'surge_level': 'NONE',
            'time': current_time
        }
    
    def get_surge_percentage(self, period, vehicle_type='bike'):
        """Get surge percentage for a specific period
        
        Args:
            period: str - 'morning', 'day', 'evening', 'night'
            vehicle_type: str - 'bike' or 'car'
            
        Returns:
            float: Surge percentage (0.0 to 1.0)
        """
        if period in self.peak_periods:
            surge_key = f"surge_{vehicle_type}"
            return self.peak_periods[period].get(surge_key, 0)
        
        if period in self.off_peak_periods:
            return self.off_peak_periods[period].get('surge', 0)
        
        return 0
    
    def get_surge_info(self, current_time=None, base_fare=100, vehicle_type='bike'):
        """Get complete surge pricing information
        
        Args:
            current_time: str or None
            base_fare: int - Base fare for calculation
            vehicle_type: str - 'bike' or 'car'
            
        Returns:
            dict: Complete surge information
        """
        peak_info = self.is_peak_hour(current_time)
        period = peak_info['period']
        surge_percentage = self.get_surge_percentage(period, vehicle_type)
        surge_amount = int(base_fare * surge_percentage)
        total_fare = base_fare + surge_amount
        
        return {
            'current_time': peak_info['time'],
            'period': period,
            'is_peak': peak_info['is_peak'],
            'surge_level': peak_info['surge_level'],
            'base_fare': base_fare,
            'surge_percentage': surge_percentage,
            'surge_amount': surge_amount,
            'total_fare': total_fare,
            'warning': "High surge pricing detected!" if peak_info['is_peak'] else None
        }
    
    def get_peak_hour_warnings(self, current_time=None):
        """Get peak hour warnings and recommendations
        
        Args:
            current_time: str or None
            
        Returns:
            dict: Warnings and recommendations
        """
        peak_info = self.is_peak_hour(current_time)
        
        warnings = []
        recommendations = []
        
        if peak_info['is_peak']:
            warnings.append(f"⚠️ PEAK HOUR ({peak_info['period'].upper()}): Fares will be significantly higher!")
            recommendations.append("Consider delaying your ride by 30-60 minutes for lower fares")
            recommendations.append("Bike rides may offer better value during this period")
        else:
            recommendations.append("✅ Good time to book! Fares are at standard rates.")
        
        return {
            'period': peak_info['period'],
            'is_peak': peak_info['is_peak'],
            'warnings': warnings,
            'recommendations': recommendations
        }
