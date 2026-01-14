"""
Learner preference collection.
"""
import streamlit as st
from typing import Optional

class PreferenceCollector:
    """Collects learner preferences."""
    
    def render(self) -> Optional[str]:
        """Render preference selection UI."""
        st.markdown("### Explanation Style")
        st.markdown("*Optional: How would you like concepts explained?*")
        
        if 'explanation_style' not in st.session_state:
            st.session_state.explanation_style = "none"
        
        selected_style = st.radio(
            "Choose your preferred style:",
            options=["none", "analogies", "step-by-step", "examples"],
            format_func=lambda x: {
                "none": "Standard explanations",
                "analogies": "Use analogies and comparisons",
                "step-by-step": "Break down into clear steps",
                "examples": "Focus on practical examples"
            }[x],
            index=["none", "analogies", "step-by-step", "examples"].index(
                st.session_state.explanation_style
            ),
            label_visibility="collapsed"
        )
        
        st.session_state.explanation_style = selected_style
        
        return selected_style if selected_style != "none" else None