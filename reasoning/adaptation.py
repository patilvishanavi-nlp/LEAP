"""
Adaptation logic and mappings for different friction types.
"""
from typing import Dict, List, Optional, Any
from enum import Enum

class AdaptationType(str, Enum):
    """Types of environment adaptations."""
    PACING = "pacing"
    SEQUENCING = "sequencing"
    STRUCTURE = "structure"
    MODALITY = "modality"
    FEEDBACK_TIMING = "feedback_timing"
    CONTEXTUAL_FRAMING = "contextual_framing"

class AdaptationMapper:
    """Maps friction types to appropriate adaptations."""
    
    # Mapping from friction patterns to suggested adaptations
    FRICTION_TO_ADAPTATION = {
        # Cognitive load patterns
        'cognitive_overload': {
            'type': AdaptationType.STRUCTURE,
            'suggestions': [
                "Break complex step into smaller sub-steps",
                "Add progressive disclosure of information",
                "Provide worked example before practice",
                "Add visual organizers or concept maps"
            ]
        },
        'increasing_response_time': {
            'type': AdaptationType.PACING,
            'suggestions': [
                "Add time indicators or progress bars",
                "Insert interim checkpoints",
                "Provide estimated time reminders",
                "Allow self-paced advancement"
            ]
        },
        
        # Access friction patterns
        'access_issues': {
            'type': AdaptationType.STRUCTURE,
            'suggestions': [
                "Restructure for vertical scrolling on mobile",
                "Increase interactive element size",
                "Simplify navigation paths",
                "Optimize content loading sequence"
            ]
        },
        
        # Motivation patterns
        'motivation_dip': {
            'type': AdaptationType.CONTEXTUAL_FRAMING,
            'suggestions': [
                "Add progress indicators and completion markers",
                "Insert micro-success milestones",
                "Provide encouraging feedback on effort",
                "Connect to practical applications"
            ]
        },
        
        # Error patterns
        'error_clustering': {
            'type': AdaptationType.FEEDBACK_TIMING,
            'suggestions': [
                "Provide immediate error prevention hints",
                "Break feedback into smaller, actionable chunks",
                "Add confirmatory checks before submission",
                "Offer targeted practice on specific sub-skills"
            ]
        },
        
        # Hint dependency
        'hint_dependency': {
            'type': AdaptationType.SEQUENCING,
            'suggestions': [
                "Present foundational concepts before application",
                "Sequence from simple to complex examples",
                "Add scaffolding that fades gradually",
                "Provide multiple solution pathways"
            ]
        }
    }
    
    @staticmethod
    def get_adaptation_for_patterns(patterns: Dict[str, bool]) -> Optional[str]:
        """
        Get appropriate adaptation for detected patterns.
        
        Args:
            patterns: Dictionary of pattern booleans
            
        Returns:
            Adaptation suggestion or None
        """
        # Prioritize patterns
        priority_order = [
            'cognitive_overload',
            'access_issues',
            'motivation_dip',
            'error_clustering',
            'hint_dependency',
            'increasing_response_time',
            'abandonment_pattern'
        ]
        
        # Find first matching pattern
        for pattern in priority_order:
            if patterns.get(pattern):
                adaptations = AdaptationMapper.FRICTION_TO_ADAPTATION.get(pattern, {})
                suggestions = adaptations.get('suggestions', [])
                if suggestions:
                    return suggestions[0]  # Return first suggestion
        
        return None
    
    @staticmethod
    def validate_adaptation(adaptation: str, original_step: Dict[str, Any]) -> bool:
        """
        Validate that an adaptation preserves learning goals.
        
        Args:
            adaptation: The adaptation description
            original_step: Original learning step
            
        Returns:
            True if adaptation is valid
        """
        # Invalid adaptations (these would change learning goals)
        invalid_indicators = [
            "simplify", "make easier", "reduce difficulty",
            "remove", "skip", "avoid",
            "change answer", "different solution",
            "permanent", "always", "forever"
        ]
        
        adaptation_lower = adaptation.lower()
        
        # Check for invalid indicators
        for indicator in invalid_indicators:
            if indicator in adaptation_lower:
                return False
        
        # Check that adaptation is environment-focused
        environment_focus = any(
            term in adaptation_lower 
            for term in ['present', 'structure', 'pace', 'sequence', 
                        'format', 'organize', 'timing', 'feedback']
        )
        
        return environment_focus

class AdaptationApplier:
    """Applies adaptations to learning steps."""
    
    @staticmethod
    def apply_adaptation(
        learning_step: Dict[str, Any],
        adaptation: str,
        explanation_style: str = None
    ) -> Dict[str, Any]:
        """
        Apply an adaptation to a learning step.
        
        Args:
            learning_step: Original learning step
            adaptation: Adaptation to apply
            explanation_style: Optional presentation style
            
        Returns:
            Adapted learning step
        """
        # Start with original
        adapted = learning_step.copy()
        
        # Apply adaptation based on type
        adaptation_lower = adaptation.lower()
        
        # Pacing adaptations
        if any(term in adaptation_lower for term in ['pace', 'time', 'progress', 'checkpoint']):
            adapted = AdaptationApplier._apply_pacing_adaptation(adapted, adaptation)
        
        # Structure adaptations
        elif any(term in adaptation_lower for term in ['structure', 'break', 'organize', 'chunk']):
            adapted = AdaptationApplier._apply_structure_adaptation(adapted, adaptation)
        
        # Sequencing adaptations
        elif any(term in adaptation_lower for term in ['sequence', 'order', 'arrange']):
            adapted = AdaptationApplier._apply_sequencing_adaptation(adapted, adaptation)
        
        # Feedback adaptations
        elif any(term in adaptation_lower for term in ['feedback', 'hint', 'confirm']):
            adapted = AdaptationApplier._apply_feedback_adaptation(adapted, adaptation)
        
        # Contextual adaptations
        elif any(term in adaptation_lower for term in ['context', 'frame', 'relevance', 'application']):
            adapted = AdaptationApplier._apply_contextual_adaptation(adapted, adaptation)
        
        # Apply explanation style if specified
        if explanation_style:
            adapted = AdaptationApplier._apply_explanation_style(adapted, explanation_style)
        
        # Mark as adapted
        adapted['adaptation_applied'] = adaptation
        adapted['is_adapted'] = True
        
        return adapted
    
    @staticmethod
    def _apply_pacing_adaptation(step: Dict[str, Any], adaptation: str) -> Dict[str, Any]:
        """Apply pacing-related adaptations."""
        content = step.get('content', '')
        task = step.get('task', '')
        
        # Add pacing elements
        pacing_elements = [
            "\n\n---\n**Progress Checkpoint**",
            "\n\n🕐 *Estimated time: Take your time with this concept*",
            "\n\n📊 *You're making progress!*",
            "\n\n⏸️ *Pause point: Consider what you've learned so far*"
        ]
        
        # Select appropriate pacing element
        if 'progress' in adaptation.lower():
            content += pacing_elements[0]
        elif 'time' in adaptation.lower():
            content += pacing_elements[1]
        elif 'checkpoint' in adaptation.lower():
            content += pacing_elements[3]
        else:
            content += pacing_elements[2]
        
        step['content'] = content
        return step
    
    @staticmethod
    def _apply_structure_adaptation(step: Dict[str, Any], adaptation: str) -> Dict[str, Any]:
        """Apply structure-related adaptations."""
        content = step.get('content', '')
        
        # Add structural elements
        if 'break' in adaptation.lower() or 'chunk' in adaptation.lower():
            # Add section headers
            lines = content.split('\n')
            if len(lines) > 4:
                # Insert section break
                midpoint = len(lines) // 2
                lines.insert(midpoint, '\n---\n**Key Concept**\n')
                content = '\n'.join(lines)
        
        # Add visual organization
        if 'organize' in adaptation.lower():
            content = content.replace('\n\n', '\n\n• ')
            if not content.startswith('• '):
                content = '• ' + content
        
        step['content'] = content
        return step
    
    @staticmethod
    def _apply_sequencing_adaptation(step: Dict[str, Any], adaptation: str) -> Dict[str, Any]:
        """Apply sequencing-related adaptations."""
        content = step.get('content', '')
        
        # Add sequencing cues
        if 'example' in adaptation.lower() and 'before' in adaptation.lower():
            # Ensure examples come before practice
            if 'Example:' in content and 'Your Task:' in content:
                # Already properly sequenced
                pass
            else:
                # Add sequencing language
                content = "First, let's look at an example:\n\n" + content
                if 'task' in step:
                    step['task'] = "Now try applying what you learned:\n\n" + step['task']
        
        step['content'] = content
        return step
    
    @staticmethod
    def _apply_feedback_adaptation(step: Dict[str, Any], adaptation: str) -> Dict[str, Any]:
        """Apply feedback-related adaptations."""
        task = step.get('task', '')
        
        # Add feedback mechanisms
        if 'confirm' in adaptation.lower():
            task += "\n\n💡 *Tip: Before submitting, double-check your reasoning.*"
        elif 'hint' in adaptation.lower():
            if 'hints' in step and step['hints']:
                task += f"\n\n🔍 *Remember: You can use hints if you get stuck.*"
        
        step['task'] = task
        return step
    
    @staticmethod
    def _apply_contextual_adaptation(step: Dict[str, Any], adaptation: str) -> Dict[str, Any]:
        """Apply contextual framing adaptations."""
        content = step.get('content', '')
        
        # Add contextual framing
        if 'relevance' in adaptation.lower() or 'application' in adaptation.lower():
            framing = "\n\n**Why this matters:** This concept is useful for solving real-world problems "
            framing += "like data analysis, automation, and building applications."
            content = framing + "\n\n" + content
        
        step['content'] = content
        return step
    
    @staticmethod
    def _apply_explanation_style(step: Dict[str, Any], style: str) -> Dict[str, Any]:
        """Apply explanation style to content."""
        content = step.get('content', '')
        
        style_markers = {
            'analogies': '\n\n🔗 **Think of it like this:** ',
            'step-by-step': '\n\n📝 **Step-by-step:** ',
            'examples': '\n\n🎯 **For example:** ',
            'none': ''
        }
        
        marker = style_markers.get(style, '')
        if marker and marker not in content:
            # Insert style marker before the task
            task_marker = '**Your Task:**'
            if task_marker in content:
                parts = content.split(task_marker)
                content = parts[0] + marker + task_marker + task_marker.join(parts[1:])
            else:
                content += marker
        
        step['content'] = content
        return step