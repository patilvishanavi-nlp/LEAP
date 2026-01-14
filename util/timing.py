"""
Timing utilities for measuring interactions.
"""
import time
from datetime import datetime
from typing import Optional, Dict, Any
import streamlit as st

class Timer:
    """High-precision timer for learning interactions."""
    
    def __init__(self):
        """Initialize timer."""
        self.start_times = {}
        self.interaction_records = []
    
    def start_step(self, step_id: int) -> None:
        """Start timing a learning step."""
        self.start_times[step_id] = {
            'start': time.perf_counter(),
            'first_interaction': None,
            'pauses': []
        }
    
    def record_first_interaction(self, step_id: int) -> Optional[float]:
        """
        Record first interaction time for a step.
        
        Returns:
            Time to first interaction in seconds, or None
        """
        if step_id not in self.start_times:
            return None
        
        if self.start_times[step_id]['first_interaction'] is None:
            elapsed = time.perf_counter() - self.start_times[step_id]['start']
            self.start_times[step_id]['first_interaction'] = elapsed
            return elapsed
        
        return None
    
    def record_pause(self, step_id: int) -> None:
        """Record a pause in interaction."""
        if step_id in self.start_times:
            current_time = time.perf_counter()
            self.start_times[step_id]['pauses'].append(current_time)
    
    def end_step(self, step_id: int) -> Dict[str, Any]:
        """
        End timing for a step and return metrics.
        
        Returns:
            Dictionary of timing metrics
        """
        if step_id not in self.start_times:
            return {}
        
        end_time = time.perf_counter()
        start_data = self.start_times[step_id]
        
        total_time = end_time - start_data['start']
        first_interaction = start_data.get('first_interaction', total_time)
        
        # Calculate pause metrics
        pauses = start_data.get('pauses', [])
        pause_count = len(pauses)
        
        # Estimate pause duration (simplified)
        total_pause_time = 0
        if pause_count > 1:
            # Assume pauses are between interactions
            total_pause_time = pause_count * 2.0  # Simplified
        
        # Calculate active time
        active_time = total_time - total_pause_time
        
        metrics = {
            'step_id': step_id,
            'total_time': total_time,
            'active_time': active_time,
            'time_to_first_interaction': first_interaction,
            'pause_count': pause_count,
            'estimated_pause_time': total_pause_time,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store in session for analysis
        if 'timing_metrics' not in st.session_state:
            st.session_state.timing_metrics = []
        
        st.session_state.timing_metrics.append(metrics)
        
        # Clean up
        del self.start_times[step_id]
        
        return metrics
    
    def get_step_timing_pattern(self, step_id: int) -> str:
        """
        Get timing pattern for a step.
        
        Returns:
            Pattern description
        """
        metrics = self.end_step(step_id) if step_id in self.start_times else {}
        
        if not metrics:
            return "no_data"
        
        total_time = metrics.get('total_time', 0)
        first_interaction = metrics.get('time_to_first_interaction', total_time)
        pause_count = metrics.get('pause_count', 0)
        
        # Pattern detection
        if first_interaction > total_time * 0.5:
            return "delayed_start"
        elif pause_count > 3:
            return "frequent_pauses"
        elif total_time > 300:  # 5 minutes
            return "extended_engagement"
        elif total_time < 30:  # 30 seconds
            return "rapid_response"
        else:
            return "typical"