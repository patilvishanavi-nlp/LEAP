"""
Data schemas for learning signals.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class SessionState:
    """Tracks current session state."""
    current_step: int = 0
    total_steps_attempted: int = 0
    total_errors: int = 0
    total_hints_used: int = 0
    average_response_time: float = 0.0
    consecutive_errors: int = 0
    
    def update_performance(self, correct: bool, response_time: float):
        """Update performance metrics."""
        self.total_steps_attempted += 1
        if not correct:
            self.total_errors += 1
            self.consecutive_errors += 1
        else:
            self.consecutive_errors = 0
        
        if self.average_response_time == 0:
            self.average_response_time = response_time
        else:
            self.average_response_time = 0.7 * self.average_response_time + 0.3 * response_time