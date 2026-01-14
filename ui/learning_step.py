"""
Learning step rendering.
"""
import streamlit as st
from typing import Optional
from content.generator import LearningStep

class LearningStepRenderer:
    """Renders learning steps."""
    
    def render(self, learning_step: LearningStep) -> None:
        """Render a learning step."""
        # Header
        st.subheader(f"{learning_step.title}")
        
        # Content
        st.markdown("### 📚 Concept")
        st.markdown(learning_step.content)
        
        # Video if available
        if hasattr(learning_step, 'video_url') and learning_step.video_url:
            st.markdown("### 📺 Video Resource")
            try:
                # Use st.video for YouTube embed URLs
                st.video(learning_step.video_url)
                st.caption(f"🎬 Educational video related to {learning_step.title}")
            except Exception as e:
                st.warning(f"Video could not be loaded: {str(e)}")
                # Show link as fallback
                st.markdown(f"[Watch video on YouTube]({learning_step.video_url})")
        
        # Task
        st.markdown("### 🎯 Your Task")
        st.markdown(learning_step.task)
        
        # Difficulty indicator
        difficulty_colors = {
            'beginner': '🟢',
            'intermediate': '🟡', 
            'advanced': '🔴'
        }
        st.caption(f"{difficulty_colors.get(learning_step.difficulty, '⚪')} Level: {learning_step.difficulty}")
        
        # Show adaptation indicator if present
        if hasattr(learning_step, 'is_adapted') and learning_step.is_adapted:
            st.info("✨ **Learning support active**: The presentation has been adjusted to reduce friction.")
    
    def apply_adaptation(self, learning_step: LearningStep, 
                        adaptation: str, explanation_style: Optional[str]) -> LearningStep:
        """Apply adaptation to learning step."""
        # Create a new step with adaptation
        adapted_content = self._apply_style(learning_step.content, adaptation, explanation_style)
        
        # Create adapted step
        adapted_step = LearningStep(
            id=learning_step.id,
            title=learning_step.title,
            content=adapted_content,
            task=learning_step.task,
            correct_answer=learning_step.correct_answer,
            hints=learning_step.hints,
            difficulty=learning_step.difficulty,
            options=getattr(learning_step, 'options', None),
            video_url=getattr(learning_step, 'video_url', None)
        )
        
        # Mark as adapted
        adapted_step.is_adapted = True
        adapted_step.adaptation_type = adaptation
        
        return adapted_step
    
    def _apply_style(self, content: str, adaptation: str, style: Optional[str]) -> str:
        """Apply explanation style to content."""
        adapted_content = content
        
        # Apply explanation style
        if style and style != "none":
            style_additions = {
                "analogies": "\n\n🔗 **Think of it like this**: This concept is similar to learning a new language - you start with basic vocabulary before forming complex sentences.",
                "step-by-step": "\n\n📝 **Step-by-step breakdown**:\n1. Start with the basic concept\n2. Understand each component\n3. See how they work together\n4. Apply the knowledge",
                "examples": "\n\n🎯 **Practical example**: For instance, in real life, this works like... (insert relevant example based on content)"
            }
            
            addition = style_additions.get(style, "")
            adapted_content += addition
        
        # Add adaptation note
        if adaptation:
            adapted_content += f"\n\n✨ **Learning Support**: {adaptation}"
        
        return adapted_content