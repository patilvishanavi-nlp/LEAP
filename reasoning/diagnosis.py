"""
Friction diagnosis engine using Gemini API.
"""
import json
import os
from typing import Dict, List, Optional, Any
import google as genai
from dotenv import load_dotenv

from .prompts import SystemPrompts
from signals.collector import SignalCollector

# Load environment variables
load_dotenv()

class FrictionDiagnosisEngine:
    """Engine for diagnosing learning friction using Gemini."""
    
    def __init__(self, api_key: str = None):
        """Initialize the diagnosis engine with Gemini."""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        # Initialize Gemini client with new API
        import google.genai
        self.client = google.genai.Client(api_key=self.api_key)
        
        # Initialize signal collector for pattern detection
        self.signal_collector = SignalCollector()
    
    def diagnose(self, signals: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Diagnose friction patterns from signals.
        
        Args:
            signals: List of learning interaction signals
            
        Returns:
            Diagnosis result with friction and adaptation, or None
        """
        try:
            # Calculate signal patterns
            signal_patterns = self.signal_collector.calculate_signal_patterns(signals)
            
            # Skip diagnosis if no concerning patterns
            if not any(signal_patterns.values()):
                return None
            
            # Get diagnosis prompt
            prompt = SystemPrompts.get_diagnosis_prompt(signals, signal_patterns)
            
            # Call Gemini
            response = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt)
            
            # Parse response
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[json_start:json_end]
            result = json.loads(json_str)
            
            # Validate result structure
            self._validate_diagnosis_result(result)
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text if 'response_text' in locals() else 'No response'}")
            return None
        except Exception as e:
            print(f"Diagnosis error: {e}")
            return None
    
    def _validate_diagnosis_result(self, result: Dict[str, Any]) -> None:
        """Validate the structure of diagnosis result."""
        required_keys = ['frictions_detected', 'evidence', 'adaptation', 'justification']
        
        for key in required_keys:
            if key not in result:
                raise ValueError(f"Missing required key: {key}")
        
        if not isinstance(result['frictions_detected'], list):
            raise ValueError("frictions_detected must be a list")
        
        if not isinstance(result['evidence'], dict):
            raise ValueError("evidence must be a dictionary")
        
        # Check that evidence matches frictions
        for friction in result['frictions_detected']:
            if friction not in result['evidence']:
                raise ValueError(f"Evidence missing for friction: {friction}")
    
    def get_adaptation_implementation(
        self, 
        learning_step: Dict[str, Any], 
        adaptation: str,
        explanation_style: str = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get implementation details for an adaptation.
        
        Args:
            learning_step: The original learning step
            adaptation: The adaptation to apply
            explanation_style: Optional style constraint
            
        Returns:
            Adapted learning step
        """
        try:
            # Get implementation prompt
            prompt = SystemPrompts.get_adaptation_implementation_prompt(
                learning_step, 
                adaptation, 
                explanation_style
            )
            
            # Call Gemini
            response = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt)
            response_text = response.text.strip()
            
            # Extract JSON
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[json_start:json_end]
            result = json.loads(json_str)
            
            return result
            
        except Exception as e:
            print(f"Adaptation implementation error: {e}")
            # Return original step as fallback
            return {
                'adapted_title': learning_step.get('title'),
                'adapted_content': learning_step.get('content'),
                'adapted_task': learning_step.get('task'),
                'adaptation_type': 'fallback_original',
                'explanation_style_used': explanation_style or 'none'
            }