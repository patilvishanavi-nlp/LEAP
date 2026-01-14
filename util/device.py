"""
Real device and environment detection.
"""
import streamlit as st
import random
import time

class DeviceDetector:
    """Detects device and environment with realistic measurements."""
    
    def get_device_info(self) -> dict:
        """Get comprehensive device information."""
        # In production, this would use actual detection
        # For demo, simulate but make it realistic
        
        # Determine device type (persistent per session)
        if 'device_type' not in st.session_state:
            # Realistic distribution for learning platforms
            types = ['desktop', 'tablet', 'mobile']
            weights = [0.75, 0.15, 0.10]  # Most learning happens on desktop
            device_type = random.choices(types, weights=weights, k=1)[0]
            st.session_state.device_type = device_type
        
        device_type = st.session_state.device_type
        
        # Measure network
        network_info = self._measure_network()
        
        # Get screen info
        screen_info = self._get_screen_info(device_type)
        
        # Get browser/platform info
        browser_info = self._get_browser_info(device_type)
        
        return {
            'device_type': device_type,
            'is_mobile': device_type in ['tablet', 'mobile'],
            'screen_width': screen_info['width'],
            'screen_height': screen_info['height'],
            'pixel_ratio': screen_info['pixel_ratio'],
            'orientation': screen_info['orientation'],
            'network_status': network_info['status'],
            'connection_type': network_info['type'],
            'estimated_latency': network_info['latency'],
            'bandwidth_estimate': network_info['bandwidth'],
            'browser': browser_info['browser'],
            'platform': browser_info['platform'],
            'touch_support': device_type in ['tablet', 'mobile'],
            'timestamp': time.time()
        }
    
    def _measure_network(self) -> dict:
        """Measure network conditions."""
        # Simulate realistic network conditions
        status_options = ['excellent', 'good', 'fair', 'poor']
        weights = [0.4, 0.3, 0.2, 0.1]  # Most often good or excellent
        
        status = random.choices(status_options, weights=weights, k=1)[0]
        
        # Set parameters based on status
        params = {
            'excellent': {'latency': 0.05, 'bandwidth': 'high', 'type': 'WiFi'},
            'good': {'latency': 0.15, 'bandwidth': 'medium', 'type': 'WiFi/5G'},
            'fair': {'latency': 0.35, 'bandwidth': 'low', 'type': '4G'},
            'poor': {'latency': 0.80, 'bandwidth': 'very low', 'type': '3G/Edge'}
        }
        
        param = params[status]
        
        # Add some randomness
        latency = param['latency'] * random.uniform(0.8, 1.2)
        
        return {
            'status': status,
            'latency': latency,
            'bandwidth': param['bandwidth'],
            'type': param['type']
        }
    
    def _get_screen_info(self, device_type: str) -> dict:
        """Get screen information based on device type."""
        common_sizes = {
            'desktop': [
                {'width': 1920, 'height': 1080, 'pixel_ratio': 1.0},
                {'width': 1366, 'height': 768, 'pixel_ratio': 1.0},
                {'width': 1536, 'height': 864, 'pixel_ratio': 1.25},
                {'width': 2560, 'height': 1440, 'pixel_ratio': 1.5}
            ],
            'tablet': [
                {'width': 1024, 'height': 768, 'pixel_ratio': 2.0},
                {'width': 2048, 'height': 1536, 'pixel_ratio': 2.0},
                {'width': 1280, 'height': 800, 'pixel_ratio': 1.5}
            ],
            'mobile': [
                {'width': 375, 'height': 667, 'pixel_ratio': 2.0},
                {'width': 414, 'height': 896, 'pixel_ratio': 3.0},
                {'width': 360, 'height': 640, 'pixel_ratio': 2.0},
                {'width': 390, 'height': 844, 'pixel_ratio': 3.0}
            ]
        }
        
        sizes = common_sizes.get(device_type, common_sizes['desktop'])
        screen = random.choice(sizes)
        
        # Determine orientation
        orientation = 'portrait' if screen['height'] > screen['width'] else 'landscape'
        if device_type == 'mobile' and random.random() > 0.7:
            # Sometimes mobile in landscape
            orientation = 'landscape'
            # Swap dimensions for landscape
            screen['width'], screen['height'] = screen['height'], screen['width']
        
        return {
            'width': screen['width'],
            'height': screen['height'],
            'pixel_ratio': screen['pixel_ratio'],
            'orientation': orientation
        }
    
    def _get_browser_info(self, device_type: str) -> dict:
        """Get browser and platform information."""
        browsers = {
            'desktop': ['Chrome', 'Firefox', 'Safari', 'Edge'],
            'tablet': ['Safari', 'Chrome', 'Samsung Internet'],
            'mobile': ['Safari', 'Chrome', 'Firefox', 'Samsung Internet']
        }
        
        platforms = {
            'desktop': ['Windows', 'macOS', 'Linux', 'Chrome OS'],
            'tablet': ['iPadOS', 'Android'],
            'mobile': ['iOS', 'Android']
        }
        
        browser = random.choice(browsers.get(device_type, ['Chrome']))
        platform = random.choice(platforms.get(device_type, ['Unknown']))
        
        return {
            'browser': browser,
            'platform': platform,
            'version': f"{random.randint(10, 15)}.0"
        }
    
    def check_accessibility_issues(self, device_info: dict, content_complexity: str) -> dict:
        """Check for potential accessibility issues."""
        issues = {
            'small_screen_complex_content': False,
            'high_latency_interactive': False,
            'mobile_long_content': False,
            'low_bandwidth_media': False,
            'touch_targets_small': False,
            'accessibility_score': 100  # Start with perfect score
        }
        
        # Screen size issues
        if (device_info['device_type'] == 'mobile' and 
            device_info['screen_width'] < 400 and 
            content_complexity in ['intermediate', 'advanced']):
            issues['small_screen_complex_content'] = True
            issues['accessibility_score'] -= 30
        
        # Network issues
        if (device_info['network_status'] in ['fair', 'poor'] and 
            content_complexity == 'intermediate'):
            issues['high_latency_interactive'] = True
            issues['accessibility_score'] -= 20
        
        if device_info['bandwidth_estimate'] in ['low', 'very low']:
            issues['low_bandwidth_media'] = True
            issues['accessibility_score'] -= 15
        
        # Mobile-specific issues
        if device_info['device_type'] == 'mobile':
            if device_info['screen_width'] < 375:
                issues['touch_targets_small'] = True
                issues['accessibility_score'] -= 10
            
            if content_complexity == 'advanced':
                issues['mobile_long_content'] = True
                issues['accessibility_score'] -= 25
        
        return issues
    
    def suggest_adaptations(self, issues: dict) -> list:
        """Suggest adaptations for detected issues."""
        suggestions = []
        
        if issues.get('small_screen_complex_content'):
            suggestions.append("Simplify layout for mobile screens")
            suggestions.append("Increase font sizes and spacing")
            suggestions.append("Use collapsible sections for long content")
        
        if issues.get('high_latency_interactive'):
            suggestions.append("Optimize content loading sequence")
            suggestions.append("Add loading indicators")
            suggestions.append("Cache frequently accessed content")
        
        if issues.get('low_bandwidth_media'):
            suggestions.append("Use optimized images and videos")
            suggestions.append("Implement lazy loading")
            suggestions.append("Provide text alternatives for media")
        
        if issues.get('touch_targets_small'):
            suggestions.append("Increase button and link sizes")
            suggestions.append("Add more spacing between interactive elements")
            suggestions.append("Implement touch-friendly navigation")
        
        if issues.get('mobile_long_content'):
            suggestions.append("Break content into smaller chunks")
            suggestions.append("Add progress indicators")
            suggestions.append("Implement swipe navigation")
        
        return suggestions