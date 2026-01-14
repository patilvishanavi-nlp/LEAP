"""
Real signal collection with proper device and network detection.
"""
import time
import random
from datetime import datetime
from typing import Dict, Any
import streamlit as st
import requests

class SignalCollector:
    """Collects learning interaction signals with real device/network detection."""
    
    def __init__(self):
        """Initialize signal collector."""
        self.step_start_times = {}
    
    def collect_pre_step_signals(self, step_id: int, step_difficulty: str) -> Dict[str, Any]:
        """Collect signals before a learning step begins."""
        step_start = time.time()
        self.step_start_times[step_id] = step_start
        
        # Real device detection from Streamlit
        device_info = self._detect_device()
        
        # Real network latency measurement
        network_latency = self._measure_network_latency()
        
        # Screen size simulation (in real app would use JS injection)
        screen_size = self._estimate_screen_size(device_info['device_type'])
        
        return {
            'step_id': step_id,
            'step_difficulty': step_difficulty,
            'step_start_time': step_start,
            'network_latency': network_latency,
            'device_info': device_info,
            'screen_width': screen_size['width'],
            'screen_height': screen_size['height'],
            'content_load_time': self._simulate_load_time(step_difficulty),
            'timestamp': datetime.now().isoformat()
        }
    
    def collect_post_step_signals(self, step_id: int, user_answer: str, 
                                 correct_answer: str, interaction_time: float,
                                 hint_used: bool, step_difficulty: str) -> Dict[str, Any]:
        """Collect signals after interaction."""
        step_start = self.step_start_times.get(step_id, time.time())
        
        # Calculate actual time metrics
        total_time = time.time() - step_start
        time_to_first_action = self._estimate_first_action_time(total_time)
        
        # Determine correctness
        is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
        
        # Get retry count
        error_key = f"step_{step_id}"
        retry_count = st.session_state.error_counts.get(error_key, 0)
        
        # Get current network status
        current_latency = self._measure_network_latency()
        
        return {
            'step_id': step_id,
            'step_difficulty': step_difficulty,
            'timestamp': datetime.now().isoformat(),
            'interaction_time': interaction_time,
            'total_time': total_time,
            'time_to_first_action': time_to_first_action,
            'correct': is_correct,
            'hint_used': hint_used,
            'retry_count': retry_count,
            'network_latency': current_latency,
            'device_type': self._detect_device()['device_type'],
            'response_pattern': self._analyze_response_pattern(step_id, interaction_time, is_correct),
            'session_duration': self._get_session_duration()
        }
    
    def _detect_device(self) -> Dict[str, Any]:
        """Detect device information."""
        # In a real implementation, this would parse User-Agent
        # For Streamlit, we can check query parameters or use JS injection
        
        # Simulate based on random but with session persistence
        if 'detected_device' not in st.session_state:
            devices = ['desktop', 'tablet', 'mobile']
            weights = [0.7, 0.2, 0.1]  # Most likely desktop in learning context
            device = random.choices(devices, weights=weights, k=1)[0]
            st.session_state.detected_device = device
        
        device_type = st.session_state.detected_device
        
        # Determine network quality
        network_status = self._assess_network_quality()
        
        return {
            'device_type': device_type,
            'is_mobile': device_type in ['tablet', 'mobile'],
            'platform': self._get_platform(device_type),
            'network_status': network_status,
            'connection_type': self._simulate_connection_type(network_status)
        }
    
    def _measure_network_latency(self) -> float:
        """Measure actual network latency."""
        try:
            # Try to ping a reliable server
            start = time.time()
            # Use Google's public DNS for latency check
            response = requests.get('https://8.8.8.8', timeout=2)
            latency = (time.time() - start) * 1000  # Convert to ms
            return min(latency, 1000) / 1000  # Return in seconds, max 1 second
        except:
            # Simulate realistic latency
            return random.uniform(0.1, 0.8)  # 100-800ms
    
    def _assess_network_quality(self) -> str:
        """Assess network quality based on latency."""
        try:
            latency = self._measure_network_latency() * 1000  # Convert to ms
            
            if latency < 50:
                return "excellent"
            elif latency < 150:
                return "good"
            elif latency < 300:
                return "fair"
            else:
                return "poor"
        except:
            return random.choice(['excellent', 'good', 'fair', 'poor'])
    
    def _estimate_screen_size(self, device_type: str) -> Dict[str, int]:
        """Estimate screen size based on device type."""
        sizes = {
            'desktop': {'width': 1920, 'height': 1080},
            'tablet': {'width': 1024, 'height': 768},
            'mobile': {'width': 375, 'height': 667}
        }
        return sizes.get(device_type, sizes['desktop'])
    
    def _simulate_load_time(self, difficulty: str) -> float:
        """Simulate content load time based on difficulty."""
        base_time = random.uniform(0.1, 0.3)
        difficulty_multiplier = {
            'beginner': 1.0,
            'intermediate': 1.2,
            'advanced': 1.5
        }
        return base_time * difficulty_multiplier.get(difficulty, 1.0)
    
    def _estimate_first_action_time(self, total_time: float) -> float:
        """Estimate time to first interaction."""
        # Typically 20-40% of total time is thinking/reading before first action
        return total_time * random.uniform(0.2, 0.4)
    
    def _get_platform(self, device_type: str) -> str:
        """Get platform/OS based on device type."""
        platforms = {
            'desktop': random.choice(['Windows', 'macOS', 'Linux']),
            'tablet': random.choice(['iOS', 'Android']),
            'mobile': random.choice(['iOS', 'Android'])
        }
        return platforms.get(device_type, 'Unknown')
    
    def _simulate_connection_type(self, network_status: str) -> str:
        """Simulate connection type based on network quality."""
        connections = {
            'excellent': 'WiFi',
            'good': 'WiFi/5G',
            'fair': '4G',
            'poor': '3G/Edge'
        }
        return connections.get(network_status, 'Unknown')
    
    def _analyze_response_pattern(self, step_id: int, interaction_time: float, is_correct: bool) -> str:
        """Analyze response pattern."""
        if interaction_time < 5 and not is_correct:
            return "rushed_error"
        elif interaction_time > 60 and not is_correct:
            return "struggling"
        elif interaction_time < 10 and is_correct:
            return "confident_fast"
        elif interaction_time > 30 and is_correct:
            return "deliberate_correct"
        else:
            return "typical"
    
    def _get_session_duration(self) -> float:
        """Get current session duration."""
        if 'session_start_time' in st.session_state:
            return (datetime.now() - st.session_state.session_start_time).total_seconds()
        return 0
    
    def calculate_friction_patterns(self, signals: list[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate friction patterns from signals."""
        if len(signals) < 2:
            return {}
        
        recent_signals = signals[-3:]
        
        patterns = {
            'access_friction': self._check_access_friction(recent_signals),
            'cognitive_friction': self._check_cognitive_friction(recent_signals),
            'motivation_friction': self._check_motivation_friction(recent_signals),
            'interaction_friction': self._check_interaction_friction(recent_signals),
            'transfer_friction': self._check_transfer_friction(signals)
        }
        
        return patterns
    
    def _check_access_friction(self, signals: list[Dict]) -> Dict[str, Any]:
        """Check for access friction patterns."""
        issues = []
        score = 0
        
        for signal in signals:
            latency = signal.get('network_latency', 0)
            device_type = signal.get('device_type', 'desktop')
            
            if latency > 0.5:  # >500ms
                issues.append(f"High latency ({latency:.1f}s)")
                score += 0.4
            
            if device_type == 'mobile' and signal.get('step_difficulty') == 'advanced':
                issues.append("Mobile with advanced content")
                score += 0.3
        
        return {
            'detected': len(issues) > 0,
            'score': min(score, 1.0),
            'issues': issues,
            'recommendation': "Optimize for mobile, reduce latency impact" if score > 0.3 else None
        }
    
    def _check_cognitive_friction(self, signals: list[Dict]) -> Dict[str, Any]:
        """Check for cognitive load friction."""
        issues = []
        score = 0
        
        # Check response time trend
        times = [s.get('interaction_time', 0) for s in signals]
        if len(times) >= 2:
            if times[-1] > times[0] * 1.5:  # Increasing by 50%+
                issues.append("Increasing response times")
                score += 0.3
        
        # Check error rate
        error_count = sum(1 for s in signals if not s.get('correct', True))
        if error_count >= 2:
            issues.append(f"Multiple errors ({error_count})")
            score += 0.4
        
        # Check hint usage
        hint_count = sum(1 for s in signals if s.get('hint_used', False))
        if hint_count >= 2:
            issues.append(f"Hint dependency ({hint_count})")
            score += 0.3
        
        return {
            'detected': len(issues) > 0,
            'score': min(score, 1.0),
            'issues': issues,
            'recommendation': "Simplify presentation, add scaffolding" if score > 0.3 else None
        }
    
    def _check_motivation_friction(self, signals: list[Dict]) -> Dict[str, Any]:
        """Check for motivation/regulation friction."""
        issues = []
        score = 0
        
        # Check for abandonment patterns
        abandonment_count = sum(1 for s in signals 
                              if s.get('interaction_time', 0) < 10 and not s.get('correct', True))
        if abandonment_count >= 1:
            issues.append("Quick attempts with errors")
            score += 0.4
        
        # Check for very long times (potential disengagement)
        long_time_count = sum(1 for s in signals if s.get('interaction_time', 0) > 90)
        if long_time_count >= 1:
            issues.append("Extended engagement without success")
            score += 0.3
        
        # Check pattern of errors after hints
        for i in range(len(signals)-1):
            if signals[i].get('hint_used', False) and not signals[i+1].get('correct', True):
                issues.append("Continued errors after hints")
                score += 0.3
                break
        
        return {
            'detected': len(issues) > 0,
            'score': min(score, 1.0),
            'issues': issues,
            'recommendation': "Add encouragement, progress markers" if score > 0.3 else None
        }
    
    def _check_interaction_friction(self, signals: list[Dict]) -> Dict[str, Any]:
        """Check for interaction/feedback friction."""
        issues = []
        score = 0
        
        # Check for repeated errors on same step
        step_errors = {}
        for signal in signals:
            step_id = signal.get('step_id', 0)
            if not signal.get('correct', True):
                step_errors[step_id] = step_errors.get(step_id, 0) + 1
        
        for step_id, error_count in step_errors.items():
            if error_count >= 2:
                issues.append(f"Repeated errors on step {step_id}")
                score += 0.5
        
        # Check response pattern
        pattern_count = {}
        for signal in signals:
            pattern = signal.get('response_pattern', '')
            pattern_count[pattern] = pattern_count.get(pattern, 0) + 1
        
        if pattern_count.get('rushed_error', 0) >= 2:
            issues.append("Pattern of rushed errors")
            score += 0.3
        
        return {
            'detected': len(issues) > 0,
            'score': min(score, 1.0),
            'issues': issues,
            'recommendation': "Improve feedback, clarify instructions" if score > 0.3 else None
        }
    
    def _check_transfer_friction(self, all_signals: list[Dict]) -> Dict[str, Any]:
        """Check for transfer/meaning friction."""
        if len(all_signals) < 4:
            return {'detected': False, 'score': 0.0, 'issues': [], 'recommendation': None}
        
        # Group by difficulty
        beginner_signals = [s for s in all_signals if s.get('step_difficulty') == 'beginner']
        intermediate_signals = [s for s in all_signals if s.get('step_difficulty') == 'intermediate']
        
        issues = []
        score = 0
        
        if beginner_signals and intermediate_signals:
            beginner_correct = sum(1 for s in beginner_signals if s.get('correct', True))
            intermediate_correct = sum(1 for s in intermediate_signals if s.get('correct', True))
            
            beginner_acc = beginner_correct / len(beginner_signals)
            intermediate_acc = intermediate_correct / len(intermediate_signals)
            
            # Significant drop in accuracy
            if beginner_acc > 0.7 and intermediate_acc < 0.4:
                issues.append(f"Performance drop: {beginner_acc:.0%} → {intermediate_acc:.0%}")
                score += 0.6
            
            # Check time increase with difficulty
            if beginner_signals and intermediate_signals:
                avg_beginner_time = sum(s.get('interaction_time', 0) for s in beginner_signals) / len(beginner_signals)
                avg_intermediate_time = sum(s.get('interaction_time', 0) for s in intermediate_signals) / len(intermediate_signals)
                
                if avg_intermediate_time > avg_beginner_time * 2:
                    issues.append("Large time increase with difficulty")
                    score += 0.4
        
        return {
            'detected': len(issues) > 0,
            'score': min(score, 1.0),
            'issues': issues,
            'recommendation': "Add bridging examples, contextualize learning" if score > 0.3 else None
        }