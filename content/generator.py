"""
Dynamic content generation using free APIs for any topic.
"""
import requests
import json
import random
import re
import time
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class LearningStep:
    """Represents a learning step with content."""
    id: int
    title: str
    content: str
    task: str
    correct_answer: str
    hints: List[str]
    difficulty: str
    options: Optional[List[str]] = None
    video_url: Optional[str] = None

class ContentGenerator:
    """Generates learning content dynamically using free APIs."""
    
    def __init__(self):
        """Initialize APIs with proper user agents."""
        # Wikipedia API endpoint (no library needed)
        self.wikipedia_api = "https://en.wikipedia.org/w/api.php"
        
        # Free educational APIs
        self.quotable_api = "https://api.quotable.io/random"
        self.free_dictionary = "https://api.dictionaryapi.dev/api/v2/entries/en"
        self.bored_api = "https://www.boredapi.com/api/activity"  # For random content
        
        # Cache for API results
        self.cache = {}
        
        # User agent for API requests
        self.headers = {
            'User-Agent': 'FrictionAwareLearningPlatform/1.0 (https://github.com/yourusername/friction-learning)',
            'Accept': 'application/json'
        }
    
    def generate_learning_path(self, topic: str) -> List[LearningStep]:
        """
        Generate a learning path for any topic using APIs.
        """
        learning_steps = []
        
        # Clear cache for new topic
        self.cache = {}
        
        # Get content about topic
        topic_content = self._get_topic_content(topic)
        
        # Search for educational videos using YouTube iframe search
        videos = self._search_videos(topic)
        
        # Generate 5 learning steps
        for step_id in range(5):
            try:
                step = self._create_dynamic_step(topic, topic_content, videos, step_id)
                if step:
                    learning_steps.append(step)
            except Exception as e:
                # Fallback step if API fails
                step = self._create_fallback_step(topic, step_id)
                learning_steps.append(step)
                print(f"Error creating step {step_id}: {e}")
        
        return learning_steps
    
    def _get_topic_content(self, topic: str) -> str:
        """Get content about topic from Wikipedia API."""
        cache_key = f"content_{topic}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # Try Wikipedia API
            params = {
                'action': 'query',
                'format': 'json',
                'titles': topic,
                'prop': 'extracts',
                'exintro': True,
                'explaintext': True,
            }
            
            response = requests.get(
                self.wikipedia_api, 
                params=params, 
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                pages = data.get('query', {}).get('pages', {})
                
                for page_id, page_data in pages.items():
                    if page_id != '-1':  # Page exists
                        extract = page_data.get('extract', '')
                        if extract:
                            # Limit length
                            content = extract[:600] + "..." if len(extract) > 600 else extract
                            self.cache[cache_key] = content
                            return content
            
            # If Wikipedia fails, try alternative sources
            return self._get_alternative_content(topic)
            
        except Exception as e:
            print(f"Wikipedia API error: {e}")
            return self._get_alternative_content(topic)
    
    def _get_alternative_content(self, topic: str) -> str:
        """Get content from alternative sources."""
        try:
            # Try a simple web search simulation
            topics = {
                "python": "Python is a high-level programming language known for its simplicity and readability. It's widely used in web development, data science, artificial intelligence, and automation.",
                "machine learning": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without explicit programming. It focuses on developing algorithms that can identify patterns and make predictions.",
                "web development": "Web development involves creating websites and web applications. It includes front-end development (user interface), back-end development (server-side logic), and full-stack development (both).",
                "data science": "Data science combines statistics, programming, and domain knowledge to extract insights from data. It involves data collection, cleaning, analysis, visualization, and machine learning.",
                "javascript": "JavaScript is a programming language used to create interactive web pages. It runs in web browsers and can also be used on servers through Node.js.",
                "artificial intelligence": "Artificial intelligence involves creating intelligent machines that can perform tasks typically requiring human intelligence, such as visual perception, speech recognition, and decision-making.",
                "blockchain": "Blockchain is a distributed ledger technology that records transactions securely and transparently. It's the foundation for cryptocurrencies like Bitcoin and enables decentralized applications.",
                "cybersecurity": "Cybersecurity involves protecting computer systems, networks, and data from digital attacks. It includes techniques for prevention, detection, and response to security threats.",
                "cloud computing": "Cloud computing delivers computing services over the internet, including storage, processing power, and software. It enables scalable and cost-effective IT solutions.",
                "mobile development": "Mobile development involves creating applications for mobile devices. It includes native development (iOS/Android) and cross-platform development using frameworks like React Native or Flutter."
            }
            
            # Find the closest matching topic
            topic_lower = topic.lower()
            for key, content in topics.items():
                if key in topic_lower:
                    return content
            
            # Generic content for any topic
            return f"{topic} is a fascinating field that combines theoretical knowledge with practical application. Learning about it helps develop critical thinking, problem-solving skills, and technical expertise that can be applied in various professional and personal contexts."
            
        except:
            return f"Learning about {topic} involves understanding fundamental concepts, practical applications, and current developments in the field."
    
    def _search_videos(self, topic: str) -> List[Dict[str, str]]:
        """Search for educational videos using YouTube iframe approach."""
        # YouTube doesn't allow direct API access without key, but we can use iframe URLs
        # These are generic educational videos that cover many topics
        
        educational_channels = {
            "python": [
                {"title": "Python Full Course for Beginners", "url": "https://www.youtube.com/embed/rfscVS0vtbw"},
                {"title": "Python Tutorial - Python for Beginners", "url": "https://www.youtube.com/embed/_uQrJ0TkZlc"},
                {"title": "Learn Python - Full Course", "url": "https://www.youtube.com/embed/8DvywoWv6fI"}
            ],
            "machine learning": [
                {"title": "Machine Learning Course for Beginners", "url": "https://www.youtube.com/embed/GwIo3gDZCVQ"},
                {"title": "Machine Learning Tutorial", "url": "https://www.youtube.com/embed/KNAWp2S3w94"},
                {"title": "Neural Networks Explained", "url": "https://www.youtube.com/embed/aircAruvnKk"}
            ],
            "web development": [
                {"title": "Web Development Full Course", "url": "https://www.youtube.com/embed/3JluqTojuME"},
                {"title": "HTML & CSS Tutorial", "url": "https://www.youtube.com/embed/qz0aGYrrlhU"},
                {"title": "JavaScript Tutorial", "url": "https://www.youtube.com/embed/PkZNo7MFNFg"}
            ],
            "data science": [
                {"title": "Data Science Full Course", "url": "https://www.youtube.com/embed/ua-CiDNNj30"},
                {"title": "Data Science for Beginners", "url": "https://www.youtube.com/embed/X3paOmcrTjQ"},
                {"title": "Python for Data Science", "url": "https://www.youtube.com/embed/LHBE6Q9XlzI"}
            ],
            "general": [
                {"title": "How to Learn Anything", "url": "https://www.youtube.com/embed/IlU-zDU6aQ0"},
                {"title": "Study Techniques That Work", "url": "https://www.youtube.com/embed/5MgBikgcWnY"},
                {"title": "Critical Thinking Skills", "url": "https://www.youtube.com/embed/Vt4Dpb4SQxU"}
            ]
        }
        
        # Find the best matching channel
        topic_lower = topic.lower()
        for channel, videos in educational_channels.items():
            if channel in topic_lower:
                return videos
        
        # Return general learning videos
        return educational_channels["general"]
    
    def _create_dynamic_step(self, topic: str, topic_content: str, videos: List[Dict], step_id: int) -> LearningStep:
        """Create a dynamic learning step."""
        
        # Get video for this step
        video_index = step_id % len(videos) if videos else 0
        video_url = videos[video_index]['url'] if videos else None
        
        # Generate content based on step_id
        content = self._generate_step_content(topic, topic_content, step_id)
        
        # Generate question and answers
        question_data = self._generate_question(topic, step_id)
        
        # Generate hints
        hints = self._generate_hints(question_data['correct_answer'], question_data['options'])
        
        return LearningStep(
            id=step_id,
            title=self._generate_step_title(topic, step_id),
            content=content,
            task=question_data['question'],
            correct_answer=question_data['correct_answer'],
            hints=hints,
            difficulty=self._get_difficulty(step_id),
            options=question_data['options'],
            video_url=video_url
        )
    
    def _generate_step_content(self, topic: str, topic_content: str, step_id: int) -> str:
        """Generate step content dynamically."""
        
        # Different content focus for each step
        step_focus = [
            f"## Introduction to {topic}\n\n{topic_content}\n\nLet's begin our learning journey with the basics...",
            f"## Core Concepts of {topic}\n\nUnderstanding fundamental principles is essential for mastering {topic}. These concepts form the foundation for more advanced learning.",
            f"## Practical Applications of {topic}\n\nLearn how {topic} is applied in real-world scenarios. Practical application reinforces theoretical knowledge.",
            f"## Advanced Topics in {topic}\n\nExplore more complex aspects and current developments in {topic}. Building on your foundational knowledge.",
            f"## Mastery and Implementation of {topic}\n\nReview key concepts and learn strategies for applying {topic} knowledge effectively."
        ]
        
        focus = step_focus[step_id] if step_id < len(step_focus) else step_focus[0]
        
        # Add learning tips
        learning_tips = [
            "**Tip**: Start with basic concepts before advancing to complex topics.",
            "**Tip**: Regular practice is more effective than cramming.",
            "**Tip**: Apply concepts to real situations to deepen understanding.",
            "**Tip**: Review previous material regularly to reinforce learning.",
            "**Tip**: Connect new knowledge to what you already know."
        ]
        
        tip = learning_tips[step_id] if step_id < len(learning_tips) else learning_tips[0]
        
        return f"{focus}\n\n{tip}"
    
    def _generate_step_title(self, topic: str, step_id: int) -> str:
        """Generate step title."""
        titles = [
            f"Introduction to {topic}",
            f"Basic Concepts of {topic}",
            f"Core Principles of {topic}",
            f"Advanced Topics in {topic}",
            f"Practical Applications of {topic}"
        ]
        return titles[step_id] if step_id < len(titles) else f"Step {step_id + 1}: {topic}"
    
    def _generate_question(self, topic: str, step_id: int) -> Dict[str, Any]:
        """Generate dynamic question."""
        
        # Question types for different steps
        question_types = [
            self._generate_definition_question,
            self._generate_concept_question,
            self._generate_application_question,
            self._generate_analysis_question,
            self._generate_synthesis_question
        ]
        
        method_idx = step_id % len(question_types)
        return question_types[method_idx](topic, step_id)
    
    def _generate_definition_question(self, topic: str, step_id: int) -> Dict[str, Any]:
        """Generate definition question."""
        question = f"What best describes {topic}?"
        
        answers = [
            f"A field that combines theory and practice for solving problems",
            f"Only theoretical concepts with no practical use",
            f"A simple collection of facts to memorize",
            f"A narrow specialty with limited applications"
        ]
        
        correct = answers[0]
        random.shuffle(answers)
        
        return {
            'question': question,
            'correct_answer': correct,
            'options': answers
        }
    
    def _generate_concept_question(self, topic: str, step_id: int) -> Dict[str, Any]:
        """Generate concept question."""
        question = f"What is a key concept in understanding {topic}?"
        
        answers = [
            "Building from foundational principles to complex applications",
            "Memorizing all technical terms immediately",
            "Avoiding practical application until mastery",
            "Focusing only on advanced topics from the start"
        ]
        
        correct = answers[0]
        random.shuffle(answers)
        
        return {
            'question': question,
            'correct_answer': correct,
            'options': answers
        }
    
    def _generate_application_question(self, topic: str, step_id: int) -> Dict[str, Any]:
        """Generate application question."""
        question = f"How is {topic} typically applied in practice?"
        
        answers = [
            "By solving real-world problems through systematic approaches",
            "Only in academic research settings",
            "Through rigid procedures without adaptation",
            "Without considering practical constraints"
        ]
        
        correct = answers[0]
        random.shuffle(answers)
        
        return {
            'question': question,
            'correct_answer': correct,
            'options': answers
        }
    
    def _generate_analysis_question(self, topic: str, step_id: int) -> Dict[str, Any]:
        """Generate analysis question."""
        question = f"What analytical approach is important in {topic}?"
        
        answers = [
            "Breaking down complex problems into manageable parts",
            "Accepting information without critical examination",
            "Avoiding different perspectives on problems",
            "Using only one method for all situations"
        ]
        
        correct = answers[0]
        random.shuffle(answers)
        
        return {
            'question': question,
            'correct_answer': correct,
            'options': answers
        }
    
    def _generate_synthesis_question(self, topic: str, step_id: int) -> Dict[str, Any]:
        """Generate synthesis question."""
        question = f"How does {topic} integrate with other fields?"
        
        answers = [
            "By building connections between related concepts and applications",
            "By remaining completely isolated from other disciplines",
            "By dominating other fields without collaboration",
            "By avoiding interdisciplinary approaches"
        ]
        
        correct = answers[0]
        random.shuffle(answers)
        
        return {
            'question': question,
            'correct_answer': correct,
            'options': answers
        }
    
    def _generate_hints(self, correct_answer: str, options: List[str]) -> List[str]:
        """Generate helpful hints."""
        return [
            "Consider which answer is most comprehensive and practical",
            "Think about what would be most helpful for real understanding",
            "Eliminate options that seem unrealistic or impractical",
            "The correct answer emphasizes both theory and practice"
        ]
    
    def _get_difficulty(self, step_id: int) -> str:
        """Determine step difficulty."""
        if step_id < 2:
            return "beginner"
        elif step_id < 4:
            return "intermediate"
        else:
            return "advanced"
    
    def _create_fallback_step(self, topic: str, step_id: int) -> LearningStep:
        """Create fallback step if APIs fail."""
        question = f"What approach is most effective for learning {topic}?"
        correct = "Building understanding gradually with consistent practice"
        
        options = [
            correct,
            "Trying to learn everything at once",
            "Avoiding practice until you feel ready",
            "Focusing only on theory without application"
        ]
        
        random.shuffle(options)
        
        return LearningStep(
            id=step_id,
            title=self._generate_step_title(topic, step_id),
            content=f"## Learning {topic}\n\n{topic} is a valuable field that combines theoretical knowledge with practical skills. Effective learning involves understanding core concepts and applying them through practice.",
            task=question,
            correct_answer=correct,
            hints=["Start with basics", "Practice regularly", "Apply concepts"],
            difficulty=self._get_difficulty(step_id),
            options=options,
            video_url=None
        )