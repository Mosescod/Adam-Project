from core.personality import AdamPersonality
from core.prophetic_responses import respond
from core.knowledge.synthesizer import DocumentSynthesizer  # Your existing RAG system
from core.knowledge.loader import DocumentLoader
from core.knowledge.mind_integrator import DivineKnowledge
from core.knowledge.sacred_scanner import SacredScanner
from core.knowledge.document_manager import DocumentManager
import signal
import sys

class AdamAI:
    def __init__(self):
        print("Initializing First Human Adam...")
        self.scanner = SacredScanner()
        self.documents = DocumentLoader.load_from_json("core/knowledge/data/documents.json")
        self.synthesizer = DocumentSynthesizer(self.documents)  # Your existing setup
        self.mind = DivineKnowledge()
        self.doc_manager = DocumentManager()
        self.doc_manager.build_knowledge_base()
        self.personality = AdamPersonality("User", self.synthesizer)

    def query(self, question: str) -> str:
        # Detect theme using NLP
        doc = self.scanner.nlp(question)
        probable_theme = max(
            self.scanner.thematic_index.keys(),
            key=lambda x: self.scanner.nlp(x).similarity(doc),
            default=None
        )
    
        if probable_theme and doc.similarity(self.scanner.nlp(probable_theme)) > 0.7:
            return self.personality.generate_thematic_response(probable_theme, question)

        """Three-tier response system"""
        # 1. Try Quranic knowledge
        if islamic_answer := self.quran.search_verse(question):
            return self.personality.generate_response(question, islamic_answer)
            
        # 2. Try document knowledge
        if doc_answer := self.synthesizer.query(question):
            return self.personality.generate_response(question, doc_answer)
            
        # 3. Fallback to rules
        return respond(question)

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

    def show_personality(self):
        """ASCII art trait display"""
        print("\nAdam's Current State:")
        for trait, value in self.personality.traits.items():
            bar = '▓' * int(value * 20) + '░' * (20 - int(value * 20))
            print(f"{trait.upper():<18} {bar} {value:.2f}")

if __name__ == "__main__":
    ai = AdamAI()
    ai.run()