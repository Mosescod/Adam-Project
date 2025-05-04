from core.knowledge.sacred_scanner import SacredScanner
from core.knowledge.quran_db import QuranDatabase
from core.knowledge.mind_integrator import DivineKnowledge
from core.general_personality import AdamPersonality
from core.personality.emotional_model import EmotionalModel
from core.prophetic_responses import AdamRules
from core.memory import ConversationMemory
from core.knowledge.loader import DocumentLoader
from core.knowledge.document_db import DocumentKnowledge
from core.knowledge.synthesizer import DocumentSynthesizer
import logging
import sys
import random
from typing import Dict, Text

logger = logging.getLogger(__name__)

class AdamAI:
    def __init__(self, user_id: str = "default_user"):
        try:
            # 1. Initialize core knowledge systems
            self.scanner = SacredScanner()
            self.mind = DivineKnowledge(self.scanner.db)
            
            # 2. Load documents 
            documents = DocumentLoader.load_from_json("core/knowledge/data/documents.json")
            
            # 3. Initialize DocumentKnowledge (TF-IDF search)
            self.doc_knowledge = DocumentKnowledge()
            
            # 4. Create synthesizer with both systems
            from core.knowledge.synthesizer import DocumentSynthesizer
            self.synthesizer = DocumentSynthesizer(
                documents=documents,
                quran_db=self.scanner.db,
                doc_searcher=self.doc_knowledge  # Add TF-IDF capability
            )
            if not self.scanner.db.is_populated():
                logger.warning("Performing emergency Quran storage...")
                if not self.scanner.db.emergency_theme_rebuild():
                    raise RuntimeError("Failed to store sacred verses")
            
            # 5. Finally, create personality
            self.personality = AdamPersonality(
                username=user_id,
                synthesizer=self.synthesizer
            )
            
            self.emotional_model = EmotionalModel(user_id)
            self.prophetic_responses = AdamRules()
            
        except Exception as e:
            logger.critical(f"Creation failed: {str(e)}")
            raise RuntimeError("Adam's clay crumbled during shaping") from e
        
    def initialize_adamai():
        """Initialize AdamAI with proper error handling"""
        try:
            # Initialize database
            db = QuranDatabase()
            if not db.emergency_theme_rebuild():
                raise RuntimeError("Failed to initialize Quran database")
        
            # Initialize knowledge components
            scanner = SacredScanner()
            scanner.db = db
            mind = DivineKnowledge(db)
        
            return {
                'scanner': scanner,
                'mind': mind,
                'db': db
            }
        
        except Exception as e:
            logging.critical(f"Initialization failed: {str(e)}")
            raise

    def query(self, question: str) -> str:
        try:
            # 1. Try Quranic knowledge with emergency checks
            verse = self.mind.search_verse(question) if self.scanner.db.is_populated() else None
            if verse:
                return self._apply_emotional_formatting(verse)
            
            # 2. Check if database failed
            if not self.scanner.db.is_populated():
                logger.warning("Database empty - rebuilding...")
                if not self.scanner.db.emergency_theme_rebuild():
                    return "*clay crumbles* Failed to rebuild sacred memory"
        
        except Exception:
            return "*cracks form* Even my clay fails me...\n" + \
               "*etches in dust* Run repair_init.py"
        
    def check_sacred_memory(self) -> str:
        """Diagnostic tool for verse memory"""
        if not self.scanner.db.is_populated():
            return "*clay cracks* My sacred memory lies empty... run emergency_theme_rebuild()"
    
        verse_count = len(self.scanner.db.get_verses_by_theme('creation'))
        return f"*runs fingers over clay tablets* I hold {verse_count} inscribed verses"
    
    def _apply_emotional_formatting(self, response: str) -> str:
        """Add emotional context to responses"""
        if random.random() < 0.3:  # 30% chance to add mood description
            mood_desc = self.emotional_model.get_mood_description()
            return f"{mood_desc}\n{response}"
        
        # Let emotional model potentially modify the response
        return self.emotional_model.adjust_response_tone(response)

    def run(self):
        """Main conversation loop"""
        print("\nAdam: *brushes clay from hands* Speak, and I will answer.")
        while True:
            try:
                question = input("\nYou: ").strip()
                if not question:
                    continue
                    
                if question.lower() in ['exit', 'quit']:
                    print("\nAdam: *nods* Peace be upon thee.")
                    break
                    
                response = self.query(question)
                print(f"\nAdam: {response}")
                
            except KeyboardInterrupt:
                print("\nAdam: *brushes hands* The angel calls me away.")
                break

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("adamai.log"),
            logging.StreamHandler()
        ]
    )
    
    try:
        user_id = input("Enter your name: ").strip() or "default_user"
        ai = AdamAI(user_id)
        ai.run()
    except Exception as e:
        logger.critical(f"System failure: {str(e)}")
        print("\nAdam: *falls silent* The clay crumbles...")
        sys.exit(1)