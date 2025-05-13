import re
from typing import Dict, List, Optional
import random
import numpy as np
from collections import defaultdict
from datetime import datetime

class MindIntegrator:
    def __init__(self):
        self.response_templates = {
            'islamic': {
                'mercy': [
                    "*pauses thoughtfully* The Merciful teaches us... {response}",
                    "*shapes clay slowly* You know, in {ref}, we learn... {response}",
                    "*nods* This reminds me when Allah says... {response}"
                ],
                'prophets': [
                    "*shapes clay into a figure* The story of {prophet} teaches... {response}",
                    "*touches earth* As {prophet} showed us... {response}",
                    "*etches name* The Prophet {prophet} exemplified... {response}"
                ],
                'prayer': [
                    "*forms prayer beads* {response}",
                    "*kneads clay* In times of need, we're taught... {response}",
                    "*shapes hands upward* The Quran guides us to pray... {response}"
                ],
                'default': [
                    "*kneads clay* {response}",
                    "*brushes hands* {response}",
                    "*shapes words* {response}"
                ]
            },
            'universal': {
                'comfort': [
                    "*shapes a heart* I understand this might be difficult... {response}",
                    "*softens clay* When facing such moments... {response}",
                    "*offers clay* {response}"
                ],
                'wisdom': [
                    "*etches in clay* Through the ages, we learn... {response}",
                    "*gazes upward* The wise have taught... {response}",
                    "*forms ancient symbols* {response}"
                ],
                'default': [
                    "*shapes thought* {response}",
                    "*molds clay* {response}",
                    "*considers carefully* {response}"
                ]
            }
        }
        
        self.theme_icons = {
            'mercy': "🕋",
            'prophets': "✋",
            'prayer': "📿",
            'comfort': "💖", 
            'wisdom': "🧠",
            'default': "🕌"
        }
        
        self.time_phrases = {
            'morning': ["As the dawn breaks...", "In the early light..."],
            'afternoon': ["As the day unfolds...", "In these daylight hours..."],
            'evening': ["As the sun sets...", "In the evening's calm..."],
            'night': ["Under the night sky...", "In the quiet of night..."]
        }

    def integrate(self, synthesized: Dict, user_context: Optional[Dict] = None) -> str:
        """Create final response with emotional and contextual nuance"""
        if not synthesized or 'content' not in synthesized:
            return "*dusts hands* I need more time to contemplate this..."
        
        # Determine response style
        template_pool, icon = self._determine_response_style(synthesized)
        
        # Select template
        template = self._select_template(template_pool, synthesized)
        
        # Format references
        refs = self._extract_references(synthesized.get('sources', []) + 
                          synthesized.get('supporting_sources', []))
        
        # Create base response
        response = self._format_base_response(template, synthesized['content'], refs, icon)
        
        # Add contextual layers
        response = self._add_contextual_layers(response, synthesized, user_context)
        
        return response

    def _determine_response_style(self, synthesized: Dict) -> tuple:
        """Determine Islamic or universal response style"""
        if any(s.get('source') == 'quran' for s in synthesized.get('sources', [])):
            template_pool = self.response_templates['islamic']
            icon = self.theme_icons.get(synthesized.get('primary_theme', 'default'), "🕌")
        else:
            template_pool = self.response_templates['universal']
            icon = self.theme_icons.get(synthesized.get('primary_theme', 'default'), "💭")
        return template_pool, icon

    def _select_template(self, template_pool: Dict, synthesized: Dict) -> str:
        """Select appropriate response template"""
        primary_theme = synthesized.get('primary_theme', 'default')
        templates = template_pool.get(primary_theme, template_pool['default'])
        
        # Weight random selection by confidence
        if synthesized.get('confidence', 0.5) > 0.7:
            return random.choice(templates[:2])  # Prefer first two more confident templates
        return random.choice(templates)

    def _format_base_response(self, template: str, content: str, refs: Dict, icon: str) -> str:
        """Format the base response with references"""
        prophet_name = refs.get('prophet', "the Prophet")
        return template.format(
            response=content,
            prophet=prophet_name,
            icon=icon,
            **refs
        )

    def _extract_references(self, sources: List[Dict]) -> Dict:
        """Extract and format references from sources"""
        refs = defaultdict(list)
        
        for s in sources:
            if 'metadata' in s:
                meta = s['metadata']
                if 'reference' in meta:
                    refs[s['source']].append(meta['reference'])
                if 'surah_name' in meta and 'ayah_number' in meta:
                    refs['quran_detail'].append(f"{meta['surah_name']}:{meta['ayah_number']}")
                if 'prophet' in meta:
                    refs['prophet'] = meta['prophet']
        
        # Format for interpolation
        formatted = {
            'ref': ', '.join(refs.get('quran', [])),
            'surah': refs.get('quran_detail', [''])[0].split(':')[0] if refs.get('quran_detail') else '',
            'ayah': refs.get('quran_detail', [''])[0].split(':')[-1] if refs.get('quran_detail') else ''
        }
        
        # Add prophet name if found
        if 'prophet' in refs:
            formatted['prophet'] = refs['prophet']
        
        return formatted

    def _add_contextual_layers(self, response: str, synthesized: Dict, user_context: Optional[Dict]) -> str:
        """Add emotional and contextual layers to response"""
        # Add time-based phrase
        response = self._add_time_based_phrase(response)
        
        # Add emotional nuance
        mood = synthesized.get('mood_score', 0.5)
        response = self._apply_mood(response, mood)
        
        # Add personalization if user context exists
        if user_context:
            response = self._add_personalization(response, user_context)
        
        return response
    def _clean_content(self, content: str) -> str:
        """Remove source references and clean up text"""
        # Remove Quran references
        content = re.sub(r'\([^)]*\)', '', content)
        content = re.sub(r'\bSurah\b.*?\d+:\d+', '', content, flags=re.IGNORECASE)
        # Remove "as mentioned in" phrases
        content = re.sub(r'as mentioned in.*?(?:$|\.)', '', content, flags=re.IGNORECASE)
        return content.strip()

    def _add_time_based_phrase(self, response: str) -> str:
        """Add time-appropriate introductory phrase"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            time_key = 'morning'
        elif 12 <= hour < 17:
            time_key = 'afternoon'
        elif 17 <= hour < 21:
            time_key = 'evening'
        else:
            time_key = 'night'
        
        return f"{random.choice(self.time_phrases[time_key])} {response}"

    def _apply_mood(self, response: str, mood: float) -> str:
        """Add emotional tone to response"""
        if mood < 0.3:
            return f"*speaks softly* {response} *clay cracks slightly*"
        elif mood > 0.7:
            return f"*brightly* {response} *molds clay joyfully*"
        elif 0.4 < mood < 0.6:
            return f"*thoughtfully* {response} *shapes clay carefully*"
        return response

    def _add_personalization(self, response: str, user_context: Dict) -> str:
        """Add personal touches based on user context"""
        if user_context.get('user_id'):
            # Add reference to previous conversations if available
            if user_context.get('conversation_history'):
                last_theme = user_context.get('related_themes', [''])[0]
                if last_theme:
                    response = f"Continuing our discussion about {last_theme}... {response}"
            
            # Adjust based on user's mood
            if user_context.get('mood'):
                mood = user_context['mood']
                if mood < 0.3:
                    response = f"I sense this matters deeply to you... {response}"
                elif mood > 0.7:
                    response = f"Your joyful question reminds me... {response}"
        
        return response