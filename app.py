"""
Main Streamlit application for the friction-aware learning platform.
"""
import streamlit as st
import time
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

# Import system modules
from signals.collector import SignalCollector
from signals.schemas import SessionState
from content.generator import ContentGenerator, LearningStep
from ui.learning_step import LearningStepRenderer
from ui.preferences import PreferenceCollector
from util.device import DeviceDetector

class FrictionAwareLearningPlatform:
    """Main orchestrator for the friction-aware learning platform."""
    
    def __init__(self):
        """Initialize the platform with all necessary components."""
        # Page configuration
        st.set_page_config(
            page_title="Friction-Aware Learning Platform",
            page_icon="📚",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Initialize session state
        self._init_session_state()
        
        # Initialize system components
        self.signal_collector = SignalCollector()
        self.content_generator = ContentGenerator()
        self.step_renderer = LearningStepRenderer()
        self.preference_collector = PreferenceCollector()
        self.device_detector = DeviceDetector()
        
        # Track current learning step in session state
        if 'current_step_id' not in st.session_state:
            st.session_state.current_step_id = 0
    
    def _init_session_state(self) -> None:
        """Initialize all session state variables."""
        if 'session_start_time' not in st.session_state:
            st.session_state.session_start_time = datetime.now()
        
        if 'session_state' not in st.session_state:
            st.session_state.session_state = SessionState()
        
        if 'signal_history' not in st.session_state:
            st.session_state.signal_history = []
        
        if 'adaptation_history' not in st.session_state:
            st.session_state.adaptation_history = []
        
        if 'current_adaptation' not in st.session_state:
            st.session_state.current_adaptation = None
        
        if 'learning_topic' not in st.session_state:
            st.session_state.learning_topic = None
        
        if 'learning_steps' not in st.session_state:
            st.session_state.learning_steps = []
        
        if 'step_completion_times' not in st.session_state:
            st.session_state.step_completion_times = {}
        
        if 'error_counts' not in st.session_state:
            st.session_state.error_counts = {}
        
        if 'content_generated' not in st.session_state:
            st.session_state.content_generated = False
        
        if 'current_step_id' not in st.session_state:
            st.session_state.current_step_id = 0
        
        if 'hint_counters' not in st.session_state:
            st.session_state.hint_counters = {}
        
        if 'last_answer_checked' not in st.session_state:
            st.session_state.last_answer_checked = None
        
        if 'last_checked_step' not in st.session_state:
            st.session_state.last_checked_step = None
        
        if 'friction_scores' not in st.session_state:
            st.session_state.friction_scores = {
                "Access friction": 0.0,
                "Cognitive load friction": 0.0,
                "Regulation & motivation friction": 0.0,
                "Interaction & feedback friction": 0.0,
                "Transfer & meaning friction": 0.0
            }
    
    def run(self) -> None:
        """Run the main application loop."""
        # Header
        st.title("📚 Friction-Aware Learning Platform")
        st.markdown("""
        An adaptive learning system that observes interaction patterns and adjusts the 
        learning environment to reduce friction. The system diagnoses **conditions**, not learners.
        """)
        
        # Sidebar for preferences and system info
        with st.sidebar:
            st.header("Learning Preferences")
            explanation_style = self.preference_collector.render()
            
            st.header("System Status")
            self._render_system_status()
            
            if st.button("Reset Session", type="secondary"):
                self._reset_session()
        
        # Main content area
        if not st.session_state.learning_topic:
            self._render_topic_selection()
        elif not st.session_state.content_generated:
            self._generate_content()
        else:
            tab1, tab2 = st.tabs(["Learning Experience", "System Insights"])
            
            with tab1:
                self._render_learning_experience(explanation_style)
            
            with tab2:
                self._render_system_insights()
    
    def _render_topic_selection(self) -> None:
        """Render topic selection interface."""
        st.header("🎯 What would you like to learn?")
        
        # Popular topics
        popular_topics = [
            "Python Programming",
            "Machine Learning",
            "Web Development",
            "Data Science",
            "JavaScript",
            "Artificial Intelligence",
            "Blockchain Technology",
            "Cybersecurity",
            "Cloud Computing",
            "Mobile App Development"
        ]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Custom topic input
            custom_topic = st.text_input(
                "Enter any topic you'd like to learn:",
                placeholder="e.g., Quantum Physics, Spanish Grammar, Digital Marketing..."
            )
            
            # Topic suggestions
            st.markdown("### Or choose from popular topics:")
            
            # Display topics as buttons
            cols = st.columns(2)
            selected_topic = None
            
            for i, topic in enumerate(popular_topics):
                with cols[i % 2]:
                    if st.button(topic, key=f"topic_{i}", use_container_width=True):
                        selected_topic = topic
        
        with col2:
            st.markdown("### ℹ️ How it works")
            st.info("""
            1. Choose or enter a learning topic
            2. The system will generate personalized content
            3. Learn through interactive steps
            4. The system adapts to your interaction patterns
            5. No personal profiling or tracking
            """)
        
        # Determine final topic
        final_topic = None
        if custom_topic and custom_topic.strip():
            final_topic = custom_topic.strip()
        elif selected_topic:
            final_topic = selected_topic
        
        if final_topic:
            if st.button("Start Learning", type="primary", use_container_width=True):
                st.session_state.learning_topic = final_topic
                st.rerun()
    
    def _generate_content(self) -> None:
        """Generate learning content for the selected topic."""
        st.header(f"🎓 Generating content for: {st.session_state.learning_topic}")
        
        with st.spinner("Creating personalized learning path..."):
            # Generate learning steps
            learning_steps = self.content_generator.generate_learning_path(
                st.session_state.learning_topic
            )
            
            if learning_steps and len(learning_steps) > 0:
                st.session_state.learning_steps = learning_steps
                st.session_state.content_generated = True
                st.success("✅ Learning content generated successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Could not generate content. Please try a different topic.")
                if st.button("Try Again"):
                    st.session_state.learning_topic = None
                    st.rerun()
    
    def _render_learning_experience(self, explanation_style: Optional[str]) -> None:
        """Render the current learning step with any active adaptations."""
        learning_steps = st.session_state.learning_steps
        current_step_id = st.session_state.current_step_id
        
        if current_step_id >= len(learning_steps):
            self._render_completion_screen()
            return
        
        current_step = learning_steps[current_step_id]
        
        # Collect signals before rendering
        self.signal_collector.collect_pre_step_signals(
            step_id=current_step_id,
            step_difficulty=current_step.difficulty
        )
        
        # Apply current adaptation if it exists
        adapted_step = current_step
        if st.session_state.current_adaptation:
            adapted_step = self.step_renderer.apply_adaptation(
                current_step, 
                st.session_state.current_adaptation,
                explanation_style
            )
        
        # Display progress
        progress = (current_step_id + 1) / len(learning_steps)
        st.progress(progress)
        st.caption(f"Step {current_step_id + 1} of {len(learning_steps)}")
        
        # Render step content
        self.step_renderer.render(adapted_step)
        
        # Create form for answer submission
        with st.form(key=f"step_form_{current_step_id}"):
            # Start timer for this interaction
            interaction_start = time.time()
            
            # User response (multiple choice or text input)
            if hasattr(current_step, 'options') and current_step.options:
                # Multiple choice question
                user_answer = st.radio(
                    "Select your answer:",
                    options=current_step.options,
                    key=f"answer_radio_{current_step_id}",
                    index=None  # No default selection
                )
                answer_key = f"answer_radio_{current_step_id}"
            else:
                # Text input question
                user_answer = st.text_input(
                    "Your answer:",
                    key=f"answer_text_{current_step_id}",
                    placeholder="Enter your answer here..."
                )
                answer_key = f"answer_text_{current_step_id}"
            
            # Submit button
            submitted = st.form_submit_button(
                "Submit Answer",
                type="primary",
                use_container_width=True
            )
            
            if submitted:
                # Get the actual answer from session state
                user_answer = st.session_state.get(answer_key, "")
                
                if user_answer:  # Only process if answer is provided
                    # Calculate time spent
                    interaction_time = time.time() - interaction_start
                    
                    # Check hint usage
                    hint_key = f"hint_used_{current_step_id}"
                    hint_used = st.session_state.get(hint_key, False)
                    
                    # Collect post-submission signals
                    signals = self.signal_collector.collect_post_step_signals(
                        step_id=current_step_id,
                        user_answer=user_answer,
                        correct_answer=current_step.correct_answer,
                        interaction_time=interaction_time,
                        hint_used=hint_used,
                        step_difficulty=current_step.difficulty
                    )
                    
                    # Store signals in history
                    st.session_state.signal_history.append(signals)
                    
                    # Update friction scores
                    self._update_friction_scores()
                    
                    # Check answer using flexible matching
                    is_correct = self._check_answer_flexible(user_answer, current_step.correct_answer)
                    
                    if is_correct:
                        # Record completion time
                        st.session_state.step_completion_times[current_step_id] = interaction_time
                        
                        # Clear hint flags for this step
                        hint_key = f"hint_used_{current_step_id}"
                        if hint_key in st.session_state:
                            del st.session_state[hint_key]
                        
                        hint_counter_key = f"hint_counter_{current_step_id}"
                        if hint_counter_key in st.session_state.hint_counters:
                            del st.session_state.hint_counters[hint_counter_key]
                        
                        # Show success message
                        st.success("✅ Correct! Well done.")
                        
                        # Clear any adaptation if performance is good
                        self._evaluate_and_clear_adaptation()
                        
                        # Mark for step progression
                        st.session_state.last_answer_checked = "correct"
                        st.session_state.last_checked_step = current_step_id
                        
                    else:
                        # Increment error count
                        error_key = f"step_{current_step_id}"
                        st.session_state.error_counts[error_key] = \
                            st.session_state.error_counts.get(error_key, 0) + 1
                        
                        # Show error message with correct answer
                        st.error(f"❌ Not quite right. The correct answer is: **{current_step.correct_answer}**")
                        
                        # Mark for error handling
                        st.session_state.last_answer_checked = "incorrect"
                        st.session_state.last_checked_step = current_step_id
                        
                        # Trigger friction diagnosis if needed
                        if len(st.session_state.signal_history) >= 2:
                            self._diagnose_and_adapt()
                else:
                    st.warning("⚠️ Please provide an answer before submitting.")
        
        # Handle step progression after correct answer
        if (st.session_state.get('last_answer_checked') == "correct" and 
            st.session_state.get('last_checked_step') == current_step_id):
            # Wait and move to next step
            time.sleep(2)
            st.session_state.current_step_id += 1
            st.session_state.last_answer_checked = None
            st.session_state.last_checked_step = None
            st.rerun()
        
        # Hint button (OUTSIDE the form)
        if hasattr(adapted_step, 'hints') and adapted_step.hints:
            st.divider()
            col1, col2 = st.columns([3, 1])
            with col2:
                hint_key = f"hint_btn_{current_step_id}"
                if st.button("💡 Need a hint?", key=hint_key, 
                            type="secondary", use_container_width=True):
                    # Get current hint index
                    hint_counter_key = f"hint_counter_{current_step_id}"
                    if hint_counter_key not in st.session_state.hint_counters:
                        st.session_state.hint_counters[hint_counter_key] = 0
                    
                    current_hint_index = st.session_state.hint_counters[hint_counter_key]
                    
                    # Show hint if available
                    if current_hint_index < len(adapted_step.hints):
                        st.session_state[f"hint_shown_{current_step_id}_{current_hint_index}"] = True
                        # Record hint usage
                        st.session_state[f"hint_used_{current_step_id}"] = True
                        # Increment hint counter
                        st.session_state.hint_counters[hint_counter_key] = current_hint_index + 1
                        st.rerun()
            
            # Display hints that have been shown
            hint_counter_key = f"hint_counter_{current_step_id}"
            hint_count = st.session_state.hint_counters.get(hint_counter_key, 0)
            
            if hint_count > 0:
                st.markdown("### 💡 Hints Shown")
                for i in range(hint_count):
                    if i < len(adapted_step.hints):
                        st.info(f"**Hint {i+1}**: {adapted_step.hints[i]}")
                
                if hint_count >= len(adapted_step.hints):
                    st.warning("✨ That's all the hints available. You can do this!")
    
    def _check_answer_flexible(self, user_answer: str, correct_answer: str) -> bool:
        """Flexible answer checking for dynamic content."""
        if not user_answer or not correct_answer:
            return False
        
        # Clean both answers
        user_clean = str(user_answer).strip().lower()
        correct_clean = str(correct_answer).strip().lower()
        
        # Exact match
        if user_clean == correct_clean:
            return True
        
        # For multiple choice questions, compare cleaned text
        # Remove any leading/trailing punctuation
        import string
        user_clean = user_clean.translate(str.maketrans('', '', string.punctuation))
        correct_clean = correct_clean.translate(str.maketrans('', '', string.punctuation))
        
        if user_clean == correct_clean:
            return True
        
        # Check for keyword overlap (for text answers)
        user_words = set(user_clean.split())
        correct_words = set(correct_clean.split())
        
        if user_words and correct_words:
            common_words = user_words.intersection(correct_words)
            if len(common_words) >= 2:  # At least 2 common words
                return True
        
        # Check if correct answer contains user answer or vice versa
        if correct_clean in user_clean or user_clean in correct_clean:
            return True
        
        return False
    
    def _update_friction_scores(self) -> None:
        """Update friction scores based on recent signals."""
        if len(st.session_state.signal_history) < 2:
            return
        
        # Get recent signals for analysis
        recent_signals = st.session_state.signal_history[-5:] if len(st.session_state.signal_history) >= 5 else st.session_state.signal_history
        
        # Reset scores
        scores = {
            "Access friction": 0.0,
            "Cognitive load friction": 0.0,
            "Regulation & motivation friction": 0.0,
            "Interaction & feedback friction": 0.0,
            "Transfer & meaning friction": 0.0
        }
        
        # 1. Access Friction (device/network issues)
        access_indicators = 0
        for signal in recent_signals:
            if signal.get('network_latency', 0) > 0.3:  # High latency
                access_indicators += 1
            device_type = signal.get('device_type', 'desktop')
            if device_type in ['mobile', 'tablet']:
                access_indicators += 0.5
        
        scores["Access friction"] = min(1.0, access_indicators / 3)
        
        # 2. Cognitive Load Friction
        cognitive_indicators = 0
        
        # Response time analysis
        response_times = [s.get('interaction_time', 0) for s in recent_signals]
        if len(response_times) >= 2:
            # Check increasing trend
            increasing = True
            for i in range(len(response_times)-1):
                if response_times[i] >= response_times[i+1]:
                    increasing = False
                    break
            if increasing:
                cognitive_indicators += 1.5
            
            # Check for high average time
            avg_time = sum(response_times) / len(response_times)
            if avg_time > 45:
                cognitive_indicators += 1
        
        # Error patterns
        error_count = sum(1 for s in recent_signals if not s.get('correct', True))
        cognitive_indicators += error_count * 0.3
        
        # Hint usage
        hint_count = sum(1 for s in recent_signals if s.get('hint_used', False))
        cognitive_indicators += hint_count * 0.4
        
        scores["Cognitive load friction"] = min(1.0, cognitive_indicators / 3)
        
        # 3. Regulation & Motivation Friction
        motivation_indicators = 0
        
        # Check for abandonment patterns
        abandonment_count = sum(1 for s in recent_signals 
                              if s.get('interaction_time', 0) < 10 and not s.get('correct', True))
        motivation_indicators += abandonment_count
        
        # Check for very long times (potential disengagement)
        if response_times:
            if max(response_times) > 90:  # Very long time on a step
                motivation_indicators += 1
        
        scores["Regulation & motivation friction"] = min(1.0, motivation_indicators / 2)
        
        # 4. Interaction & Feedback Friction
        interaction_indicators = 0
        
        # Check for repeated errors on same step
        step_error_counts = {}
        for signal in recent_signals:
            step_id = signal.get('step_id', 0)
            if not signal.get('correct', True):
                step_error_counts[step_id] = step_error_counts.get(step_id, 0) + 1
        
        for count in step_error_counts.values():
            if count >= 2:
                interaction_indicators += 1
        
        scores["Interaction & feedback friction"] = min(1.0, interaction_indicators / 2)
        
        # 5. Transfer & Meaning Friction
        transfer_indicators = 0
        
        if len(st.session_state.signal_history) >= 4:
            # Check performance across different difficulty levels
            beginner_signals = [s for s in st.session_state.signal_history 
                              if s.get('step_difficulty') == 'beginner']
            intermediate_signals = [s for s in st.session_state.signal_history 
                                  if s.get('step_difficulty') == 'intermediate']
            
            if beginner_signals and intermediate_signals:
                beginner_correct = sum(1 for s in beginner_signals if s.get('correct', True))
                intermediate_correct = sum(1 for s in intermediate_signals if s.get('correct', True))
                
                beginner_acc = beginner_correct / len(beginner_signals)
                intermediate_acc = intermediate_correct / len(intermediate_signals)
                
                # If performance drops significantly with increased difficulty
                if beginner_acc > 0.7 and intermediate_acc < 0.4:
                    transfer_indicators += 1
        
        scores["Transfer & meaning friction"] = min(1.0, transfer_indicators)
        
        # Update session state
        st.session_state.friction_scores = scores
    
    def _evaluate_and_clear_adaptation(self) -> None:
        """Clear adaptation if learner performance has improved."""
        if (st.session_state.current_adaptation and 
            len(st.session_state.signal_history) >= 3):
            
            # Check recent performance
            recent_signals = st.session_state.signal_history[-3:]
            error_counts = sum(1 for s in recent_signals if not s.get('correct', True))
            
            if error_counts == 0:  # No errors in recent attempts
                st.session_state.adaptation_history.append({
                    'action': 'cleared',
                    'adaptation': st.session_state.current_adaptation,
                    'reason': 'Improved performance'
                })
                st.session_state.current_adaptation = None
                # Show toast notification
                st.toast("✅ Learning environment returning to standard mode", icon="🔄")
    
    def _diagnose_and_adapt(self) -> None:
        """Diagnose friction and apply adaptation if needed."""
        if len(st.session_state.signal_history) < 2:
            return
        
        # Get friction scores
        scores = st.session_state.friction_scores
        
        # Find the highest friction
        max_friction = max(scores.items(), key=lambda x: x[1])
        friction_type, friction_score = max_friction
        
        # Only adapt if friction score is significant
        if friction_score > 0.4:
            adaptation = self._get_adaptation_for_friction(friction_type)
            
            if adaptation:
                st.session_state.current_adaptation = adaptation
                
                # Record in history
                st.session_state.adaptation_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'friction_type': friction_type,
                    'friction_score': friction_score,
                    'adaptation': adaptation,
                    'reason': f'High {friction_type} detected ({friction_score:.0%})'
                })
                
                # Show subtle notification
                st.toast(f"✨ Adjusting for {friction_type}...", icon="🔄")
    
    def _get_adaptation_for_friction(self, friction_type: str) -> Optional[str]:
        """Get appropriate adaptation for friction type."""
        adaptations = {
            "Access friction": [
                "Simplifying layout for better accessibility",
                "Increasing text size and button targets",
                "Optimizing content for different devices"
            ],
            "Cognitive load friction": [
                "Breaking complex concepts into smaller parts",
                "Adding more examples and step-by-step explanations",
                "Providing visual aids and diagrams"
            ],
            "Regulation & motivation friction": [
                "Adding progress indicators and milestones",
                "Providing encouraging feedback and reinforcement",
                "Breaking sessions into shorter, focused segments"
            ],
            "Interaction & feedback friction": [
                "Simplifying interface and reducing cognitive load",
                "Providing clearer instructions and expectations",
                "Adding immediate, actionable feedback"
            ],
            "Transfer & meaning friction": [
                "Adding real-world examples and applications",
                "Connecting concepts to practical situations",
                "Providing context and relevance explanations"
            ]
        }
        
        adaptation_list = adaptations.get(friction_type, [])
        if adaptation_list:
            # Use the first adaptation for now
            return adaptation_list[0]
        return None
    
    def _render_system_status(self) -> None:
        """Render system status in sidebar."""
        session_duration = datetime.now() - st.session_state.session_start_time
        minutes = int(session_duration.total_seconds() / 60)
        
        st.metric("Session Duration", f"{minutes} min")
        st.metric("Steps Completed", st.session_state.current_step_id)
        
        if st.session_state.learning_topic:
            st.info(f"**Learning**: {st.session_state.learning_topic}")
        
        if st.session_state.current_adaptation:
            st.success(f"**Active Support**: {st.session_state.current_adaptation}")
        else:
            st.success("**Status**: Learning environment is standard")
        
        # Show highest friction if detected
        scores = st.session_state.friction_scores
        if any(score > 0.4 for score in scores.values()):
            max_friction = max(scores.items(), key=lambda x: x[1])
            if max_friction[1] > 0.4:
                st.warning(f"**Detected**: {max_friction[0]} ({max_friction[1]:.0%})")
        
        # Device info
        device_info = self.device_detector.get_device_info()
        st.caption(f"📱 {device_info['device_type']}")
    
    def _render_system_insights(self) -> None:
        """Render system insights tab with friction metrics."""
        st.header("📊 System Insights & Friction Detection")
        st.markdown("""
        > **Ethical Boundary**: This system observes **interaction patterns**, not learners.
        All adaptations are temporary and environment-focused. No personal profiling occurs.
        """)
        
        # Friction Detection Metrics
        if st.session_state.signal_history:
            st.subheader("🎯 Friction Detection Dashboard")
            
            scores = st.session_state.friction_scores
            
            # Create 2x3 grid for friction scores
            cols = st.columns(3)
            friction_items = list(scores.items())
            
            for idx, (friction_type, score) in enumerate(friction_items):
                col_idx = idx % 3
                with cols[col_idx]:
                    # Create a metric card for each friction type
                    if score > 0.7:
                        color = "🔴"
                        level = "High"
                    elif score > 0.4:
                        color = "🟡"
                        level = "Medium"
                    else:
                        color = "🟢"
                        level = "Low"
                    
                    st.metric(
                        label=f"{color} {friction_type}",
                        value=f"{score:.0%}",
                        delta=level,
                        delta_color="off"
                    )
                    
                    # Add progress bar below
                    st.progress(score)
            
            # Interpretation guide
            with st.expander("📖 How to interpret these metrics"):
                st.markdown("""
                **Friction Types Explained:**
                
                - **Access Friction** (🔴🟡🟢): Issues with device compatibility, network latency, or interface accessibility
                - **Cognitive Load Friction**: When information processing demands exceed working memory capacity
                - **Regulation & Motivation Friction**: Patterns suggesting engagement, persistence, or emotional challenges
                - **Interaction & Feedback Friction**: Issues with UI/UX clarity, instructions, or feedback timing
                - **Transfer & Meaning Friction**: Difficulties applying knowledge across contexts or finding relevance
                
                **Scoring Guide:**
                - 🔴 **High (70%+)**: Strong pattern detected, system may adapt
                - 🟡 **Medium (40-70%)**: Emerging pattern, being monitored
                - 🟢 **Low (<40%)**: Minimal friction detected
                """)
            
            # Signal patterns summary
            st.subheader("📈 Learning Performance Metrics")
            
            cols = st.columns(4)
            with cols[0]:
                total_steps = len(st.session_state.signal_history)
                correct_steps = sum(1 for s in st.session_state.signal_history if s.get('correct', True))
                accuracy = (correct_steps / total_steps * 100) if total_steps > 0 else 0
                st.metric("Accuracy", f"{accuracy:.1f}%")
            
            with cols[1]:
                if st.session_state.signal_history:
                    avg_time = sum(s.get('interaction_time', 0) for s in st.session_state.signal_history) / len(st.session_state.signal_history)
                    st.metric("Avg. Time/Step", f"{avg_time:.1f}s")
                else:
                    st.metric("Avg. Time/Step", "0s")
            
            with cols[2]:
                hint_usage = sum(1 for s in st.session_state.signal_history if s.get('hint_used', False))
                st.metric("Hints Used", hint_usage)
            
            with cols[3]:
                error_count = sum(1 for s in st.session_state.signal_history if not s.get('correct', True))
                st.metric("Total Errors", error_count)
            
            # Response time trend
            if len(st.session_state.signal_history) >= 2:
                st.subheader("⏱️ Response Time Trend (Last 5 Steps)")
                times = [s.get('interaction_time', 0) for s in st.session_state.signal_history[-5:]]
                if times:
                    # Create a simple text-based trend indicator
                    if len(times) >= 2:
                        first_half = sum(times[:len(times)//2]) / (len(times)//2)
                        second_half = sum(times[len(times)//2:]) / (len(times) - len(times)//2)
                        
                        if second_half > first_half * 1.3:
                            trend = "📈 Increasing"
                            color = "orange"
                        elif second_half < first_half * 0.7:
                            trend = "📉 Decreasing"
                            color = "green"
                        else:
                            trend = "📊 Stable"
                            color = "blue"
                        
                        st.write(f"**Trend**: <span style='color:{color}'>{trend}</span>", unsafe_allow_html=True)
                    
                    # Show individual times
                    st.write("**Recent times**: " + ", ".join([f"{t:.1f}s" for t in times]))
            
            # Adaptation history
            if st.session_state.adaptation_history:
                st.subheader("🔄 Recent Environment Adaptations")
                for i, adaptation in enumerate(st.session_state.adaptation_history[-3:]):
                    with st.expander(f"Adaptation {i+1}: {adaptation.get('adaptation', 'Unknown')[:50]}..."):
                        st.write(f"**Friction Type**: {adaptation.get('friction_type', 'Unknown')}")
                        st.write(f"**Friction Score**: {adaptation.get('friction_score', 0):.0%}")
                        st.write(f"**Applied**: {adaptation.get('timestamp', 'Unknown')}")
                        st.write(f"**Reason**: {adaptation.get('reason', 'Pattern detected')}")
        
        # System principles
        st.divider()
        st.subheader("⚖️ System Principles")
        
        principles = [
            "🔍 **Diagnoses Conditions, Not Learners**: Observes interaction patterns, not ability",
            "🔄 **Adapts Environment, Not Learner**: Changes presentation, not content difficulty",
            "⏱️ **Temporary Interventions**: All adaptations fade as performance improves",
            "🎯 **Preserves Learning Goals**: Maintains original learning objectives",
            "🚫 **No Profiling**: Creates no permanent learner profiles or labels",
            "📊 **Transparent Metrics**: Shows friction patterns for system transparency"
        ]
        
        for principle in principles:
            st.write(principle)
    
    def _render_completion_screen(self) -> None:
        """Render completion screen when all steps are done."""
        st.balloons()
        st.success("## 🎉 Learning Session Complete!")
        
        # Session summary
        total_time = sum(st.session_state.step_completion_times.values())
        total_steps = len(st.session_state.learning_steps)
        correct_steps = len([s for s in st.session_state.signal_history if s.get('correct', True)])
        accuracy = (correct_steps / total_steps * 100) if total_steps > 0 else 0
        
        # Friction summary
        scores = st.session_state.friction_scores
        high_frictions = [ft for ft, score in scores.items() if score > 0.5]
        
        st.markdown(f"""
        ### 📊 Session Summary
        - **Topic**: {st.session_state.learning_topic}
        - **Steps Completed**: {total_steps}
        - **Total Learning Time**: {total_time:.0f} seconds
        - **Accuracy**: {accuracy:.1f}%
        - **Environment Adaptations**: {len(st.session_state.adaptation_history)}
        - **Friction Patterns Detected**: {len(high_frictions)}
        
        ### 🎯 What You've Learned
        You've completed a full learning session where the system:
        1. **Generated topic-relevant content** for {st.session_state.learning_topic}
        2. **Observed 5 friction patterns** in your interaction
        3. **Made temporary adjustments** to reduce detected friction
        4. **Faded support** as your performance improved
        
        ### 📈 Friction Insights
        The system monitored these learning conditions:
        """)
        
        # Show friction insights
        for friction_type, score in scores.items():
            if score > 0.3:
                st.write(f"- **{friction_type}**: {score:.0%} detected")
        
        st.markdown("""
        ### 🔄 Ready for Another Session?
        Click **Reset Session** in the sidebar to learn something new!
        """)
    
    def _reset_session(self) -> None:
        """Reset the entire learning session."""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def main():
    """Entry point for the Streamlit application."""
    platform = FrictionAwareLearningPlatform()
    platform.run()

if __name__ == "__main__":
    main()