from core.knowledge.sacred_scanner import SacredScanner
from core.knowledge.mind_integrator import DivineKnowledge
from core.personality.emotional_model import EmotionalModel
from core.prophetic_responses import respond
import logging
import sys
import random

logger = logging.getLogger(__name__)

class AdamAI:
    def __init__(self, user_id: str = "default_user"):
        logger.info("Initializing AdamAI...")
        try:
            # Initialize knowledge base
            self.scanner = SacredScanner()
            if not self.scanner.scan_entire_quran():
                raise Exception("Failed to initialize Quran database")
            
            # Initialize mind with scanner's database
            self.mind = DivineKnowledge(self.scanner.db)
            
            # Initialize emotional model
            self.emotional_model = EmotionalModel()  # No arguments needed
            
            # Initialize personality
            self.personality = EmotionalModel(user_id)
            
            logger.info("AdamAI initialization complete")
            
        except Exception as e:
            logger.critical(f"Initialization failed: {str(e)}")
            raise

    def query(self, question: str) -> str:
        """Handle user queries"""
        try:
            # Update emotional state
            self.emotional_model.update_mood(question)
            
            # Try Quranic knowledge first
            if verse := self.mind.search_verse(question):
                # Call generate_response on personality, not emotional_model
                response = self.personality.generate_response(question, verse)
                return self._apply_emotional_formatting(response)
                
            # Fallback to other methods...
            return respond(question)
            
        except Exception as e:
            logger.error(f"Query failed: {str(e)}")
            return "*molds clay* My thoughts are scattered..."

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