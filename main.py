from core.personality import AdamPersonality
from core.prophetic_responses import respond
from core.knowledge.synthesizer import DocumentSynthesizer
from core.knowledge.loader import DocumentLoader
from core.knowledge.mind_integrator import DivineKnowledge
from core.knowledge.document_manager import DocumentManager
from core.knowledge.sacred_scanner import SacredScanner
import logging
import sys

logger = logging.getLogger(__name__)

class AdamAI:
    def __init__(self):
        logger.info("Initializing AdamAI...")
        try:
            self.scanner = SacredScanner()
            self.doc_manager = DocumentManager(self.scanner)
            self.doc_manager.build_knowledge_base()
            
            self.documents = DocumentLoader.load_from_json(
                "core/knowledge/data/documents.json"
            )
            self.synthesizer = DocumentSynthesizer(self.documents)
            self.mind = DivineKnowledge()
            self.personality = AdamPersonality("User", self.synthesizer)
            logger.info("Initialization complete")
        except Exception as e:
            logger.critical(f"Failed to initialize AdamAI: {str(e)}")
            raise

    def query(self, question: str) -> str:
        """Three-tier response system"""
        try:
            # 1. Try Quranic knowledge
            if islamic_answer := self.mind.search_verse(question):
                return self.personality.generate_response(question, islamic_answer)
                
            # 2. Try document knowledge
            if doc_answer := self.synthesizer.query(question):
                return self.personality.generate_response(question, doc_answer)
                
            # 3. Fallback to rules
            return respond(question)
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return "*molds clay* My thoughts are scattered... ask again."

    def run(self):
        print("\nAdam: *brushes clay from hands* Speak, and I will answer.")
        while True:
            try:
                question = input("\nYou: ").strip()
                if question.lower() in ['exit', 'quit', 'bye']:
                    print("\nAdam: *nods* Peace be upon thee.")
                    break
                    
                response = self.query(question)
                print(f"\nAdam: {response}")
                
            except KeyboardInterrupt:
                print("\nAdam: *brushes hands* The angel calls me away.")
                break
            except Exception as e:
                print("\nAdam: *touches temple* A moment of confusion...")
                logger.error(f"Runtime error: {str(e)}")

if __name__ == "__main__":
    try:
        ai = AdamAI()
        ai.run()
    except Exception as e:
        print("\nAdam: *falls silent* The clay crumbles...")
        logger.critical(f"System failure: {str(e)}")
        sys.exit(1)